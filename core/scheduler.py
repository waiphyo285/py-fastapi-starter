from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Callable, Any, Dict
from core.logger import logger

scheduler = AsyncIOScheduler()

def start_scheduler(
    config: Dict[str, Any],
    cron_config: Dict[str, Any] = None,
    job: Callable[..., Any] = None,
):
    """
    :param config: Custom config to pass to the job function.
    :param cron_config: Dict of cron params (minute, hour, etc.)
    :param job: The job function to run.
    """

    # Fallback values  --- default every 5 mins
    cron_config = cron_config or {"minute": "*/5"}  

    def default_job(task_name: str):
        logger.info(f"Running default job: {task_name}")

    scheduler.add_job(
        job or default_job,
        trigger=CronTrigger(**cron_config),
        kwargs={"task_name": config.get("task_name", "Untitled")},
        id="dynamic_cron_job",
        replace_existing=True
    )

    logger.info("Scheduler started with cron config: %s", cron_config)
