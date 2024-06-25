def test_delete_v1_account_login_all(
        prepare_user,
        auth_account_helper,

):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.register_new_user(login=login, password=password, email=email)
    auth_account_helper.auth_client(login=login, password=password)
    auth_account_helper.dm_account_api.account_api.delete_v1_account_login_all()