import allure


@allure.suite('Tests to validate method DELETE /v1/account/login ')
@allure.sub_suite('Tests positive')
@allure.title('Check user logout')
def test_delete_v1_account_login(
        prepare_user,
        auth_account_helper,

):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.user_logout(login=login, password=password, email=email)
