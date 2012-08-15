from django.core.management.base import BaseCommand, CommandError
from kucb.community.models import Event
import feedparser
import datetime
class Command(BaseCommand):
	args = ''
	help = 'Removes old events from system'
	def handle(self, *args, **options):
		currdate = datetime.date.today()
		events = Event.objects.filter(start_date__lt = currdate)
		for event in events:
			if not event.end_date or event.end_date < currdate:
				event.delete()
