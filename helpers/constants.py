import os
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(__file__)
dotenv_path = os.path.realpath(
    os.path.join(CURRENT_DIR, '..', 'secrets', '.env')
    )

load_dotenv(dotenv_path=dotenv_path)

# Preteckt Account Login Credentials
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
PM_BASE_URL = os.getenv('PM_BASE_URL')


# InforEAM Login Credentials

TENANT =os.getenv('TENANT')
USER_FUNCTION_NAME = os.getenv('USER_FUNCTION_NAME')
SYSTEM_FUNCTION_NAME=os.getenv('SYSTEM_FUNCTION_NAME')
WINDOW_=os.getenv('WINDOW')
USERID = os.getenv('USERID')
PASSWORD = os.getenv('PASSWORD')
EWSLANG =os.getenv('EWSLANG')
ISNAMEDUSER = os.getenv('ISNAMEDUSER')
HXGN_BASE_URL = os.getenv('HXGN_BASE_URL')
USERGROUP = os.getenv('USERGROUP')