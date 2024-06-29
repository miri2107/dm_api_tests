import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_token():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    login = 'IM_test_a25'
    email = f'{login}@mail.com'
    password = 'pass123456'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
