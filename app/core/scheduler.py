from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.jobs.sample_job import sample_cron_task

scheduler = AsyncIOScheduler()

def setup_cron_jobs():
    scheduler.add_job(
        func=sample_cron_task,
        trigger=CronTrigger(hour=0, minute=0),  # Once daily at midnight
        id="sample_task",
        name="Run sample task every midnight",
        replace_existing=True
    )
