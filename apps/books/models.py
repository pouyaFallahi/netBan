import uuid
from django.db import models
from apps.user.models import User
from django.core.exceptions import ValidationError


def validate_score(value):
    if value < 0 or value > 5:
        raise ValidationError('Score must be between 0 and 5.')


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pk} - {self.title} - {self.author}"


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    score = models.IntegerField(default=0, validators=[validate_score])

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.pk} - {self.book} - {self.user}"
