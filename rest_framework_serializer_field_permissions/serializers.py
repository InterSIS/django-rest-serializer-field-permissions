"""
Drop in serializer mixins.
"""

from rest_framework_serializer_field_permissions.middleware import RequestMiddleware


class FieldPermissionSerializerMixin(object):
    """
    Mixin to your serializer class as follows:

        class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

            family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
            given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
    """

    def __init__(self, *args, **kwargs):
        super(FieldPermissionSerializerMixin, self).__init__(*args, **kwargs)
        self.current_instance = None

    def to_representation(self, instance):
        self.current_instance = instance
        return super(FieldPermissionSerializerMixin, self).to_representation(instance)

    @property
    def fields(self):
        """
        Supercedes drf's serializers.ModelSerializer's fields property
        :return: a set of permission-scrubbed fields
        """
        ret = super(FieldPermissionSerializerMixin, self).fields
        request = RequestMiddleware.request
        instance = self.current_instance

        if request is None:
            raise RuntimeError(
                "Request object not available. Did you forget to add the rest_framework_serializer_field_permissions "
                "middleware? See https://github.com/InterSIS/django-rest-serializer-field-permissions ")

        forbidden_field_names = [
            field_name for field_name, field in ret.items() if hasattr(field, 'check_permission') and (not field.check_permission(request, instance))
        ]

        for field_name in forbidden_field_names:
            ret.pop(field_name)

        return ret
