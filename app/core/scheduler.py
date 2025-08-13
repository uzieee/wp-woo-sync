"""
Background scheduler for sync operations.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import settings


# Global scheduler instance
scheduler = AsyncIOScheduler()


def setup_sync_jobs():
    """Setup background sync jobs."""
    if not settings.ENABLE_SCHEDULER:
        return
    
    # Add sync jobs here when needed
    # Example: scheduler.add_job(sync_products, CronTrigger.from_crontab(settings.SYNC_CRON))
    pass 