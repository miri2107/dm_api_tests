import requests

from dm_api_account.models.registration import Registration
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def post_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def put_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        headers = {
            'accept': 'text/plain',
        }
        """
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
            self,
            json_data,
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs

    ):
        """
        Logout as current user
        :param json_data:
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(
            self,
            **kwargs

    ):
        """
        Logout as current user from every device
        :param json_data:
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response
