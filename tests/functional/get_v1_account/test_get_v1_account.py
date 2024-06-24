def test_get_v1_account_auth(
        prepare_user,
        auth_account_helper,

):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    auth_account_helper.register_new_user(login=login, password=password, email=email)
    auth_account_helper.auth_client(login=login, password=password)
    auth_account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(
        account_helper
):
    account_helper.dm_account_api.account_api.get_v1_account()
