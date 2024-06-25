import time
from json import loads

from retrying import retry

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

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                'login': login,
                'password': password
            }
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"User wasn't created {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Token not received for user {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "User not activated"
        return response

    def activate_user_after_changing_mail(
            self,
            login: str,
            password: str,

    ):
        change_mail_data = {
            'login': login,
            'email': f'{login}_upd@mail.com',
            'password': password,

        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=change_mail_data)
        assert response.status_code == 200, "Email was not changed"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Token not received for user {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "User not activated"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)

        assert response.status_code == 200, "User not logged in"
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

    def change_user_password(
            self,
            login: str,
            email: str,
            password: str,
            new_password: str
    ):
        """
        authorisation token will be received in auth_client in test function
        and used via auth_account_helper
        :param login, email, password:
        :return:
        """
        json_data = {
            'login': login,
            'oldPassword': password,
            'email': email,
            'newPassword': new_password
        }

        self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        self.get_activation_token_on_changing_password(login=login)
        self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)

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
