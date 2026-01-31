from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
import logging

scheduler = None

def start_scheduler():
    global scheduler
    if scheduler:
        return  # prevent duplicate start

    jobstores = {
        "default": SQLAlchemyJobStore(url="sqlite:///incident.db")
    }

    executors = {
        "default": ThreadPoolExecutor(5)
    }

    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        timezone="UTC"
    )

    scheduler.start()
    logging.info("APScheduler started")

def shutdown_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown(wait=False)
        logging.info("APScheduler stopped")
