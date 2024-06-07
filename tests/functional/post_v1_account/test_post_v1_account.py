from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # ---User registration
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'IM_test_user_17'
    email = f'{login}@mail.com'
    password = 'pass123458'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code, '  - User creation status code')
    print(response.text)
    assert response.status_code == 201, f"User wasn't created {response.json()}"

    # ---Get email from mail server

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code, ' - Get mails status code')
    assert response.status_code == 200, "Mails not received"

    # ---Get activation token
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Token not received for user {login}"

    # ---User activation
    response = account_api.put_v1_account_token(token)

    print(response.status_code, ' - User activation status code')
    assert response.status_code == 200, "User not activated"

    # ---Log in user

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code, ' - Login status code for', login)
    print(response.text)
    assert response.status_code == 200, "User didn't logged in"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = (loads(item['Content']['Body']))
        user_login = user_data['Login']

        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(response.status_code, ' - Get activation token status code')
    return token