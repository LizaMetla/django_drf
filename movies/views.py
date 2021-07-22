from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import models
from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    ReviewCreateSerializer, CreateRatingSerializer,
    ActorSerializer, ActorDetailSerializer,
)
from .service import get_client_ip


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        # 1 способ
        # rating_user=models.Case(
        #    models.When(ratings__ip=get_client_ip(request), then=True),
        #    default=False,
        #    output_field=models.BooleanField()
        # ),

        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод списка фильмов"""

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk, draft=False)
        # movie = Movie.objects.filter(id=pk, draft=False).first()
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    serializer_class = ReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        review = ReviewCreateSerializer(data=request.data)
        review.is_valid(raise_exception=True)
        review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=get_client_ip(request))
        return Response(status=201)


class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
