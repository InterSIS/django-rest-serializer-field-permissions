"""
Drop in replacements for DRF's fields. Use as follows:

    from rest_framework_serializer_field_permissions import fields

    class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

        family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
        given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
        nick_name = fields.CharField(permission_classes=(AllowAny(), ))
"""
import copy
import inspect

from rest_framework import fields
from rest_framework.serializers import LIST_SERIALIZER_KWARGS, ListSerializer


class PermissionMixin(object):
    """
    Mixin for DRF's field objects, to make them permission capable.
    """
    def __init__(self, *args, **kwargs):
        permission_classes = kwargs.pop("permission_classes", ())

        super(PermissionMixin, self).__init__(*args, **kwargs)
        self.permission_classes = permission_classes

    def check_permission(self, request, obj):
        """
        Check this field's permissions to determine whether or not it may be
        shown.
        """
        return all((permission.has_permission(request) and permission.has_object_permission(request, obj)
                    for permission in self.permission_classes))


# TODO: docstring
# pylint: disable=missing-docstring
class SerializerPermissionMixin(PermissionMixin):

    # TODO: diagnost/address abstract-method issue
    # pylint: disable=abstract-method
    class PermissionListSerializer(ListSerializer):

        def __init__(self, *args, **kwargs):
            self.child = kwargs.pop('child', copy.deepcopy(self.child))

            self.permission_classes = self.child.permission_classes
            self.check_permission = self.child.check_permission

            self.allow_empty = kwargs.pop('allow_empty', True)

            assert self.child is not None, '`child` is a required argument.'
            assert not inspect.isclass(self.child), '`child` has not been instantiated.'

            # TODO: diagnose/address bad-super-call issue
            # pylint: disable=bad-super-call
            super(ListSerializer, self).__init__(*args, **kwargs)

            self.child.bind(field_name='', parent=self)

    @classmethod
    def many_init(cls, *args, **kwargs):

        child_serializer = cls(*args, **kwargs)
        list_kwargs = {'child': child_serializer}
        list_kwargs.update(dict([
            (key, value) for key, value in kwargs.items()
            if key in LIST_SERIALIZER_KWARGS
        ]))
        return SerializerPermissionMixin.PermissionListSerializer(*args, **list_kwargs)


# pylint: disable=missing-docstring
class BooleanField(PermissionMixin, fields.BooleanField):
    pass


# pylint: disable=missing-docstring
class NullBooleanField(PermissionMixin, fields.NullBooleanField):
    pass


# pylint: disable=missing-docstring
class CharField(PermissionMixin, fields.CharField):
    pass


# pylint: disable=missing-docstring
class EmailField(PermissionMixin, fields.EmailField):
    pass


# pylint: disable=missing-docstring
class RegexField(PermissionMixin, fields.RegexField):
    pass


# pylint: disable=missing-docstring
class SlugField(PermissionMixin, fields.SlugField):
    pass


# pylint: disable=missing-docstring
class URLField(PermissionMixin, fields.URLField):
    pass


# pylint: disable=missing-docstring
class IntegerField(PermissionMixin, fields.IntegerField):
    pass


# pylint: disable=missing-docstring
class FloatField(PermissionMixin, fields.FloatField):
    pass


# pylint: disable=missing-docstring
class DecimalField(PermissionMixin, fields.DecimalField):
    pass


# pylint: disable=missing-docstring
class DateField(PermissionMixin, fields.DateField):
    pass


# pylint: disable=missing-docstring
class DateTimeField(PermissionMixin, fields.DateTimeField):
    pass


# pylint: disable=missing-docstring
class TimeField(PermissionMixin, fields.TimeField):
    pass


# pylint: disable=missing-docstring
class ChoiceField(PermissionMixin, fields.ChoiceField):
    pass


# pylint: disable=missing-docstring
class MultipleChoiceField(PermissionMixin, fields.MultipleChoiceField):
    pass


# pylint: disable=missing-docstring
class FileField(PermissionMixin, fields.FileField):
    pass


# pylint: disable=missing-docstring
class ImageField(PermissionMixin, fields.ImageField):
    pass


# pylint: disable=missing-docstring
class ListField(PermissionMixin, fields.ListField):
    pass


# pylint: disable=missing-docstring
# pylint: disable=abstract-method
class ReadOnlyField(PermissionMixin, fields.ReadOnlyField):
    pass


# pylint: disable=missing-docstring
# pylint: disable=abstract-method
class HiddenField(PermissionMixin, fields.HiddenField):
    pass


# pylint: disable=missing-docstring
class ModelField(PermissionMixin, fields.ModelField):
    pass


# pylint: disable=missing-docstring
# pylint: disable=abstract-method
class SerializerMethodField(PermissionMixin, fields.SerializerMethodField):
    pass
