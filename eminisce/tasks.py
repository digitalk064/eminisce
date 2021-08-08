from background_task import background

from eminisce.models.loans import Loan
from eminisce.models.reservation import Reservation

from django.utils import timezone as timmy
from django.conf import settings

timmy.activate(settings.TIME_ZONE)


@background(schedule=0)
def auto_update_statuses(): #Auto update various statuses of models such as late for loans and reservations
    #print("Executing 'auto updating statuses' task")
    loans= Loan.objects.filter(status=Loan.Status.ACTIVE)
    for loan in loans:
        loan.update_late_status()
    reserves = Reservation.objects.filter(status=Reservation.Status.ACTIVE)
    for reserve in reserves:
        reserve.update_late_status()

@background(schedule=0)
def cleanup_completed_tasks_db():
    from background_task.models import CompletedTask
    print("Cleanup CompletedTask objects")
    CompletedTask.objects.all().delete()