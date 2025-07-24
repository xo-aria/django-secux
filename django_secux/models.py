from django.db import models

class PageRequestLog(models.Model):
    path = models.CharField(max_length=255)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('path', 'date')

    def __str__(self):
        return f"{self.path} - {self.date} - {self.count}"
