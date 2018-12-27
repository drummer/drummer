
SCRIPT_CODE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DRUMMER LAUNCHING SCRIPT
# THIS FILE IS AUTOMATICALLY GENERATED
# DO NOT EDIT IT UNLESS YOU KNOW WHAT YOU ARE DOING

from drummer.utils import Configuration
from drummer import Drummer
from sys import argv as sys_argv
from os import path

if __name__ == "__main__":

    BASE_DIR = path.join(path.dirname(path.abspath(__file__)))

    config = Configuration.load(BASE_DIR)

    drummer = Drummer(config)
    drummer.process(sys_argv)
"""


SERVICE_CODE = """[Unit]
Description=drummer - daemon for scheduling tasks
After=multi-user.target

[Service]
Type=idle
ExecStart=<pythonpath> <command>

[Install]
WantedBy=multi-user.target
"""
