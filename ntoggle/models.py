import datetime

from django.db import models

import zulip


class ZulipUser(models.Model):
  zulip_id = models.PositiveBigIntegerField(unique=True)
  timezone = TimeZoneField(default="UTC")

  created = models.DateTimeField(auto_now_add=True, db_index=True)

  def __str__(self):
    return str(zulip_id)


class NotificationToggle(models.Model):
  class ToggleTypes(models.TextChoices):
    ON = 'ON'
    OFF = 'OFF'

  zuser = models.ForeignKey(ZulipUser, on_delete=models.CASCADE)

  toggle_ts = models.DateTimeField(db_index=True)
  toggle_type = models.CharField(max_length=3, choices=ToggleTypes.choices)

  last_executed = models.DateTimeField(blank=True, null=True)

  created = models.DateTimeField(auto_now_add=True, db_index=True)
  modified = models.DateTimeField(auto_now=True, db_index=True)

  class Meta:
    ordering =('toggle_ts',)

  def __str__(self):
    return '{} {}'.format(self.zuser.zulip_id, self.event_type)

  def reschedule(self):
    new_event = self.toggle_ts + datetime.timedelta(days=7)
    new_event = new_event.replace(hour=self.toggle_type.hour)
    self.toggle_ts = new_event
