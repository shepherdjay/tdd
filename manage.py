#!/usr/bin/env python
import os
import sys

import collections.abc
collections.Iterator = collections.abc.Iterator
collections.Mapping = collections.abc.Mapping
collections.Iterable = collections.abc.Iterable


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
