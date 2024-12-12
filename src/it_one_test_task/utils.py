from sqlalchemy import URL

from it_one_test_task.db.manager import SessionManager


def get_session_manager(url: str | URL, echo: bool = False) -> 'SessionManager':
    engine_kwargs = {'echo': echo}
    if application_name := url.query.get('application_name'):
        query =  dict(url.query)
        query.pop('application_name')
        url = url.set(query=query)
        engine_kwargs['connect_args'] = {'server_settings': {'application_name': application_name}}
    return SessionManager(url=url, engine_kwargs=engine_kwargs)
