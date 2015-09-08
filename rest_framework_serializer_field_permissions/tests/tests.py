from argparse import Namespace

from django.test import TestCase

from rest_framework import serializers

from rest_framework_serializer_field_permissions.permissions import AllowAny, AllowNone, IsAuthenticated
from rest_framework_serializer_field_permissions.fields import BooleanField, SerializerPermissionMixin
from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
from test_app.models import Album, Track


class PermissionTests(TestCase):
    def test_allow_any(self):
        permission = AllowAny()

        self.assertTrue(permission.has_permission({}))

    def test_allow_none(self):
        permission = AllowNone()

        self.assertFalse(permission.has_permission({}))

    def test_is_authenticated(self):
        permission = IsAuthenticated()

        authenticated_user = Namespace(is_authenticated=lambda: True)
        authenticated_request = Namespace(user=authenticated_user)
        self.assertTrue(permission.has_permission(authenticated_request))

        unauthenticated_user = Namespace(is_authenticated=lambda: False)
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
        self.assertTrue(field.check_permission({}))

        field = BooleanField(permission_classes=(AllowNone(),))
        self.assertFalse(field.check_permission({}))

        field = BooleanField(permission_classes=(IsAuthenticated(),))
        authenticated_user = Namespace(is_authenticated=lambda: True)
        authenticated_request = Namespace(user=authenticated_user)
        self.assertTrue(field.check_permission(authenticated_request))

        unauthenticated_user = Namespace(is_authenticated=lambda: False)
        unauthenticated_request = Namespace(user=unauthenticated_user)
        self.assertFalse(field.check_permission(unauthenticated_request))

    def test_multiple_permission_checking(self):
        """
        Field check_permission should only return true if all of its permissions return true
        """

        field = BooleanField(permission_classes=(AllowAny(), AllowNone()))
        self.assertFalse(field.check_permission({}))

        field = BooleanField(permission_classes=(AllowNone(), AllowAny()))
        self.assertFalse(field.check_permission({}))

        field = BooleanField(permission_classes=(AllowNone(), AllowNone()))
        self.assertFalse(field.check_permission({}))

        field = BooleanField(permission_classes=(AllowAny(), AllowAny()))
        self.assertTrue(field.check_permission({}))


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

    def get_album_serializer(self, _tracks):
        class AlbumSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):
            tracks = _tracks

            class Meta:
                model = Album
                fields = ('album_name', 'artist', 'tracks')

        return AlbumSerializer

    def test_many_false_serializer_field(self):
        field = TrackSerializer(permission_classes=(AllowNone(),))
        self.assertFalse(field.check_permission({}))

    def test_many_true_serializer_field(self):
        field = TrackSerializer(permission_classes=(AllowNone(),), many=True)

        self.assertFalse(field.check_permission({}))

    def test_many_false_serializer_field_removed(self):
        tracks = TrackSerializer(permission_classes=(AllowNone(),))

        album_serializer = self.get_album_serializer(tracks)(instance=self.album, context={'request': {}})

        self.assertFalse('tracks' in album_serializer.data)

    def test_many_true_serializer_field_removed(self):
        tracks = TrackSerializer(permission_classes=(AllowNone(),), many=True)

        album_serializer = self.get_album_serializer(tracks)(instance=self.album, context={'request': {}})

        self.assertFalse('tracks' in album_serializer.data)
