from hamcrest import (
    assert_that,
    has_property)

def test_get_v1_account_auth(
        prepare_user,
        account_helper,
        auth_account_helper,

):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    auth_account_helper.create_user(login=login, password=password, email=email)
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    print(response)
    assert_that(
        response, has_property("resource"))


<<<<<<< HEAD

def test_get_v1_account_no_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.create_user(login=login, password=password, email=email)
    account_helper.dm_account_api.account_api.get_v1_account()
=======
# def test_get_v1_account_no_auth(
#         account_helper,
#         prepare_user
# ):
#     login = prepare_user.login
#     password = prepare_user.password
#     email = prepare_user.email
#
#     account_helper.create_user(login=login, password=password, email=email)
#     account_helper.dm_account_api.account_api.get_v1_account()
>>>>>>> b35a083 (add hamcrest)
