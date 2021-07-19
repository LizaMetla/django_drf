from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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
    # ip адрес пользователя
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ip=self.get_client_ip(request))
        return Response(status=201)