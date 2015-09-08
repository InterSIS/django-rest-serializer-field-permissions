import copy
import inspect
from rest_framework import fields
from rest_framework.serializers import LIST_SERIALIZER_KWARGS, ListSerializer


class PermissionMixin(object):
    def __init__(self, *args, **kwargs):
        permission_classes = kwargs.pop("permission_classes", ())

        super(PermissionMixin, self).__init__(*args, **kwargs)
        self.permission_classes = permission_classes

    def check_permission(self, request):
        return all((permission.has_permission(request) for permission in self.permission_classes))


class SerializerPermissionMixin(PermissionMixin):
    class PermissionListSerializer(ListSerializer):
        def __init__(self, *args, **kwargs):
            self.child = kwargs.pop('child', copy.deepcopy(self.child))

            self.permission_classes = self.child.permission_classes
            self.check_permission = self.child.check_permission

            self.allow_empty = kwargs.pop('allow_empty', True)

            assert self.child is not None, '`child` is a required argument.'
            assert not inspect.isclass(self.child), '`child` has not been instantiated.'

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


class BooleanField(PermissionMixin, fields.BooleanField):
    pass


class NullBooleanField(PermissionMixin, fields.NullBooleanField):
    pass


class CharField(PermissionMixin, fields.CharField):
    pass


class EmailField(PermissionMixin, fields.EmailField):
    pass


class RegexField(PermissionMixin, fields.RegexField):
    pass


class SlugField(PermissionMixin, fields.SlugField):
    pass


class URLField(PermissionMixin, fields.URLField):
    pass


class IntegerField(PermissionMixin, fields.IntegerField):
    pass


class FloatField(PermissionMixin, fields.FloatField):
    pass


class DecimalField(PermissionMixin, fields.DecimalField):
    pass


class DateField(PermissionMixin, fields.DateField):
    pass


class DateTimeField(PermissionMixin, fields.DateTimeField):
    pass


class TimeField(PermissionMixin, fields.TimeField):
    pass


class ChoiceField(PermissionMixin, fields.ChoiceField):
    pass


class MultipleChoiceField(PermissionMixin, fields.MultipleChoiceField):
    pass


class FileField(PermissionMixin, fields.FileField):
    pass


class ImageField(PermissionMixin, fields.ImageField):
    pass


class ListField(PermissionMixin, fields.ListField):
    pass


class ReadOnlyField(PermissionMixin, fields.ReadOnlyField):
    pass


class HiddenField(PermissionMixin, fields.HiddenField):
    pass


class ModelField(PermissionMixin, fields.ModelField):
    pass


class SerializerMethodField(PermissionMixin, fields.SerializerMethodField):
    pass
