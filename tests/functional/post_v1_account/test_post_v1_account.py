import pytest
from checkers.https_checkers import check_status_code_http

from datetime import datetime

from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    equal_to,
    has_properties,
)

data = [
    # Positive test: correct registration data
    {
        "login": "my_login40",
        "password": "pass123456",
        "email": "email_40@mail.com",
        "expected_status_code": 200,

    },
    # Negative tests:
    # short login
    {
        "login": "m",
        "password": "pass123456",
        "email": "email_41@mail.com",
        "expected_status_code": 400,
        "expected_message": "Validation failed"
    },
    # short password
    {
        "login": "my_login_42",
        "password": "p",
        "email": "my_email_42@mail.com",
        "expected_status_code": 400,
        "expected_message": "Validation failed"

    },
    # incorrect email
    {
        "login": "my_login_43",
        "password": "pass123456",
        "email": "email_43",
        "expected_status_code": 400,
        "expected_message": "Validation failed"
    }
]


@pytest.mark.parametrize('test_data', data)
def test_post_v1_account(
        account_helper,
        test_data
):
    login = test_data.get('login')
    password = test_data.get('password')
    email = test_data.get('email')
    expected_message = test_data.get('expected_message')
    expected_status_code = test_data.get('expected_status_code')

    with check_status_code_http(expected_status_code, expected_message):
        response = account_helper.register_new_user(login=login, password=password, email=email)
        print(response)
        if response:
            response = account_helper.user_login(login=login, password=password, validate_response=True)

            assert_that(
                response, all_of(
                    has_property("resource", has_property('login', starts_with('my'))),

                    has_property("resource", has_property('registration', instance_of(datetime))),
                    has_property(
                        "resource", has_properties(
                            {
                                "rating": has_properties(
                                    {
                                        "enabled": equal_to(True),
                                        "quality": equal_to(0),
                                        "quantity": equal_to(0)
                                    }
                                )
                            }
                        )
                    )
                )
            )

            print(response)
