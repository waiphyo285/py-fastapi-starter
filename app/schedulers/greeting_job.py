from core.logger import logger
from core.scheduler import start_scheduler

def say_greeting_job():
    config = {"task_name": "Sawadee Krub!"}

    # Every day at 02:00 AM
    cron_config = {
        "minute": "0",
        "hour": "2" 
    }

    def job(task_name: str):
        logger.info(f"Running scheduled job: {task_name}")

    start_scheduler(config=config, cron_config=cron_config, job=job)