# from json import loads
# import pprint
#
# from dm_api_account.apis.login_api import LoginApi
# from dm_api_account.apis.account_api import AccountApi
# from api_mailhog.apis.mailhog_api import MailhogApi
# import structlog
# from restclient.configuration import Configuration as MailhogConfiguration
# from restclient.configuration import Configuration as DmApiConfiguration
#
# structlog.configure(
#     processors=[
#         structlog.processors.JSONRenderer(
#             indent=4,
#             ensure_ascii=True
#             # sort_keys=True
#         )
#     ]
# )
#
#
# def test_put_v1_account_email():
#     mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
#     dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
#
#     account_api = AccountApi(configuration=dm_api_configuration)
#     login_api = LoginApi(configuration=dm_api_configuration)
#     mailhog_api = MailhogApi(configuration=mailhog_configuration)
#
#     login = 'IM_test_e20'
#     email = f'{login}@mail.com'
#     email_upd = f'{login}_upd@mail.com'
#     password = 'pass123456'
#
#     #  -------User registration
#
#     json_data = {
#         'login': login,
#         'email': email,
#         'password': password,
#     }
#
#     response = account_api.post_v1_account(json_data=json_data)
#
#     assert response.status_code == 201, f"User wasn't created {response.json()}"
#
#     # -------Get mail from mail server
#
#     response = mailhog_api.get_api_v2_messages()
#
#     assert response.status_code == 200, "Mails not received"
#
#     #  -------Get activation token
#
#     token = get_activation_token_by_login(login, response)
#
#     assert token is not None, f"Token not received for user {login}"
#
#     #  -------Activate user
#     response = account_api.put_v1_account_token(token)
#
#     assert response.status_code == 200, "User not activated"
#
#     # ---Log in user
#
#     login_json_data = {
#         'login': login,
#         'password': password,
#         'rememberMe': True,
#     }
#
#     response = login_api.post_v1_account_login(json_data=login_json_data)
#
#     assert response.status_code == 200, "User didn't logged in"

# ________________________!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!_________________________________
#
#     #  -------Update email
#
#     change_mail_data = {
#         'login': login,
#         'email': f'{login}_upd@mail.com',
#         'password': password,
#
#     }
#     response = account_api.put_v1_account_email(json_data=change_mail_data)
#
#     assert response.status_code == 200, "Email was not changed"
#
#     # ---Log in 2 user after changing email
#
#     response = login_api.post_v1_account_login(json_data=login_json_data)
#
#     assert response.status_code != 200, "User  logged in successfully"
#
#
#
# -------Get mail from mail server
#
#     response = mailhog_api.get_api_v2_messages()
#
#     assert response.status_code == 200, "Mails not received"
#
#     #  -------Get activation token after changing mail
#
#     token = get_activation_token_by_login_after_changing_mail(login, email_upd, response)
#
#     #  -------Activate user after changing email
#
#     response = account_api.put_v1_account_token(token)
#
#     assert response.status_code == 200, "User not activated"
#
#     # ---Log in 3 user after changing email and new activation
#
#     response = login_api.post_v1_account_login(json_data=login_json_data)
#
#     assert response.status_code == 200, "User didn't logged in"
#
#
# def get_activation_token_by_login(
#         login,
#         response
# ):
#     for item in response.json()['items']:
#         user_data = loads(item['Content']['Body'])
#         user_login = user_data['Login']
#         if user_login == login:
#             token = user_data['ConfirmationLinkUrl'].split('/')[-1]
#
#     return token
#
#
# def get_activation_token_by_login_after_changing_mail(
#         login,
#         email_upd,
#         response
# ):
#     for item in response.json()['items']:
#         mail_to = item['Raw']['To'][0]
#         if mail_to == email_upd:
#             user_data = loads(item['Content']['Body'])
#             user_login = user_data['Login']
#
#             if user_login == login:
#                 token = user_data['ConfirmationLinkUrl'].split('/')[-1]
#
#                 break
#     return token




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


def test_post_v1_account_login():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    login = 'IM_test_l20'
    email = f'{login}@mail.com'
    password = 'pass123456'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.activate_user_after_changing_mail(login=login, password=password)
    account_helper.user_login(login=login, password=password)

