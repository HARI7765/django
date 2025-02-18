from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import cleanup_expired_tokens
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean up expired verification tokens'

    def handle(self, *args, **options):
        try:
            cleanup_expired_tokens()
            self.stdout.write(self.style.SUCCESS('Successfully cleaned up expired tokens'))
        except Exception as e:
            logger.error(f'Error during token cleanup: {str(e)}')
            self.stdout.write(self.style.ERROR('Error cleaning up tokens'))
