import logging

from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from core.config import CoreConfig
from core.types.requests import WebRequest
from core.models import TracebackError


@require_http_methods(["GET"])
def view_settings_page_endpoint(request: WebRequest, page: str | None = None):
    context = {}

    # If no page is provided, default to the 'profile' page
    if not page:
        template = "core/settings/pages/profile.html"
        # Check if 'on_main' query parameter is present to decide layout
        if not request.GET.get("on_main"):
            context["page_template"] = template
            return render(request, "core/settings/main.html", context)
        return render(request, template, context)

    # If a page is provided, look for its handler
    handler_path = CoreConfig().SETTINGS_PAGE_CONTEXT_HANDLERS.get(page)

    if not handler_path:
        logging.error(f"Settings page handler not found for {page}")
        messages.error(request, "Settings page not found")
        if request.htmx:
            return render(request, "core/base/toast.html")
        return redirect("core:settings:dashboard")

    # Extract the module path and function name from the handler path
    module_path, func_name = handler_path.rsplit(".", 1)

    try:
        # Dynamically import the module and get the handler function
        module = __import__(module_path, fromlist=[func_name])
        context_function = getattr(module, func_name)
        context_function(request, context)  # Call the handler function to fill the context
    except (ImportError, AttributeError) as e:
        print(e)
        messages.error(request, f"Settings page handler not implemented for {page}. Please contact the site support.")
        TracebackError.objects.create(user=request.user, error=f"Settings page handler not implemented for {page}")
        if request.htmx:
            return render(request, "core/base/toast.html")
        return redirect("core:settings:dashboard")

    # Default template for the provided page
    template = f"core/settings/pages/{page}.html"

    # Check if 'on_main' query parameter is present to decide layout
    if not request.GET.get("on_main"):
        context["page_template"] = template
        return render(request, "core/settings/main.html", context)

    # Otherwise, render the page directly
    response = render(request, template, context)
    response.no_retarget = True  # type: ignore[attr-defined]
    return response


def change_password(request: WebRequest):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        error = validate_password_change(request.user, current_password, password, confirm_password)

        if error:
            messages.error(request, error)
            return redirect("core:settings:change_password")

        # If no errors, update the password
        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Successfully changed your password.")
        return redirect("core:settings:dashboard")

    return render(request, "pages/reset_password.html", {"type": "change"})


def validate_password_change(user, current_password, new_password, confirm_password):
    if not user.check_password(current_password):
        return "Incorrect current password"

    if new_password != confirm_password:
        return "Passwords don't match"

    if not new_password:
        return "Something went wrong, no password was provided."

    if len(new_password) < 8 or len(new_password) > 128:
        return "Password must be between 8 and 128 characters."

    return None
