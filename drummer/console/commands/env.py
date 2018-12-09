#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.database import Base, Schedule
from drummer.utils.files import YamlFile
import drummer.local.data as appdata
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine
from os import path, makedirs
import inquirer

class EnvInit():

    def execute(self, args):

        print('Setting the environment for Drummer...')

        ROOT_DIR = path.abspath(args['root_dir'])

        # task folder
        TASK_DIR = 'tasks'
        TASK_DIR_PATH = path.join(ROOT_DIR, TASK_DIR)

        # config folder
        CONFIG_DIR = 'config'
        CONFIG_DIR_PATH = path.join(ROOT_DIR, CONFIG_DIR)
        CONFIG_FILE = 'drummer-config.yml'
        TASK_FILE = 'drummer-tasks.yml'

        # database folder and filepath
        DATABASE_DIR = 'database'
        DATABASE_DIR_PATH = path.join(ROOT_DIR, DATABASE_DIR)

        database_file = args.get('database')
        database_filepath = path.join(DATABASE_DIR_PATH, database_file)

        SCRIPT_FILE = 'drummer-cli.py'
        SERVICE_FILE = 'drummered.service'

        # FOLDER CREATION
        # ----------------------------------------------- #

        # create root folder
        if not path.exists(ROOT_DIR):
            makedirs(ROOT_DIR)

        # create task folder
        if not path.exists(TASK_DIR_PATH):
            makedirs(TASK_DIR_PATH)

        # create config folder
        if not path.exists(CONFIG_DIR_PATH):
            makedirs(CONFIG_DIR_PATH)

        # create database folder
        if not path.exists(DATABASE_DIR_PATH):
            makedirs(DATABASE_DIR_PATH)


        # DATABASE CREATION
        # ----------------------------------------------- #

        # create database
        conn_string = 'sqlite+pysqlite:///{0}'.format(database_filepath)

        db_engine = create_engine(conn_string, module=sqlite)
        Base.metadata.create_all(db_engine, checkfirst=True)

        print('Database created.')

        # CONFIG CREATION
        # ----------------------------------------------- #

        config_data = {
            'application-name': 'Drummer',
            'socket': {
                'address': 'localhost',
                'port': 10200,
                'max_connections': 1,
                'message_len': 4096
            },
            'logging': {
                'filename': '/var/log/drummer.log',
                'type': 'file-rotation',
                'level': 'DEBUG'
            },
            'database': database_filepath,
            'taskdir': TASK_DIR_PATH,
            'max-runners': 4,
            'idle-time': 0.1
        }

        YamlFile.write(path.join(CONFIG_DIR_PATH, CONFIG_FILE), config_data)

        task_data = [
            {
                'classname': 'YourTaskClass',
                'filename': 'filename.py',
                'description': 'Description of task'
            }
        ]

        YamlFile.write(path.join(CONFIG_DIR_PATH, TASK_FILE), task_data)

        # task readme
        with open(path.join(TASK_DIR_PATH, 'README.txt'), 'w') as f:
            f.write('Insert your task files in this folder')

        print('Configuration files created.')


        # SCRIPT CREATION
        # ----------------------------------------------- #

        with open(path.join(ROOT_DIR, SCRIPT_FILE), 'w') as f:
            f.write(appdata.SCRIPT_CODE)

        print('Python script created.')


        # SERVICE CREATION
        # ----------------------------------------------- #

        question = [
            inquirer.Confirm(
                'service',
                message = 'Create service file?',
                default = True,
            )
        ]

        ans = inquirer.prompt(question)

        if ans['service']:

            question = [
                inquirer.Text(
                    'path',
                    message = 'Python executable to use',
                    default = '/usr/bin/env python3'
                )
            ]

            ans = inquirer.prompt(question)

            service_code = appdata.SERVICE_CODE

            service_code = service_code.replace('<pythonpath>', ans['path'])

            command = '{0} service:start'.format(path.join(ROOT_DIR, SCRIPT_FILE))
            service_code = service_code.replace('<command>', command)

            with open(path.join(CONFIG_DIR_PATH, SERVICE_FILE), 'w') as f:
                f.write(service_code)

            print('Service file created in {0}'.format(CONFIG_DIR_PATH))