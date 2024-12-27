from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.api.public import APIAuthToken

from core.models import (
    PasswordSecret,
    AuditLog,
    LoginLog,
    Error,
    TracebackError,
    UserSettings,
    Notification,
    Organization,
    TeamInvitation,
    TeamMemberPermission,
    User,
    FeatureFlags,
    VerificationCodes,
    EmailSendStatus,
)

from django.conf import settings

# from django.contrib.auth.models imp/ort User
# admin.register(Invoice)
admin.site.register(
    [
        UserSettings,
        PasswordSecret,
        AuditLog,
        LoginLog,
        Error,
        TracebackError,
        Notification,
        Organization,
        TeamInvitation,
        TeamMemberPermission,
        FeatureFlags,
        VerificationCodes,
        APIAuthToken,
    ]
)

if getattr(settings, "BILLING_ENABLED", False):
    from billing.models import PlanFeature, PlanFeatureGroup, SubscriptionPlan, UserSubscription

    admin.site.register([PlanFeature, PlanFeatureGroup, SubscriptionPlan, UserSubscription])


class EmailSendStatusAdmin(admin.ModelAdmin):
    readonly_fields = ["aws_message_id"]


admin.site.register(EmailSendStatus, EmailSendStatusAdmin)

# admin.site.unregister(User)
fields = list(UserAdmin.fieldsets)  # type: ignore[arg-type]
fields[0] = (
    None,
    {
        "fields": (
            "username",
            "password",
            "logged_in_as_team",
            "awaiting_email_verification",
            "stripe_customer_id",
            "entitlements",
            "require_change_password",
        )
    },
)
UserAdmin.fieldsets = tuple(fields)
admin.site.register(User, UserAdmin)

admin.site.site_header = "Strelix Core Admin"
admin.site.index_title = "Strelix"
admin.site.site_title = "Strelix | Administration"
