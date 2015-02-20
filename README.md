[![Downloads](https://pypip.in/download/django-rest-serializer-field-permissions/badge.svg)](https://pypi.python.org/pypi/django-rest-serializer-field-permissions/)
django-rest-serializer-field-permissions
=============

Add permission classes to your serializer fields that look like this:

```
  class PersonSerializer(FieldPermissionSerializerMixin, LookupModelSerializer):

      family_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))
      given_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))

```

This package is **unstable**. It is in **alpha**. It basically works for me. I am actively working towards a beta release.

Installation
===============

Install the module in your Python distribution or virtualenv:

    $ pip install django-rest-serializer-field-permissions

Add the application to your `INSTALLED_APPS`:

```
  INSTALLED_APPS = (
  ...
  "rest_framework_serializer_field_permissions",
  ...
  )
```

Use
===

In your serializers, mix `FieldPermissionSerializerMixin` into your serializer classes, as the left-most parent. The fields
provided by `rest_framework_serializer_field_permissions.fields` accept `permission_classes` which operate in typical
DRF fashion:
```
  from rest_framework import serializers
  
  from rest_framework_serializer_field_permissions import fields
  from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
  from rest_framework_serializer_field_permissions.permissions import IsAuthenticated

  class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

      family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
      given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))

```

Any pagination-capable viewset with which you wish to include permission-capable fields must use the
`ContextPassingPaginationSerializer` provided by `rest_framework_serializer_field_permissions.serializers`.
```
  from rest_framework import viewsets
  
  from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
  
  from rest_
  class InterSISEncryptedLookupGenericViewset(viewsets.GenericViewSet):
      pagination_serializer_class = ContextPassingPaginationSerializer
```

The `FieldPermissionSerializerMixin` may be mixed with any DRF serializer class, not just `ModelSerializer`. Similarly,
the `ContextPassingPaginationSerializer` may be used with any pagination-capable viewset, not just `GenericViewSet`.

You can write your own permission classes by sub-classing `BaseFieldPermission` in `permissions.py`.

How it Works
============

The `FieldPermissionSerializerMixin` provides its own `fields` property, which DRF serializers call to get a list
of their own fields. The amended `fields` property checks for permission-bearing fields, forces them to check their
permissions against the request, and scrubs from the return any fields which fail their permission checks.

Compatibility
=============

* Django Rest Framework 3
* Django 1.6, 1.7
* Python 2.7, 3.4

Additional Requirements
=======================

None

Todo
====

* Tests

Getting Involved
================

Feel free to open pull requests or issues. GitHub is the canonical location of this project.
