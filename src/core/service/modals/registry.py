import logging
from abc import abstractmethod, ABC

from django.http import HttpResponse
from django.shortcuts import render

from core.types.requests import WebRequest

modal_registry = {}


class Modal(ABC):
    modal_name = None  # Override in subclasses
    template_name = None  # Override in subclasses
    context = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls.modal_name:
            raise ValueError(f"Modal class {cls.__name__} must define a `modal_name`.")
        if cls.modal_name in modal_registry:
            logging.info(f"Modal {cls.modal_name} is being overridden by {cls.__name__}.", UserWarning)
        modal_registry[cls.modal_name] = cls

    def get_context(self, request) -> dict:
        """Aggregate context data from classes that explicitly define a `get_context` method."""
        context = {}

        for base in self.__class__.mro():
            # Ensure the base has a distinct `get_context` method to avoid infinite recursion
            if base is Modal:
                continue
            if "get_context" in base.__dict__:
                # logging.debug(f"Gathering context from: {base.__name__}")
                base_context = base.get_context(self, request)
                context.update(base_context)
        return context

    def get(self, request: WebRequest):
        """Populate the context with all inherited context mixins, then return the response."""
        context = self.get_context(request)
        return render(request, self.template_name or f"modals/{self.modal_name}.html", context)

    def get_template_name(self):
        return self.template_name or f"modals/{self.modal_name}.html"

    class _Response:
        def __init__(self, modal_instance, request, context=None, template=None):
            self.modal_instance = modal_instance
            self.request = request
            self.context = context or modal_instance.get_context(request)
            self.template = template or modal_instance.get_template_name()

        def render(self) -> HttpResponse:
            """Return the rendered response."""
            return render(self.request, self.template, self.context)

    def Response(self, request, context=None, template=None) -> HttpResponse:
        """Shortcut to create and render a response."""
        return self._Response(self, request, context, template).render()


def get_modal(name):
    return modal_registry.get(name)


# EXAMPLE MODAL

# class LogoutModal(Modal):
#     modal_name = 'logout'
#
#     def get(self, request: WebRequest, *args, **kwargs):
#         context = {'message': 'Are you sure you want to log out?'}
#         return self.Response(request, context)
