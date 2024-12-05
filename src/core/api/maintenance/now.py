from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from login_required import login_not_required

from core.service.maintenance.tasks import execute_maintenance_tasks, get_maintenance_tasks
from core.service.webhooks.auth import authenticate_api_key

from core.service.maintenance.expire.run import expire_and_cleanup_objects

import logging

from core.types.requests import WebRequest

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
@login_not_required
def handle_maintenance_now_endpoint(request: WebRequest):
    logger.info("Received routine cleanup handler. Now authenticating...")
    api_auth_response = authenticate_api_key(request)

    if api_auth_response.failed:
        logger.info(f"Maintenance auth failed: {api_auth_response.error}")
        return JsonResponse({"message": api_auth_response.error, "success": False}, status=api_auth_response.status_code or 400)

    output_str = execute_maintenance_tasks(get_maintenance_tasks())
    logger.info(output_str)
    return JsonResponse({"message": output_str, "success": True}, status=200)
