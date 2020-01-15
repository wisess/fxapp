import time
import datetime
import re
import requests
from django.dispatch import receiver
from . import signals


@receiver(signals.load_weekly_zones)
def load_weekly_zones(sender, **kwargs):
	print('Ok!')