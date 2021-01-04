import pytest
from django.conf import settings

from rec_demo.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/{settings.LANGUAGE_CODE}/users/{user.username}/"
