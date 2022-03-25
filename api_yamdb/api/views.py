from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User, UserRole

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly, IsAdminPermission,
                          IsAuthorStaffOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Родительский класс для определения сета миксинов для Category и Genre"""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['name']


class TokenObtain(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
                user, confirmation_code) is False:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        response = Response(status=status.HTTP_200_OK)
        response.data = {
            'token': str(refresh.access_token)
        }
        return response


class RegistrationAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            user = get_object_or_404(User, username=username)
            conf_code = user.confirmation_code
            email = user.email
            send_mail(
                'Регистрация на YAMDB(повторно)',
                f'Код для получения JWT-токена: {conf_code}',
                f'{DEFAULT_FROM_EMAIL}',
                [f'{email}']
            )
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response.data = {
                'message': 'Письмо повторно направлено на почту'
            }
            return response
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        try:
            User.objects.create(
                username=username,
                email=email
            )
        except IntegrityError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
            response.data = {'message': 'username и/или email уже заняты'}
            return response
        User.objects.get(
            username=username,
            email=email
        ).delete()
        serializer.save()
        user = get_object_or_404(User, username=username)
        conf_code = default_token_generator.make_token(user)
        User.objects.filter(
            username=username).update(confirmation_code=conf_code)
        email = user.email
        send_mail(
            'Регистрация на YAMDB',
            f'Код для получения JWT-токена: {conf_code}',
            f'{DEFAULT_FROM_EMAIL}',
            [f'{email}']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        if request.method != 'PATCH':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = request.data
        _mutable = data._mutable
        data._mutable = True
        if user.role == UserRole.USER:
            try:
                data.pop('role')
            except KeyError:
                pass
        data._mutable = _mutable
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorStaffOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorStaffOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(review=review)
