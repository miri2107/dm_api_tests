import allure
import pytest
from checkers.https_checkers import check_status_code_http

from datetime import datetime

from checkers.post_v1_account import PostV1Account
from helpers.dm_db import DmDataBase

now = datetime.now()
current_time = now.strftime("%d%H%M%S")

data = [
    # Positive test: correct registration data
    {
        "login": f"my_login_{current_time}",
        "password": "pass123456",
        "email": f"email_{current_time}@mail.com",
        "expected_status_code": 200,

    },
    # Negative tests:
    # short login
    {
        "login": "m",
        "password": "pass123456",
        "email": "email_45@mail.com",
        "expected_status_code": 400,
        "expected_message": "Validation failed"
    },
    # short password
    {
        "login": "my_login_46",
        "password": "p",
        "email": "my_email_46@mail.com",
        "expected_status_code": 400,
        "expected_message": "Validation failed"

    },
    # incorrect email
    {
        "login": "my_login_47",
        "password": "pass123456",
        "email": "email_47",
        "expected_status_code": 400,
        "expected_message": "Validation failed"
    }
]


@allure.suite('Tests to validate method POST /v1/account ')
@allure.sub_suite('Tests positive')
class TestsPostV1Account:

    @allure.title('Check new user registration')
    @pytest.mark.parametrize('test_data', data)
    def test_post_v1_account(
            self,
            account_helper,
            test_data
    ):
        login = test_data.get('login')
        password = test_data.get('password')
        email = test_data.get('email')
        expected_message = test_data.get('expected_message')
        expected_status_code = test_data.get('expected_status_code')

        db = DmDataBase('postgres', 'admin', '5.63.153.31', 'dm3.5')

        with check_status_code_http(expected_status_code, expected_message):
            response = account_helper.register_new_user(login=login, password=password, email=email)
            print(response)
            if response:
                response = account_helper.user_login(login=login, password=password, validate_response=True)
                PostV1Account.check_response_values(response)
