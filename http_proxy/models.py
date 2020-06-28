import datetime

from django.db import models
from django.utils.timezone import utc


class ProxyStatus(models.Model):
    """
    The purpose of this class is to store the status of the proxy server.

    For the status page, this is done at the oject with ID 1.
    """
    request_count = models.IntegerField(default=0, blank=False, null=False)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "Proxy Status"

    def __str__(self):
        return f"Start Time: { self.start_time }, { self.request_count } requests received"

    def increment_number_of_requests(self):
        self.request_count = self.request_count + 1
        self.save(update_fields=['request_count'])

    def time_from_start(self):
        if self.start_time:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.start_time
            return timediff
