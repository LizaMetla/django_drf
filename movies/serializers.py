from rest_framework import serializers

from .models import Movie, Review


class RecursiveSerializer(serializers.Serializer):
    """Ввод рекурсивно children"""

    def to_representation(self, value):  # получаем 1 значение из базы данных - ищем детей на отзыве
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
