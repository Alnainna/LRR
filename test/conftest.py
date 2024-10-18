import os
import pytest
from selenium import webdriver


@pytest.fixture
def restore_database():
    ''' Restore the database.
        It is useful for making sure that each end-to-end test
        starts with the same database.
        Benefit: we can reproduce the same test result.
    '''

    PASSWORD = 'p-@va9'  # root password
    DB_NAME = 'lrr' # database name used for LRR

    # commands used to import data to DB_NAME
    cmds = [
        f'mysql -u root -p{PASSWORD} -e "DROP DATABASE IF EXISTS {DB_NAME};"',        
        f'mysql -u root -p{PASSWORD} -e "CREATE DATABASE {DB_NAME};"',
        f'mysql -u root -p{PASSWORD} -e "GRANT ALL PRIVILEGES ON {DB_NAME}.* TO lrr@localhost WITH GRANT OPTION;"',
        f'mysql -u root -p{PASSWORD} {DB_NAME} < ../lrr_database.sql']

    for command in cmds:
        os.system(command)
    return None


@pytest.fixture
def url():
    return 'http://localhost/LRR/' # URL of LRR


@pytest.fixture
def driver():
    return  webdriver.Chrome()


@pytest.fixture
def admin_username():
    return 'admin@qq.com'


@pytest.fixture
def admin_password():
    return '123'
