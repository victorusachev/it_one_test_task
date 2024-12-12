import contextlib
from typing import TYPE_CHECKING, Any, AsyncIterator

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession


class SessionManager:
    def __init__(self, url: str | URL, engine_kwargs: dict[str, Any] | None = None) -> None:
        self._engine = create_async_engine(url=url, **engine_kwargs)
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @contextlib.asynccontextmanager
    async def connect(self) -> 'AsyncIterator[AsyncConnection]':
        self._check_engine()

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> 'AsyncIterator[AsyncSession]':
        self._check_sessionmaker()

        session = self._session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        self._check_engine()
        await self._engine.dispose()

        self._engine = None
        self._session_maker = None

    def _check_engine(self) -> None:
        if not self._engine:
            raise Exception('Database session manager is not initialized')

    def _check_sessionmaker(self) -> None:
        if not self._session_maker:
            raise Exception('Database session manager is not initialized')
