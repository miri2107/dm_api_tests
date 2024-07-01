from collections import namedtuple
from datetime import datetime

import pytest
from pathlib import Path

from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

import structlog
from vyper import v
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True
            # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'service.login',
    'service.password'
)


@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
        ):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))


def pytest_addoption(
        parser
        ):
    parser.addoption('--env', action='store', default='stg', help='run stg')

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"))
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope="class")
def prepare_user():
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'IM_test_{date}'
    email = f'{login}@mail.com'
    password = v.get('user.password')
    new_password = 'pass_new'
    User = namedtuple("User", ["login", "password", "email", "new_password"])
    user = User(login=login, password=password, email=email, new_password=new_password)
    print(login, email)
    return user


@pytest.fixture(scope="class")
def auth_account_helper(
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(
        host=v.get('service.dm_api_account'), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get('user.login'),
        password=v.get('user.password')
    )
    return account_helper
