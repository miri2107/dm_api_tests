def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    response = account_helper.register_new_user(login=login, password=password, email=email)
    print(response)
    account_helper.user_login(login=login, password=password)
