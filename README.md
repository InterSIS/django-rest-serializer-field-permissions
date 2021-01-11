[![Build Status](https://travis-ci.org/InterSIS/django-rest-serializer-field-permissions.svg?branch=master)](https://travis-ci.org/InterSIS/django-rest-serializer-field-permissions)
[![Code Climate](https://codeclimate.com/github/InterSIS/django-rest-serializer-field-permissions/badges/gpa.svg)](https://codeclimate.com/github/InterSIS/django-rest-serializer-field-permissions)
[![Coverage Status](https://coveralls.io/repos/InterSIS/django-rest-serializer-field-permissions/badge.svg?branch=master&service=github)](https://coveralls.io/github/InterSIS/django-rest-serializer-field-permissions?branch=master)
[![PyPI version](https://badge.fury.io/py/django-rest-serializer-field-permissions.svg)](http://badge.fury.io/py/django-rest-serializer-field-permissions)

django-rest-serializer-field-permissions
=============

Add field-by-field permission classes to your serializer fields that look like this:

```python
  class PersonSerializer(FieldPermissionSerializerMixin, LookupModelSerializer):

      # Only allow authenticated users to retrieve family and given names
      family_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))
      given_names = serializers.CharField(permission_classes=(IsAuthenticated(), ))
      
      # Allow all users to retrieve nick name
      nick_name = serializers.CharField(permission_classes=(AllowAll(), ))

```

Complete Tutorial
----------------

This example builds on the example Django REST Framework API in the [DRF 3.9 documentation](https://github.com/encode/django-rest-framework/tree/3.9.x#example). Please make sure that you have completed that tutorial before beginning this one.

Install this module into your environment:

```
  $ pip install django-rest-serializer-field-permissions~=3.0
```

Install this module into Django by adding it to your `INSTALLED_APPS`.
```python
  INSTALLED_APPS = (
  # ...
      'rest_framework_serializer_field_permissions',
  # ...
  )
```


Now you can add retrieve permissions to individual fields. You must import the modules and classes shown below, mix `FieldPermissionSerializerMixin` as the **leftmost** parent to your serializers, and then define your fields using the provided drop-in field classes.

For example, modify the root `urls.py` you created in the DRF tutorial with the following code:

```python
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from rest_framework_serializer_field_permissions import fields                                      # <--
from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin  # <--
from rest_framework_serializer_field_permissions.permissions import IsAuthenticated                 # <--

# Serializers define the API representation.
class UserSerializer(FieldPermissionSerializerMixin, serializers.HyperlinkedModelSerializer):       # <--
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

    email = fields.EmailField(permission_classes=(IsAuthenticated(), ))                             # <--

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

```

Now, only authenticated users will be able to retrieve your users' emails. You can confirm this by creating a superuser account, if you haven't already, and visiting [http://localhost:8000/users/](http://localhost:8000/users) as both an authenticated user and an unauthenticated visitor.

Alternately, you could have restricted retrieve access to the `username` field with the code:

```python
    username = fields.CharField(permission_classes=(IsAuthenticated(), ))
```

You can define your own permissions classes that operate on any aspect of the incoming `request`, and you can specify multiple r`permission_classes` on a field: all provided permissions must be satisfied for the visitor to retrieve the given field.

Use
---

### Installation

Install the module in your Python distribution or virtualenv:

    $ pip install django-rest-serializer-field-permissions

Add the application to your `INSTALLED_APPS`:

```python
  INSTALLED_APPS = (
  ...
  'rest_framework_serializer_field_permissions',
  ...
  )
```

### Adding Permissions

In your serializers, mix `FieldPermissionSerializerMixin` into your serializer classes, as the left-most parent. The fields
provided by `rest_framework_serializer_field_permissions.fields` accept `permission_classes` which operate in typical
DRF fashion:

```python
  from rest_framework import serializers
  
  from rest_framework_serializer_field_permissions import fields
  from rest_framework_serializer_field_permissions.serializers import FieldPermissionSerializerMixin
  from rest_framework_serializer_field_permissions.permissions import IsAuthenticated

  class UserSerializer(FieldPermissionSerializerMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

    email = fields.EmailField(permission_classes=(IsAuthenticated(), ))

```

The `FieldPermissionSerializerMixin` may be mixed with any DRF serializer class, not just `ModelSerializer`.

You can write your own permission classes by sub-classing `BaseFieldPermission` in `permissions.py`.

How it Works
------------

The `FieldPermissionSerializerMixin` provides its own `fields` property, which DRF serializers call to get a list
of their own fields. The amended `fields` property checks for permission-bearing fields, forces them to check their
permissions against the request, and scrubs from the return any fields which fail their permission checks.

Compatibility
-------------

This package is tested for compatibility against the following software versions:

* Django Rest Framework 3.11
* Django 2.2, 3.0
* Python 3.7

This package may incidentally be compatible with other similar versions of the above software. See tox.ini for specific minor versions tested.

Additional Requirements
-----------------------

None

Todo
----

* Integration tests

Getting Involved
----------------

Feel free to open pull requests or issues. [GitHub](https://github.com/InterSIS/django-rest-serializer-field-permissions) is the canonical location of this project.

Here's the general sequence of events for contribution:

1. Open an issue in the [issue tracker](https://github.com/InterSIS/django-rest-serializer-field-permissions/issues/).
2. In any order:
  * Submit a pull request with a **failing** test that demonstrates the issue/feature.
  * Get acknowledgement/concurrence.
3. Submit pull request that passes your test in (2). Include documentation, if appropriate.
