import contextlib
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from it_one_test_task.services.search import search_logs_by_email
from it_one_test_task.settings import Settings
from it_one_test_task.utils import get_session_manager


settings = Settings()
session_manager = get_session_manager(url=settings.db.get_url(), echo=settings.db.log_sql)


async def get_db_session() -> 'AsyncIterator[AsyncSession]':
    async with session_manager.session() as session:
        yield session


DBSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> 'AsyncIterator[None]':
    yield
    try:
        await session_manager.close()
    except Exception:
        pass


app = FastAPI(lifespan=lifespan)


@app.get('/', response_class=HTMLResponse)
async def root():
    return FileResponse('public/index.html')


@app.post('/search')
async def search(db_session: DBSessionDependency, email: str = Form(...)):
    limit = 100
    results = list(await search_logs_by_email(session=db_session, email=email, limit=limit + 1))
    has_more = len(results) > limit
    return {'items': results[:limit], 'hasMore': has_more}
