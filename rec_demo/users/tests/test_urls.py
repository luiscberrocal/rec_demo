import pytest
from django.conf import settings
from django.urls import resolve, reverse

from rec_demo.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/{settings.LANGUAGE_CODE}/users/{user.username}/"
    )
    assert resolve(f"/{settings.LANGUAGE_CODE}/users/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == f"/{settings.LANGUAGE_CODE}/users/~update/"
    assert resolve(f"/{settings.LANGUAGE_CODE}/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == f"/{settings.LANGUAGE_CODE}/users/~redirect/"
    assert resolve(f"/{settings.LANGUAGE_CODE}/users/~redirect/").view_name == "users:redirect"
