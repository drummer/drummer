#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.classloader import ClassLoader


class EventRunner:

    def work(self, request):

        self.running = True

        # load class to exec
        classname = request.classname
        classpath = request.classpath

        # run the task and get task result
        EventToExec = ClassLoader().load(classpath, classname)
        response = EventToExec().execute(request)

        return response
