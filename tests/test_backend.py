import logging

import pytest
from conftest import get_valid_customer

from interfaces.parabank_backend_api import BackendAPI, CustomerProfile

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("customer_profile", get_valid_customer())
def test_get_login_valid_credentials(
    customer_profile: CustomerProfile, backend_api: BackendAPI
) -> None:
    response_customer = backend_api.misc_controller.get_login(
        customer_profile.credentials
    )
    assert response_customer.id == customer_profile.data.id
