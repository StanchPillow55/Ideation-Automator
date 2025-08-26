import os; from celery import Celery
redis=os.getenv("REDIS_URL","redis://redis:6379/0"); celery=Celery("multimedia_sourcer",broker=redis,backend=redis); celery.conf.result_expires=3600
