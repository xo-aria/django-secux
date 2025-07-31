from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.session_key}"


class PageRequestLog(models.Model):
    path = models.CharField(max_length=255)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('path', 'date')

    def __str__(self):
        return f"{self.path} - {self.date} - {self.count}"


class OptimizedImageFile(ImageFieldFile):
    def save(self, name, content, save=True):
        try:
            quality = getattr(self.field, 'quality', 70)
            file_name = getattr(self.field, 'custom_name', name)
            image = Image.open(content)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)
            content = ContentFile(buffer.read(), name=file_name)
        except Exception:
            pass
        super().save(name, content, save)


class OptimizeImageField(models.ImageField):
    attr_class = OptimizedImageFile

    def __init__(self, *args, quality=70, name=None, **kwargs):
        self.quality = quality
        self.custom_name = name
        super().__init__(*args, **kwargs)
