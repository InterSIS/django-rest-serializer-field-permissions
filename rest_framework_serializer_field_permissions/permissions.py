

class BaseFieldPermission(object):

    def has_permission(self, request):
        return True


class AllowAny(BaseFieldPermission):

    def has_permission(self, request):
        return True


class AllowNone(BaseFieldPermission):

    def has_permission(self, request):
        return False


class IsAuthenticated(BaseFieldPermission):

    def has_permission(self, request):
        return request.user and request.user.is_authenticated()