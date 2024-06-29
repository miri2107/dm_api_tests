import requests

from restclient.client import RestClient


class MailhogApi(RestClient):


    def get_api_v2_messages(
            self,
            limit=50
    ):
        params = {
            'limit': limit,
        }
        """
        Get user emails
        :return:
        """
        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response
