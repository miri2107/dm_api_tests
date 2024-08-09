import allure


@allure.suite('Tests to validate method PUT /v1/account/password ')
@allure.sub_suite('Tests positive')
@allure.title('Check changing password for user')
def test_put_v1_account_password(
        account_helper,
        prepare_user,
        auth_account_helper
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = prepare_user.new_password

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    auth_account_helper.auth_client(login=login, password=password)
    auth_account_helper.change_user_password(login=login, password=password, email=email, new_password=new_password)
    account_helper.user_login(login=login, password=new_password)
