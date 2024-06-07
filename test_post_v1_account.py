import requests


def test_post_v1_account():
    # User registration
    login = 'IM_test_user_7'
    email = f'{login}@mail.com'
    password = 'pass123456'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)

    print(response.status_code)
    print(response.text)
    # Get email from mail server

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)

    print(response.status_code)
    print(response.text)

    # Get activation token
    ...
    # User activation
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/5e6cbe19-6172-4210-85f4-dc320ba9c11a', headers=headers)

    print(response.status_code)
    print(response.text)
    # Log in user

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)

    print(response.status_code)
    print(response.text)
