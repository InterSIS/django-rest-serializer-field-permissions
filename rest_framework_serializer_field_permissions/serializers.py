class FieldPermissionSerializerMixin(object):
    @property
    def fields(self):
        ret = super(FieldPermissionSerializerMixin, self).fields
        request = self._context["request"]

        for field_name, field in ret.items():
            if hasattr(field, 'check_permission') and (not field.check_permission(request)):
                ret.pop(field_name)

        return ret


"""
Django REST Framework 3.1+ killed PaginationSerializer and DefaultObjectSerializer
"""


# class ContextPassingPaginationSerializer(PaginationSerializer):
#     def __init__(self, *args, **kwargs):
#         """
#         Override init to add in the object serializer field on-the-fly.
#         """
#         super(ContextPassingPaginationSerializer, self).__init__(*args, **kwargs)
#         results_field = self.results_field
#
#         try:
#             object_serializer = self.Meta.object_serializer_class
#         except AttributeError:
#             object_serializer = DefaultObjectSerializer
#
#         self.fields[results_field] = ListSerializer(
#             child=object_serializer(context=kwargs["context"]),
#             source='object_list'
#         )
