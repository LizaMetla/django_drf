from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Только parent комментарии - фильтр"""

    def to_representation(self, data):
        data = data.filter(parent=None)  # data является querySet . Выводятся только родительские комментарии
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Ввод рекурсивно children"""

    def to_representation(self, value):  # получаем 1 значение из базы данных - ищем детей на отзыве
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data  # возвращаем отзывы в древовидном образе


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(ReviewCreateSerializer, self).to_representation(instance)

        return ret


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавлеине рейтинга к отзыву"""

    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorSerializer(read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
