import allure


@allure.suite('Tests to validate method PUT /v1/account/{token} ')
@allure.sub_suite('Tests positive')
@allure.title('Check getting user authentication token')

def test_put_v1_account_token(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
