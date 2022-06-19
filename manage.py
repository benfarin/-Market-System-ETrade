#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread

from Backend.Service.DTO import SimpleDiscountDTO
from Backend.Service.Initializer import Initializer
from ModelsBackend.models import Initialized

sys.path.append('....')
from Backend.Service.DTO.GuestDTO import GuestDTO
from Backend.Service.DTO.MemberDTO import MemberDTO
from Backend.Service.DTO.ProductDTO import ProductDTO
from Backend.Service.DTO.StoreDTO import StoreDTO
from django.db.models.signals import post_migrate
from django.conf import settings

is_initialized = False
def web_run():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    initialize_system()


def initialize_system():
    f = open(settings.INIT_FILE, 'r')
    lines = f.readlines()
    for line in lines:
        exec(line)

def main():
    web_run()


if __name__ == '__main__':
    main()
