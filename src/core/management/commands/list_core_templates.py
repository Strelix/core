from django.core.management.base import BaseCommand
from django.template.utils import get_app_template_dirs


class Command(BaseCommand):
    help = "List core template files"

    def handle(self, *args, **options):
        app_template_dirs = get_app_template_dirs("templates")
        app_template_dirs = map(lambda a: "TMPL:" + str(a), app_template_dirs)
        self.stdout.write("\n".join(app_template_dirs))