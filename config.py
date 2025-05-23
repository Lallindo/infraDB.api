_USER = 'root'
_PASSWORD = 'root'
_HOST = 'localhost'
_PORT = '3306'
_DATABASE_NAME = 'produtos_tiny'
_driver = ''

def get_conn_string(db_driver: str) -> str:
    if db_driver == 'postgresql':
        _driver = 'postgresql+psycopg2'
    elif db_driver == 'mysql':
        _driver = "mysql+pymysql"
    else:
        return "ERROR"

    return f"{_driver}://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}/{_DATABASE_NAME}"