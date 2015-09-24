"""
Drop in serializer mixins.
"""


class FieldPermissionSerializerMixin(object):
    """
    Mixin to your serializer class as follows:

        class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

            family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
            given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
    """

    @property
    def fields(self):
        """
        Supercedes drf's serializers.ModelSerializer's fields property
        :return: a set of permission-scrubbed fields
        """
        ret = super(FieldPermissionSerializerMixin, self).fields
        request = self._context["request"]

        for field_name, field in ret.items():
            if hasattr(field, 'check_permission') and (not field.check_permission(request)):
                ret.pop(field_name)

        return ret
