from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from core.api.public import APIAuthToken
from core.api.public.permissions import SCOPE_DESCRIPTIONS
from core.models import UserSettings, Organization
from core.service.modals.registry import Modal
from core.types.requests import WebRequest


# class LogoutModal(Modal):
#     modal_name = 'logout'
#
#     def get(self, request: WebRequest, *args, **kwargs):
#         return HttpResponse("logout_modal.html")


class PermissionModalContext:
    def get_context(self, request: WebRequest) -> dict:
        # example
        # "clients": {
        #     "description": "Access customer details",
        #     "options": ["read", "write"]
        # }
        return {
            "permissions": [
                {"name": group, "description": perms["description"], "options": perms["options"]}
                for group, perms in SCOPE_DESCRIPTIONS.items()
            ],
            "APIAuthToken_types": APIAuthToken.AdministratorServiceTypes,
        }


class GenerateAPIKeyModal(Modal, PermissionModalContext):
    modal_name = "generate_api_key"


class PassTeamIdContext:
    def get_context(self, request: WebRequest) -> dict:
        return {
            "team_id": request.GET.get("team"),
        }


class TeamCreateUserModal(Modal, PermissionModalContext, PassTeamIdContext):
    modal_name = "team_create_user"

    def get(self, request: WebRequest):
        context = self.get_context(request)
        context["team_id"] = request.GET.get("team")
        return self.Response(request, context)


class CreateTeamModal(Modal):
    modal_name = "create_team"


class EditTeamMemberPermissions(Modal, PermissionModalContext):
    modal_name = "edit_team_member_permissions"
    template_name = "modals/edit_team_member_permissions.html"

    def get(self, request: WebRequest):
        context = self.get_context(request)

        team = request.user.logged_in_as_team

        if not team:
            messages.error(request, "You are not logged in as a team")
            return render(request, "core/base/toast.html", context)

        for_user = team.members.filter(id=request.GET.get("user")).first()
        for_user_perms = team.permissions.filter(user=for_user).first()

        if not for_user:
            messages.error(request, "User not found")
            return render(request, "core/base/toast.html", context)

        context["editing_user"] = for_user
        context["user_current_scopes"] = for_user_perms.scopes if for_user_perms else []

        return self.Response(request, context)


class ChangeProfilePictureModal(Modal):
    modal_name = "change_profile_picture"

    def get(self, request: WebRequest):
        context = self.get_context(request)

        try:
            context["users_profile_picture"] = request.user.user_profile.profile_picture_url
        except UserSettings.DoesNotExist:
            pass

        return self.Response(request, context)


class LeaveTeamModal(Modal):
    modal_name = "leave_team"

    def get(self, request: WebRequest):
        context = self.get_context(request)

        if request.user.teams_joined.filter(id=request.GET.get("team")).exists():
            context["team"] = Organization.objects.filter(id=request.GET.get("team")).first()

        return self.Response(request, context)


class InvoiceUserToTeamModal(Modal, PassTeamIdContext):
    modal_name = "invite_user_to_team"
