from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Circle(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, help_text="Auto-filled from name; can edit.")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True, help_text="If false, only members can view.")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_circles")
    members = models.ManyToManyField(User, related_name="circles", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("circles:circle_detail", kwargs={"slug": self.slug})