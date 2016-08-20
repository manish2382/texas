from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField

# Create your models here.


class Files(models.Model):
    data = JSONField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Texas_files'
