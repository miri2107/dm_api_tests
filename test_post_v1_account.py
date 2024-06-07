import pprint
import requests
from json import loads


def test_post_v1_account():
    # ---User registration
    login = 'IM_test_user_12'
    email = f'{login}@mail.com'
    password = 'pass123458'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)

    print(response.status_code, '  - User creation status code')
    print(response.text)
    assert response.status_code == 201, f"User wasn't created {response.json()}"


    # ---Get email from mail server

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code, ' - Get mails status code')
    print(response.text)
    assert response.status_code == 200, "Mails not received"

    # ---Get activation token

    for item in response.json()['items']:
        user_data = (loads(item['Content']['Body']))
        user_login = user_data['Login']
        token = None
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(response.status_code, ' - Get activation token status code')
            print('for user ', login)
            print('token:', token)

        assert token is not None, f"Token not received for user {login}"

    ...
    # ---User activation
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)

    print(response.status_code, ' - User activation status code')
    assert response.status_code == 200, "User not activated"

    # ---Log in user

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)

    print(response.status_code, ' - Login status code for', login)
    print(response.text)
    assert response.status_code == 200, "User didn't logged in"
