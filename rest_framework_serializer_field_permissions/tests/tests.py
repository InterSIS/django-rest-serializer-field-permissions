from argparse import Namespace

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from rest_framework import serializers

from rest_framework_serializer_field_permissions.permissions import AllowAny, AllowNone, IsAuthenticated, BaseFieldPermission
from rest_framework_serializer_field_permissions.fields import BooleanField, SerializerPermissionMixin, CharField
from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
from rest_framework_serializer_field_permissions.middleware import RequestMiddleware
from test_app.models import Album, Track


class PermissionTests(TestCase):
    def test_allow_any(self):
        permission = AllowAny()

        self.assertTrue(permission.has_permission({}))
        self.assertTrue(permission.has_object_permission({}, None))

    def test_allow_none(self):
        permission = AllowNone()

        self.assertFalse(permission.has_permission({}))
        self.assertFalse(permission.has_object_permission({}, None))

    def test_is_authenticated(self):
        permission = IsAuthenticated()

        authenticated_user = Namespace(is_authenticated=True)
        authenticated_request = Namespace(user=authenticated_user)
        self.assertTrue(permission.has_permission(authenticated_request))

        unauthenticated_user = Namespace(is_authenticated=False)
        unauthenticated_request = Namespace(user=unauthenticated_user)
        self.assertFalse(permission.has_permission(unauthenticated_request))


class FieldTests(TestCase):
    def test_permission_field_assignment(self):
        field = BooleanField()
        self.assertTrue(hasattr(field, "permission_classes"))
        self.assertEqual(len(field.permission_classes), 0)

        field = BooleanField(permission_classes=(AllowAny(), AllowNone()))
        self.assertTrue(hasattr(field, "permission_classes"))
        self.assertEqual(len(field.permission_classes), 2)

    def test_single_permission_checking(self):
        field = BooleanField(permission_classes=(AllowAny(),))
        self.assertTrue(field.check_permission({}, None))

        field = BooleanField(permission_classes=(AllowNone(),))
        self.assertFalse(field.check_permission({}, None))

        field = BooleanField(permission_classes=(IsAuthenticated(),))
        authenticated_user = Namespace(is_authenticated=True)
        authenticated_request = Namespace(user=authenticated_user)
        self.assertTrue(field.check_permission(authenticated_request, None))

        unauthenticated_user = Namespace(is_authenticated=False)
        unauthenticated_request = Namespace(user=unauthenticated_user)
        self.assertFalse(field.check_permission(unauthenticated_request, None))

    def test_multiple_permission_checking(self):
        """
        Field check_permission should only return true if all of its permissions return true
        """

        field = BooleanField(permission_classes=(AllowAny(), AllowNone()))
        self.assertFalse(field.check_permission({}, None))

        field = BooleanField(permission_classes=(AllowNone(), AllowAny()))
        self.assertFalse(field.check_permission({}, None))

        field = BooleanField(permission_classes=(AllowNone(), AllowNone()))
        self.assertFalse(field.check_permission({}, None))

        field = BooleanField(permission_classes=(AllowAny(), AllowAny()))
        self.assertTrue(field.check_permission({}, None))


class TrackSerializer(SerializerPermissionMixin, serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title')


class SerializerFieldTests(TestCase):
    def setUp(self):
        self.album = Album.objects.create(album_name='Album Name',
                                          artist='Album Artist')

        Track.objects.create(album=self.album,
                             order=1,
                             title='Public Service Announcement',
                             duration=245)

        RequestMiddleware.request = {}  # Provide the request middleware with a dummy request object

    def get_album_serializer(self, _tracks):
        class AlbumSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
            tracks = _tracks

            class Meta:
                model = Album
                fields = ('album_name', 'artist', 'tracks')

        return AlbumSerializer

    def test_many_false_serializer_field(self):
        field = TrackSerializer(permission_classes=(AllowNone(),))
        self.assertFalse(field.check_permission({}, None))

    def test_many_true_serializer_field(self):
        field = TrackSerializer(permission_classes=(AllowNone(),), many=True)

        self.assertFalse(field.check_permission({}, None))

    def test_many_false_serializer_field_removed(self):
        tracks = TrackSerializer(permission_classes=(AllowNone(),))

        album_serializer = self.get_album_serializer(tracks)(instance=self.album, context={'request': {}})

        self.assertFalse('tracks' in album_serializer.data)

    def test_many_true_serializer_field_removed(self):
        tracks = TrackSerializer(permission_classes=(AllowNone(),), many=True)

        album_serializer = self.get_album_serializer(tracks)(instance=self.album, context={'request': {}})

        self.assertFalse('tracks' in album_serializer.data)


class ObjectPermissionTests(TestCase):
    class IsArtist(BaseFieldPermission):
        def has_object_permission(self, request, obj):
            return request.user.username == obj.artist

    def setUp(self):
        self.user = User.objects.create_user(username='Album Artist', email='jacob@jacob.com', password='top_secret')
        self.album = Album.objects.create(album_name='Album Name',
                                          diary='I hated recording every second of this',
                                          artist=self.user.username)

        self.request = RequestFactory().get(f'/album/{self.album.album_name}')
        self.request.user = self.user
        RequestMiddleware.request = self.request  # Provide the request middleware with a dummy request object

    def get_album_serializer(self, _diary):
        class AlbumSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
            diary = _diary

            class Meta:
                model = Album
                fields = ('album_name', 'artist', 'diary')

        return AlbumSerializer

    def test_only_artist_can_see_album_diary(self):
        diary = CharField(permission_classes=(self.IsArtist(),))

        album_serializer = self.get_album_serializer(diary)(instance=self.album, context={'request': self.request})
        self.assertTrue('diary' in album_serializer.data)

        self.request.user = AnonymousUser()
        album_serializer = self.get_album_serializer(diary)(instance=self.album, context={'request': self.request})
        self.assertFalse('diary' in album_serializer.data)

        album_2 = Album.objects.create(album_name='Other Album Name',
                                       diary='I have a crush on "Album Artist"',
                                       artist='Other Album Artist')

        self.request.user = self.user
        album_serializer = self.get_album_serializer(diary)(many=True, instance=[self.album, album_2], context={'request': self.request})
        self.assertTrue('diary' in album_serializer.data[0])
        self.assertFalse('diary' in album_serializer.data[1])
