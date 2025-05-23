_USER = ''
_PASSWORD = ''
_HOST = ''
_PORT = ''
_DATABASE_NAME = ''
_driver = ''

def get_conn_string(db_driver: str) -> str:
    if db_driver == 'postgresql':
        _driver = 'postgresql+psycopg2'
    elif db_driver == 'mysql':
        _driver = "mysql+pymysql"
    else:
        return "ERROR"

    return f"{_driver}://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_DATABASE_NAME}"