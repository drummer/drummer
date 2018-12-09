#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from drummer.utils.classloader import ClassLoader
from os import getpid as os_getpid
from os import path

class Runner(Process):
    """ This worker executes commands and tasks """

    def __init__(self, executing_task):

        # worker init
        super().__init__()

        # queue worker -> master
        self.queue_w2m = Queue(1)
        # queue master -> worker
        #self.queue_m2w = Queue(1)

        self.executing_task = executing_task


    def get_queues(self):
        #return self.queue_w2m, self.queue_m2w
        return self.queue_w2m


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue_w2m.put(pid)

        # begin working
        self.work()


    def work(self):

        # get shared queues
        queue_w2m = self.queue_w2m

        # get the task to exec
        executing_task = self.executing_task

        # load class to exec
        classname = executing_task.classname
        filename = executing_task.filename

        timeout = executing_task.timeout
        params = executing_task.params

        # load task class
        TaskToExec = ClassLoader().load(filename, classname)

        # init task and run
        task_to_exec = TaskToExec()
        task_result = task_to_exec.run(params)

        executing_task.result = task_result

        # queue_done
        queue_w2m.put(executing_task)

        return
