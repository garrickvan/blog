#!/usr/bin/env python
# This file is for django build-in web server and use for dev.
# It make the settings_dev as the running config to avoid the cof
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings_dev")

    os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings_dev'

    os.environ['IN_DJANGO_DEV_MODE'] = 'True'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)