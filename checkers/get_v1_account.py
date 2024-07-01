from assertpy import assert_that
from hamcrest import (
    has_property,
    has_item,
    has_properties,
)


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
            ):
        assert_that(
            response,
            has_property('resource', has_property('roles', has_item('Player'))),
        )
        assert_that(
            (response,
             has_properties(
                 {
                     'medium_picture_url': 'No',
                     'status': 'None'
                 }
             )
             )
            )
