from checkers.get_v1_account import GetV1Account
from checkers.https_checkers import check_status_code_http
import allure


@allure.suite('Tests to validate method GET /v1/account')
@allure.sub_suite('Tests positive')
@allure.title('Check getting user info for authorised client')
def test_get_v1_account_auth(
        prepare_user,
        account_helper,
        auth_account_helper,
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.create_user(login=login, password=password, email=email)

    with check_status_code_http(200):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        print(response)
        GetV1Account.check_response_values(response)


@allure.suite('Tests to validate method GET /v1/account')
@allure.sub_suite('Tests positive')
@allure.title('Check getting user info for non-authorised client')
def test_get_v1_account_no_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
