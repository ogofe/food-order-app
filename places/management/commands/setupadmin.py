from django.core.management.base import BaseCommand
from ..setup import (
	create_permissions
	)

class Command(BaseCommand):
	help = "Setup the admin permissions and database"


	def add_arguments(self, parser):
		return

	def handle(self, *args):
		create_permissions()
		return
