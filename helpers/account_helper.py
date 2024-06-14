from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

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
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Mails not received"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Token not received for user {login}"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "User not activated"
        return response


    #  Activate user after changing mail
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
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Mails not received"
        token = self.get_activation_token_by_login(login=login, response=response)
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
        return response

    @staticmethod
    def get_activation_token_by_login(
            login,
            response
    ):
        token = None
        for item in response.json()['items']:
            user_data = (loads(item['Content']['Body']))
            user_login = user_data['Login']

            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token
