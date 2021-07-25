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


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        # 1 способ
        # rating_user=models.Case(
        #    models.When(ratings__ip=get_client_ip(request), then=True),
        #    default=False,
        #    output_field=models.BooleanField()
        # ),
        return movies


class MovieDetailView(APIView):
    """Вывод списка фильмов"""

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk, draft=False)
        # movie = Movie.objects.filter(id=pk, draft=False).first()
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
