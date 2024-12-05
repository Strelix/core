from django.conf import settings

from core.service.maintenance.expire.run import expire_models_task

CORE_MAINTENANCE_TASKS: list[callable] = [
    expire_models_task
]


def get_maintenance_tasks() -> list[callable]:
    return getattr(settings, "MAINTENANCE_FUNCTIONS", CORE_MAINTENANCE_TASKS)


def execute_maintenance_tasks(tasks: list[callable]) -> str:
    output = ""
    for i, task in enumerate(tasks):
        output += f"\n{task()}" if i != 0 else task()
    return output
