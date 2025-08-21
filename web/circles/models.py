from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Activity(TimeStampedModel):
    DAYS = [
        (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"),
        (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
    ]
    title = models.CharField(max_length=120)
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_day_of_week_display()})"

class Event(TimeStampedModel):
    name = models.CharField(max_length=160)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    category = models.CharField(max_length=60, blank=True)   # academic/sports/etc
    location = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Post(TimeStampedModel):
    title = models.CharField(max_length=160)
    body = models.TextField()

    def __str__(self):
        return self.title

class EmergencyContact(TimeStampedModel):
    name = models.CharField(max_length=120)
    department = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40)

    def __str__(self):
        return self.name
