from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import settings


scheduler = AsyncIOScheduler()


def setup_sync_jobs():
    if not settings.ENABLE_SCHEDULER:
        return
    pass 