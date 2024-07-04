from datetime import datetime

import allure
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    equal_to,
    has_properties,
)

from assertpy import (
    soft_assertions,
    assert_that,
)


class PostV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
            ):
        with allure.step('Response verification'):
            today = datetime.now().strftime('%Y-%m-%d')
            assert_that(str(response.resource.registration), starts_with(today))
            assert_that(
                response, all_of(
                    has_property("resource", has_property('login', starts_with('my'))),

                    has_property("resource", has_property('registration', instance_of(datetime))),
                    has_property(
                        "resource", has_properties(
                            {
                                "rating": has_properties(
                                    {
                                        "enabled": equal_to(True),
                                        "quality": equal_to(0),
                                        "quantity": equal_to(0)
                                    }
                                )
                            }
                        )
                    )
                )
            )
            print(response)
