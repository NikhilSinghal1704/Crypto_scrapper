from django.db import models
import uuid

class ScrapingJob(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CoinData(models.Model):
    job = models.ForeignKey(ScrapingJob, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=100)
    output = models.JSONField()
