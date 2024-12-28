from __future__ import annotations

from django.http import HttpResponseBadRequest
from core.service.modals.registry import get_modal
from core.types.requests import WebRequest


def open_modal_endpoint(request: WebRequest, modal_name):
    modal_class = get_modal(modal_name)
    if not modal_class:
        print(f"Modal {modal_name} not found.")
        return HttpResponseBadRequest("Something went wrong with loading this modal.")
    modal_instance = modal_class()
    return modal_instance.get(request)
