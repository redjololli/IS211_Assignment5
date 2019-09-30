#!/usr/bin/env python
# coding: utf-8

# In[ ]:


""" Week 5 Assignment ­ Data Structures"""

import argparse
import csv
import urllib2
import sys


def downloadData(url):
    datafile = urllib2.urlopen(url)
    return datafile


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_server_request()


class Request:
    def __init__(self, time, server_request):
        self.timestamp = int(time)
        self.server_request = int(server_request)

    def get_stamp(self):
        return self.timestamp

    def get_server_request(self):
        return self.server_request

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(csv_file):
    server = Server()
    server_queue = Queue()
    waiting_times = []

    response = urllib2.urlopen(csv_file)
    html = csv.reader(response)

    for row in html:
        request = Request(row[0], row[2])
        server_queue.enqueue(request)

        if (not server.busy()) and (not server_queue.is_empty()):
            new_request = server_queue.dequeue()
            waiting_times.append(new_request.wait_time(int(row[0])))
            server.start_next(new_request)

        server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print "Average Wait %6.2f secs %3d tasks remaining." % (average_wait, server_queue.size())


def simulateManyServers(csv_file, number):
    server = Server()
    server_queue = Queue()
    waiting_times = []
    server_list = []

    response = urllib2.urlopen(csv_file)
    html = csv.reader(response)

    for num in range(int(number)):
        server_list.append(server)
    for item in server_list:
        for row in html:
            request = Request(row[0], row[2])
            server_list.append(server_queue.enqueue(request))

            if (not server.busy()) and (not server_queue.is_empty()):
                new_request = server_queue.dequeue()
                waiting_times.append(new_request.wait_time(int(row[0])))
                server.start_next(new_request)

            server.tick()

        average_wait = sum(waiting_times) / len(waiting_times)
        print "Average Wait %6.2f secs %3d tasks remaining." % (average_wait, server_queue.size())




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--servers", type=int, default=1)
    args = parser.parse_args()
    url = args.url
    servers = args.servers

    if servers == 1:
        simulateOneServer(url)
    else:
        simulateManyServers(url, servers)


if __name__ == '__main__':
    main()

