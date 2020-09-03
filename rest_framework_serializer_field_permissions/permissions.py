"""
Permissions to use with the rest_framework_serializer_field_permissions.field classes:

    class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

        family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
        given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
        nick_name = fields.CharField(permission_classes=(AllowAny(), ))
"""


class BaseFieldPermission(object):
    """
    The permission from which all other field-permissions inherit.

    Create your own field-permissions by extending this object and overriding
    has_permission.
    """

    # pylint: disable=no-self-use
    def has_permission(self, request):
        """
        Return true if permission is granted, return false if permission is
        denied.
        """
        return True

    # pylint: disable=no-self-use
    def has_object_permission(self, request, obj):
        """
        Return true if permission is granted, return false if permission is
        denied.
        """
        return True


class AllowAny(BaseFieldPermission):
    """
    Permission which allows free-access to the given field.
    """

    def has_permission(self, request):
        return True


class AllowNone(BaseFieldPermission):
    """
    Permission which allows no access to the given field.
    """

    def has_permission(self, request):
        return False

    def has_object_permission(self, request, obj):
        return False


class IsAuthenticated(BaseFieldPermission):
    """
    Permission which only allows authenticated users access to the field.
    """

    def has_permission(self, request):
        return request.user and request.user.is_authenticated
