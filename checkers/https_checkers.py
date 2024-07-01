import requests


from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = ""
):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Expected status code should be equal to {expected_status_code} ")
        if expected_message:
            raise AssertionError(f'Expected to get message "{expected_message}", but request was successful')
        else:
            return

    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()['title'] == expected_message
