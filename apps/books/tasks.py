from time import sleep

from celery.task import task


@task(name='my_first_task')
def my_first_task(duration):

    return 'first_task_done'
