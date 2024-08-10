import time
from json import loads

import allure
from retrying import retry

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from helpers.dm_db import DmDataBase
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f'Getting token attempt =  {count} ')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Exceeded the number of attempts to receive the activation token")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    db = DmDataBase('postgres', 'admin', '5.63.153.31', 'dm3.5')

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)

        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    @allure.step('New user registration')
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        self.send_registration_request(registration=registration)
        response = self.send_activation_request(login=login)
        return response

    @allure.step('Send registration request')
    def send_registration_request(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)

        dataset = self.db.get_user_by_login(login=login)
        for row in dataset:
            assert row['Login'] == login, f'User {login} not registered'
            assert row['Activated'] is False, f'User {login}  activated'
        print(dataset)
        return response

    @allure.step('Send activation request')
    def send_activation_request(
            self,
            login: str
    ):
        login = login
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 25, "Exceeded the time to activate the user"
        assert token is not None, f"Token not received for user {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        dataset = self.db.get_user_by_login(login=login)
        for row in dataset:
            assert row['Activated'] is True, f'User {login} not activated'
        print(dataset)
        return response

    @allure.step("Change user's email")
    def activate_user_after_changing_mail(
            self,
            login: str,
            password: str,

    ):

        change_email = ChangeEmail(
            login=login,
            password=password,
            email='new_email@mail.com'

        )
        self.dm_account_api.account_api.put_v1_account_email(
            change_email=change_email
        )

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Token not received for user {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @allure.step('User Authentication')
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials, validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Authorisation token not received"
        return response

    @retrier
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        time.sleep(3)
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = (loads(item['Content']['Body']))
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token

    @allure.step('Set new password')
    def change_user_password(
            self,
            login: str,
            password: str,
            new_password: str,
            email: str
    ):
        """
        authorisation token will be received in auth_client in test function
        and used via auth_account_helper
        :param login, email, password:
        :return:
        """
        reset_password = ResetPassword(
            login=login,
            email=email
        )

        change_password = ChangePassword(
            login=login,
            oldPassword=password,
            newPassword=new_password
        )

        self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        self.get_activation_token_on_changing_password(login=login)
        self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_on_changing_password(
            self,
            login
    ):
        token = None
        time.sleep(3)
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = (loads(item['Content']['Body']))
            user_login = user_data['Login']
            reset_token = user_data.get('ConfirmationLinkUri')
            if user_login == login:
                token = reset_token.split('/')[-1]
            return token

    def user_logout(
            self,
            login: str,
            email: str,
            password: str
    ):

        self.create_user(login=login, password=password, email=email)
        self.dm_account_api.account_api.delete_v1_account_login()

    def user_logout_all(
            self,
            login: str,
            email: str,
            password: str
    ):

        self.create_user(login=login, password=password, email=email)
        self.dm_account_api.account_api.delete_v1_account_login_all()

    def create_user(
            self,
            login: str,
            email: str,
            password: str
    ):
        """
        register user and get authorisation token
        :param login, email, password:
        :return:
        """
        self.register_new_user(login=login, password=password, email=email)
        self.auth_client(login=login, password=password)
