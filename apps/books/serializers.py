from .models import Book, Rating
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.user.serializers import UserSerializer


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['book', 'score', 'user']
        read_only_fields = ('user',)

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError(_('Score must be between 0 and 5.'))
        return value


class BookSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'ratings']


class BookFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
