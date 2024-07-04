from assertpy import (
    soft_assertions,
    assert_that,
)
from dm_api_account.models.user_details_envelope import UserRole
import allure


@allure.suite('Tests to validate method POST /v1/account/login ')
@allure.sub_suite('Tests positive')
@allure.title('Check user login')
def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    response = account_helper.register_new_user(login=login, password=password, email=email)
    print(response)

    with soft_assertions():
        assert_that(response.resource.login).starts_with('IM')
        assert_that(response.resource.status).is_equal_to(None)
        assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
    account_helper.user_login(login=login, password=password)
