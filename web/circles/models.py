from django.db import models
from django.db.models import Sum
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

class Membership(TimeStampedModel):
    MEMBER = "member"
    MOD = "mod"
    OWNER = "owner"
    ROLES = (
        (MEMBER, "Member"),
        (MOD, "Moderator"),
        (OWNER, "Owner"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="circle_memberships")
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=12, choices=ROLES, default=MEMBER)

    class Meta:
        unique_together = ("user", "circle")

    def __str__(self):
        return f"{self.user} in {self.circle} as {self.role}"


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


class Post(TimeStampedModel):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    link_url = models.URLField(blank=True)
    score = models.IntegerField(default=0)  # optional legacy field; display uses score_total

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("circles:post_detail", kwargs={"slug": self.circle.slug, "pk": self.pk})

    @property
    def score_total(self) -> int:
        """Sum of all votes (+1/-1). Falls back to 0 if no votes."""
        return self.votes.aggregate(total=Sum("value"))["total"] or 0


class Comment(TimeStampedModel):
    # Use string FK to avoid NameError if Post isn't loaded yet
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Vote(TimeStampedModel):
    UPVOTE = 1
    DOWNVOTE = -1
    VALUES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    # String FK avoids load-order issues with Post
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=VALUES)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} voted {self.get_value_display()} on {self.post}"
    
class Event(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    circle = models.ForeignKey(
        Circle, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='events'
    )
    # Remove created_by temporarily
    # created_by = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE, 
    #     related_name='created_events'
    # )

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("circles:event_detail", kwargs={"pk": self.pk})