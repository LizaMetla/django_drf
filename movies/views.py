from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer


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
        if review.is_valid():
            review.save()
        return Response(status=201)
