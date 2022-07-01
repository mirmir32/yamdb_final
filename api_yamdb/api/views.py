from uuid import uuid4

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Categories, Genre, Review, Title
from users.models import CustomUser

from .filters import TitleGenreFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsObjectOwnerModeratorAdminOrReadOnly)
from .serializers import (AccountSerializer, CategoriesSerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)
from .throttling import PostUserRateThrottle


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Функция-обработчик для запросов по модели Review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsObjectOwnerModeratorAdminOrReadOnly)
    throttle_classes = (PostUserRateThrottle,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.review_title.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        return title.review_title.all()

    def perform_update(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        return title.review_title.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Функция-обработчик для запросов по модели Comment.
    """
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsObjectOwnerModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        queryset = review.comment_review.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        review=review)
        return review.comment_review.all()

    def perform_update(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        review=review)
        return review.comment_review.all()


class TitleViewSet(viewsets.ModelViewSet):
    """
    Функция-обработчик для запросов по модели Title.
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleGenreFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitleCreateSerializer
        return TitleSerializer


class CategoriesViewSet(CreateDestroyListViewSet):
    """
    Функция-обработчик для запросов по модели Categories.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(CreateDestroyListViewSet):
    """
    Функция-обработчик для запросов по модели Genre.
    """
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class UserViewSet(viewsets.ModelViewSet):
    """
    Функция-обработчик для запросов по модели CustomUser.
    """
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        methods=('GET', 'PATCH',),
        detail=False,
        url_path='me',
        serializer_class=AccountSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(CustomUser, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']
    if confirmation_code != user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    confirmation_code = str(uuid4())
    user, created = CustomUser.objects.get_or_create(
        username=username,
        email=email,
        confirmation_code=confirmation_code
    )
    send_mail(
        subject='Код подтверждения доступа Yamdb',
        message=f'Код подтверждения доступа: {confirmation_code}',
        from_email='admin@yamdb.com',
        recipient_list=(email,))
    return Response(
        serializer.data,
        status=status.HTTP_200_OK)
