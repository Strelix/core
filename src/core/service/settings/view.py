from django.db.models import QuerySet

from core.api.public import APIAuthToken
from core.models import UserSettings

# from core.service.defaults.get import get_account_defaults
from core.types.requests import WebRequest


def validate_page(page: str | None) -> bool:
    return not page or page in ["profile", "account", "api_keys", "account_defaults", "account_security", "email_templates"]


def get_user_profile(request: WebRequest) -> UserSettings:
    try:
        usersettings = request.user.user_profile
    except UserSettings.DoesNotExist:
        # Create a new UserSettings object
        usersettings = UserSettings.objects.create(user=request.user)
    return usersettings


def get_api_keys(request: WebRequest) -> QuerySet[APIAuthToken]:
    return APIAuthToken.filter_by_owner(request.actor).filter(active=True).only("created", "name", "last_used", "description", "expires")


def get_account_page_context(request: WebRequest, context: dict) -> None:
    user_profile = get_user_profile(request)
    context.update({"currency_signs": user_profile.CURRENCIES, "currency": user_profile.currency})


def api_keys_page_context(request: WebRequest, context: dict) -> None:
    api_keys = get_api_keys(request)
    context.update({"api_keys": api_keys})


def account_defaults_context(request: WebRequest, context: dict) -> None:
    ...
    # context.update({"account_defaults": get_account_defaults(request.actor)})


def profile_context(request: WebRequest, context: dict) -> None: ...


def account_security_context(request: WebRequest, context: dict) -> None: ...
