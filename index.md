[![Build Status](https://travis-ci.org/InterSIS/django-rest-serializer-field-permissions.svg?branch=master)](https://travis-ci.org/InterSIS/django-rest-serializer-field-permissions)
[![Code Climate](https://codeclimate.com/github/InterSIS/django-rest-serializer-field-permissions/badges/gpa.svg)](https://codeclimate.com/github/InterSIS/django-rest-serializer-field-permissions)
[![Coverage Status](https://coveralls.io/repos/InterSIS/django-rest-serializer-field-permissions/badge.svg?branch=master&service=github)](https://coveralls.io/github/InterSIS/django-rest-serializer-field-permissions?branch=master)
[![PyPI version](https://badge.fury.io/py/django-rest-serializer-field-permissions.svg)](http://badge.fury.io/py/django-rest-serializer-field-permissions)

django-rest-serializer-field-permissions
=============

Add field-by-field permission classes to your serializer fields that look like this:

```
  class PersonSerializer(FieldPermissionSerializerMixin, LookupModelSerializer):

      // Only allow authenticated users to retrieve family and given names
      family_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))
      given_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))
      
      // Allow all users to retrieve nick name
      nick_name = serializers.CharField(permission_classes=(AllowAll(), ))

```

Define your own permission classes as a function of any request variable.

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
  

  class MyViewset(viewsets.GenericViewSet):
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

* Django Rest Framework 3.0
* Django 1.6, 1.7, 1.8
* Python 2.7, 3.3, 3.4

See tox.ini for specific minor versions tested.

Additional Requirements
=======================

None

Todo
====

* Serializer tests
* Integration tests

Getting Involved
================

Feel free to open pull requests or issues. GitHub is the canonical location of this project.
