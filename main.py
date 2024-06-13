import requests
import pprint

# url = 'http://5.63.153.31:5051/v1/account'
#
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
#
# json = {
#     'login': 'IM_test_user_5',
#     'email': 'IM_test_user_5@mail.com',
#     'password': 'pass123456',
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )
#
# url = 'http://5.63.153.31:5051/v1/account/1efe497a-e32c-4b3c-804c-a7c0c7a001d9'
#
# headers = {
#     'accept': 'text/plain',
# }
#
# response = requests.put(
#     url=url,
#     headers=headers,
#
# )
#
# print(response.status_code)
# pprint.pprint(response.json())
# response_json = response.json()
# print(response_json['resource']['roles'][1])

from json import loads
import pprint

from dm_api_account.apis.login_api import LoginApi
from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi

def test_put_v1_account_email2():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'IM_test_16'
    email = f'{login}@mail.com'
    password = 'pass123456'

# -------Get mail from mail server

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code, ' - Get mails status code')
    assert response.status_code == 200, "Mails not received"


    #  -------Get activation token

    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Token not received for user {login}"


#  -------Activate user
    response = account_api.put_v1_account_token(token)
    for item in response.json()['items']:
        user_data = (loads(item['Content']['Body']))
        print(user_data)

    print(response.status_code, ' - User activation status code')
    assert response.status_code == 200, "User not activated"

    login = 'IM_test_16'
    email = f'{login}@mail.com'
    password = 'pass123456'

    # ---Get activation2 token for email

    def get_activation2_token_by_login(
            login,
            email,
            response
    ):
        for item in response.json()['items']:
            print(item)
            # user_data = (loads(item['Content']['Body']))
            # user_login = user_data['Login']
    #         token = None
    #         if user_login == login:
    #             token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    #             print(response.status_code, ' - Get activation token status code')
    #             print('for user ', login)
    #             print('token:', token)
    #
    #         assert token is not None, f"Token not received for user {login}"

def get_activation_token_by_login(
        login,
        email,
        response
):
    for item in response.json()['items']:
        user_data = (loads(item['Content']['Body']))
        # mail_to = (loads(item['To']['Mailbox']))
        user_login = user_data['Login']
        # user_email = mail_to
        # pprint.pprint((user_email, user_login))
        if user_login == login :
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(login, token)
    return token



