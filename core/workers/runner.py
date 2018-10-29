#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from utils.classloader import ClassLoader
from os import getpid as os_getpid
#import signal

class Runner(Process):
    """ This worker executes commands and tasks"""

    def __init__(self, task_executing):

        # worker init
        super().__init__()

        # queue worker -> master
        self.queue_w2m = Queue(1)
        # queue master -> worker
        #self.queue_m2w = Queue(1)
        self.task_executing = task_executing


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
        task_executing = self.task_executing
        task = task_executing.task

        # load class to exec
        classpath = 'tasks'
        classname = task.classname

        timeout = task.timeout
        params = task.params

        # run the task and get task result
        TaskToExec = ClassLoader().load(classpath, classname)
        task_result = TaskToExec().run(params)

        task_executing.terminated = True
        task_executing.result = task_result

        # queue_done
        queue_w2m.put(task_executing)

        return


    def handler(signum, frame):
        """ timeout handler """
        raise Exception("task ended in timeout")