from django.db import models
from django.utils.text import slugify


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    native_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(
        upload_to="languages/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name