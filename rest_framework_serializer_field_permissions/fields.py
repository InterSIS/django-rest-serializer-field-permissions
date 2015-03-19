from rest_framework import fields


class PermissionMixin(object):

    def __init__(self, *args, **kwargs):

        super(PermissionMixin, self).__init__(*args, **kwargs)
        self.permission_classes = kwargs.get("permission_classes", ())

    def check_permission(self, request):
        return all((permission.has_permission(request) for permission in self.permission_classes))


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
















