from django.db import models
from jsonfield import JSONField

# Create your models here.
#
#
class OptResult(models.Model):
    job = models.CharField('job', max_length=200)
    n_iter = models.IntegerField('n_iter')
    optResult = JSONField()

    def save(self, *args, **kwargs):
        if OptResult.objects.count() >= 200:
            OptResult.objects[0].delete()

        super(OptResult, self).save(*args, **kwargs)
