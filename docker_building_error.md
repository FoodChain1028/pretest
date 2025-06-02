# Docker Building Error

## Problem

I was trying to build the docker container with the original Dockerfile config, yet the result shown that psycopg2 is not compatible with `python3.13`.

## Solution

The version of python is modified from `python:3` into `python:3.12-slim`, where the former one installs the latest version (`python3.13`) of `psycopg2` and the former one works fine.

I understand that changing anything in the `dockerfile` is not a good choice, yet due to the time pressure of this project, this is done to make it work.

## Appendix

error log when building:

```bash
2025-06-02 18:11:28 web-1  | Traceback (most recent call last):
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 25, in <module>
2025-06-02 18:11:28 web-1  |     import psycopg as Database
2025-06-02 18:11:28 web-1  | ModuleNotFoundError: No module named 'psycopg'
2025-06-02 18:11:28 web-1  | 
2025-06-02 18:11:28 web-1  | During handling of the above exception, another exception occurred:
2025-06-02 18:11:28 web-1  | 
2025-06-02 18:11:28 web-1  | Traceback (most recent call last):
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 27, in <module>
2025-06-02 18:11:28 web-1  |     import psycopg2 as Database
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/psycopg2/__init__.py", line 51, in <module>
2025-06-02 18:11:28 web-1  |     from psycopg2._psycopg import (                     # noqa
2025-06-02 18:11:28 web-1  |     ...<10 lines>...
2025-06-02 18:11:28 web-1  |     )
2025-06-02 18:11:28 web-1  | ImportError: /usr/local/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-aarch64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
2025-06-02 18:11:28 web-1  | 
2025-06-02 18:11:28 web-1  | During handling of the above exception, another exception occurred:
2025-06-02 18:11:28 web-1  | 
2025-06-02 18:11:28 web-1  | Traceback (most recent call last):
2025-06-02 18:11:28 web-1  |   File "/code/manage.py", line 21, in <module>
2025-06-02 18:11:28 web-1  |     main()
2025-06-02 18:11:28 web-1  |     ~~~~^^
2025-06-02 18:11:28 web-1  |   File "/code/manage.py", line 17, in main
2025-06-02 18:11:28 web-1  |     execute_from_command_line(sys.argv)
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2025-06-02 18:11:28 web-1  |     utility.execute()
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~~~^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/core/management/__init__.py", line 416, in execute
2025-06-02 18:11:28 web-1  |     django.setup()
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/__init__.py", line 24, in setup
2025-06-02 18:11:28 web-1  |     apps.populate(settings.INSTALLED_APPS)
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/apps/registry.py", line 116, in populate
2025-06-02 18:11:28 web-1  |     app_config.import_models()
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/apps/config.py", line 269, in import_models
2025-06-02 18:11:28 web-1  |     self.models_module = import_module(models_module_name)
2025-06-02 18:11:28 web-1  |                          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-06-02 18:11:28 web-1  |     return _bootstrap._gcd_import(name[level:], package, level)
2025-06-02 18:11:28 web-1  |            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-06-02 18:11:28 web-1  |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/contrib/auth/models.py", line 3, in <module>
2025-06-02 18:11:28 web-1  |     from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/contrib/auth/base_user.py", line 57, in <module>
2025-06-02 18:11:28 web-1  |     class AbstractBaseUser(models.Model):
2025-06-02 18:11:28 web-1  |     ...<109 lines>...
2025-06-02 18:11:28 web-1  |             )
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/base.py", line 143, in __new__
2025-06-02 18:11:28 web-1  |     new_class.add_to_class("_meta", Options(meta, app_label))
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/base.py", line 371, in add_to_class
2025-06-02 18:11:28 web-1  |     value.contribute_to_class(cls, name)
2025-06-02 18:11:28 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/options.py", line 243, in contribute_to_class
2025-06-02 18:11:28 web-1  |     self.db_table, connection.ops.max_name_length()
2025-06-02 18:11:28 web-1  |                    ^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/connection.py", line 15, in __getattr__
2025-06-02 18:11:28 web-1  |     return getattr(self._connections[self._alias], item)
2025-06-02 18:11:28 web-1  |                    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/connection.py", line 62, in __getitem__
2025-06-02 18:11:28 web-1  |     conn = self.create_connection(alias)
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/utils.py", line 193, in create_connection
2025-06-02 18:11:28 web-1  |     backend = load_backend(db["ENGINE"])
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/utils.py", line 113, in load_backend
2025-06-02 18:11:28 web-1  |     return import_module("%s.base" % backend_name)
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-06-02 18:11:28 web-1  |     return _bootstrap._gcd_import(name[level:], package, level)
2025-06-02 18:11:28 web-1  |            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:28 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 29, in <module>
2025-06-02 18:11:28 web-1  |     raise ImproperlyConfigured("Error loading psycopg2 or psycopg module")
2025-06-02 18:11:28 web-1  | django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module
2025-06-02 18:11:29 web-1  | Watching for file changes with StatReloader
2025-06-02 18:11:29 web-1  | Exception in thread django-main-thread:
2025-06-02 18:11:29 web-1  | Traceback (most recent call last):
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 25, in <module>
2025-06-02 18:11:29 web-1  |     import psycopg as Database
2025-06-02 18:11:29 web-1  | ModuleNotFoundError: No module named 'psycopg'
2025-06-02 18:11:29 web-1  | 
2025-06-02 18:11:29 web-1  | During handling of the above exception, another exception occurred:
2025-06-02 18:11:29 web-1  | 
2025-06-02 18:11:29 web-1  | Traceback (most recent call last):
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 27, in <module>
2025-06-02 18:11:29 web-1  |     import psycopg2 as Database
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/psycopg2/__init__.py", line 51, in <module>
2025-06-02 18:11:29 web-1  |     from psycopg2._psycopg import (                     # noqa
2025-06-02 18:11:29 web-1  |     ...<10 lines>...
2025-06-02 18:11:29 web-1  |     )
2025-06-02 18:11:29 web-1  | ImportError: /usr/local/lib/python3.13/site-packages/psycopg2/_psycopg.cpython-313-aarch64-linux-gnu.so: undefined symbol: _PyInterpreterState_Get
2025-06-02 18:11:29 web-1  | 
2025-06-02 18:11:29 web-1  | During handling of the above exception, another exception occurred:
2025-06-02 18:11:29 web-1  | 
2025-06-02 18:11:29 web-1  | Traceback (most recent call last):
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/threading.py", line 1041, in _bootstrap_inner
2025-06-02 18:11:29 web-1  |     self.run()
2025-06-02 18:11:29 web-1  |     ~~~~~~~~^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/threading.py", line 992, in run
2025-06-02 18:11:29 web-1  |     self._target(*self._args, **self._kwargs)
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/autoreload.py", line 64, in wrapper
2025-06-02 18:11:29 web-1  |     fn(*args, **kwargs)
2025-06-02 18:11:29 web-1  |     ~~^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/core/management/commands/runserver.py", line 125, in inner_run
2025-06-02 18:11:29 web-1  |     autoreload.raise_last_exception()
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/autoreload.py", line 87, in raise_last_exception
2025-06-02 18:11:29 web-1  |     raise _exception[1]
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/core/management/__init__.py", line 394, in execute
2025-06-02 18:11:29 web-1  |     autoreload.check_errors(django.setup)()
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/autoreload.py", line 64, in wrapper
2025-06-02 18:11:29 web-1  |     fn(*args, **kwargs)
2025-06-02 18:11:29 web-1  |     ~~^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/__init__.py", line 24, in setup
2025-06-02 18:11:29 web-1  |     apps.populate(settings.INSTALLED_APPS)
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/apps/registry.py", line 116, in populate
2025-06-02 18:11:29 web-1  |     app_config.import_models()
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/apps/config.py", line 269, in import_models
2025-06-02 18:11:29 web-1  |     self.models_module = import_module(models_module_name)
2025-06-02 18:11:29 web-1  |                          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-06-02 18:11:29 web-1  |     return _bootstrap._gcd_import(name[level:], package, level)
2025-06-02 18:11:29 web-1  |            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-06-02 18:11:29 web-1  |   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/contrib/auth/models.py", line 3, in <module>
2025-06-02 18:11:29 web-1  |     from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/contrib/auth/base_user.py", line 57, in <module>
2025-06-02 18:11:29 web-1  |     class AbstractBaseUser(models.Model):
2025-06-02 18:11:29 web-1  |     ...<109 lines>...
2025-06-02 18:11:29 web-1  |             )
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/base.py", line 143, in __new__
2025-06-02 18:11:29 web-1  |     new_class.add_to_class("_meta", Options(meta, app_label))
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/base.py", line 371, in add_to_class
2025-06-02 18:11:29 web-1  |     value.contribute_to_class(cls, name)
2025-06-02 18:11:29 web-1  |     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/models/options.py", line 243, in contribute_to_class
2025-06-02 18:11:29 web-1  |     self.db_table, connection.ops.max_name_length()
2025-06-02 18:11:29 web-1  |                    ^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/connection.py", line 15, in __getattr__
2025-06-02 18:11:29 web-1  |     return getattr(self._connections[self._alias], item)
2025-06-02 18:11:29 web-1  |                    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/utils/connection.py", line 62, in __getitem__
2025-06-02 18:11:29 web-1  |     conn = self.create_connection(alias)
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/utils.py", line 193, in create_connection
2025-06-02 18:11:29 web-1  |     backend = load_backend(db["ENGINE"])
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/utils.py", line 113, in load_backend
2025-06-02 18:11:29 web-1  |     return import_module("%s.base" % backend_name)
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-06-02 18:11:29 web-1  |     return _bootstrap._gcd_import(name[level:], package, level)
2025-06-02 18:11:29 web-1  |            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-06-02 18:11:29 web-1  |   File "/usr/local/lib/python3.13/site-packages/django/db/backends/postgresql/base.py", line 29, in <module>
2025-06-02 18:11:29 web-1  |     raise ImproperlyConfigured("Error loading psycopg2 or psycopg module")
2025-06-02 18:11:29 web-1  | django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module
```