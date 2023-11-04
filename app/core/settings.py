from dotenv import load_dotenv
from os.path import abspath, dirname, sep, exists
from os import getenv

ROOT_PATH = dirname(dirname(dirname(abspath(__file__))))

ENV_FILE = ROOT_PATH + sep + ".env"

if exists(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE)
else:
    print(f'{ENV_FILE} - not exist')

DATABASE_FILE = getenv('DATABASE_FILE', 'sqlite_example.db')
DATABASE_PATH = ROOT_PATH + sep + 'app' + sep + DATABASE_FILE
DSN = f'sqlite+aiosqlite:///{DATABASE_PATH}'
DB_CLEAR_AT_THE_END = getenv("CLEAR_DB_AT_THE_END", 'False').lower() \
                      in ('true', '1', 't')

SECRET_KEY = getenv(
    'SECRET_KEY',
    'BJeoP/3zVHPWJwnmeRurIt27vb8nu0M98BpYJE3xFE='
)
ALGORITHM = getenv('ALGORITHM', 'HS256')
TOKEN_EXPIRE_MINUTES = int(getenv('TOKEN_EXPIRE_MINUTES', '30'))

PROJECT_NAME = getenv('PROJECT_NAME', 'Example')
API_PORT = int(getenv('API_PORT', '8000'))

print('init settings')
