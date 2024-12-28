from django.db.models import QuerySet

from core.models import Organization
from core.types.requests import WebRequest


def get_all_users_teams(request: WebRequest) -> QuerySet[Organization]:
    return request.user.teams_joined.all() | request.user.teams_leader_of.all()
