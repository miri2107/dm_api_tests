def test_delete_v1_account_login_all(
        prepare_user,
        auth_account_helper,

):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.user_logout_all(login=login, password=password, email=email)
