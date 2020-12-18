import time
import csv
import os
import gc
import re
import copy
import datetime


class Entry:

    def __init__(self, timestamp, uptime, loads, memory_total, memory_free, memory_used, buff):
        self.timestamp = timestamp
        self.uptime = uptime
        self.loads = loads
        self.memory_total = memory_total
        self.memory_free = memory_free
        self.memory_used = memory_used
        self.buff = buff
        self.processes = []

    def append_process(self, process):
        self.processes.append(process)

    def toString(self):
        txt = self.timestamp + " " + self.uptime + " " + self.loads[0] + " " + self.loads[1] + " " + self.loads[
            2] + " " + self.memory_total + " " + self.memory_free + " " + self.memory_used + " " + self.buff
        for p in self.processes:
            txt = txt + " " + p.toString()
        return txt

    def header(self):
        tup = "timestamp", "uptime", "load1", "load5", "load15",\
               "memory_total", "memory_free", "memory_used", "buff"
        for p in self.processes:
            tup = tup + p.header()
        return tup

    def toRow(self):
        tup = self.timestamp, self.uptime, self.loads[0], self.loads[1], self.loads[2], self.memory_total,\
              self.memory_free, self.memory_used, self.buff
        for p in self.processes:
            tup = tup + p.toRow()
        return tup


class Process:

    def __init__(self, pid, user, cpu, ram, cputime, command):
        self.pid = pid
        self.user = user
        self.cpu = cpu
        self.ram = ram
        self.cputime = cputime
        self.command = command

    def toString(self):
        return str(
            self.pid) + " " + self.user + " " + self.cpu + " " + self.ram + " " + self.cputime + " " + self.command

    def header(self):
        return self.command + "-" + "PID", \
            self.command + "-" + "CPU%",\
            self.command + "-" + "MEM%", \
            self.command + "-" + "CPUTIME"

    def toRow(self):
        return str(self.pid), self.cpu, self.ram, self.cputime


def process_command(command):
    if "java-11-openjdk-amd64/bin/java" in command:
        if "taesa-controller-gui/build/classes/java/main" in command:
            return "GUI (app)"
        elif "taesa-controller-gui/gradle" in command:
            return "GUI (java,GradleWrapperMain)"
        elif "root/.gradle/wrapper" in command:
            return "GUI (java,gradle)"
        elif "karaf." in command:
            return "ONOS (karaf,java)"
        else:
            return command
    elif "/bin/sh" in command and "bin/karaf" in command:
        return "ONOS (karaf,shell)"
    elif "sudo java -jar target/accesscontrol" in command:
        return "AC (sudo,app)"
    elif "java -jar target/accesscontrol" in command:
        return "AC (app)"
    elif "sudo ./onos-service" in command:
        return "ONOS (onos-service,shell)"
    else:
        return command


def processData(file):
    entries = []
    with open(str(file)+".log") as csvfile:
        print "Reading log..."
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', skipinitialspace=True)
        timestamp = None
        uptime = None
        loads = []
        processes_size = 0
        day = 0
        previous_entry_hour = 0
        current_entry = None
        for row in spamreader:
            if row[0] == "top":  # Header 1, GET Timestamp, uptime, loads
                if current_entry is not None:
                    current_entry.processes.sort(key=lambda x: x.pid, reverse=True)
                    if processes_size > 0 and processes_size != len(current_entry.processes):
                        print "WARNING: Discrepancy in the number of processes!"
                    processes_size = len(current_entry.processes)
                    entries.append(current_entry)
                    # print current_entry.toRow(), "\n"
                    current_entry = None
                if previous_entry_hour == 23 and int(row[2][:2]) == 0:
                    print "Day " + str(day) + " processed."
                    day = day + 1
                timestamp = str(day).zfill(2) + ":" + row[2]
                previous_entry_hour = int(row[2][:2])
                if "day" in row[5]:
                    if "min" in row[7]:
                        uptime = str(row[4]) + "-0:" + str(row[6]).zfill(2)
                        loads = [row[12][:-1].replace(',','.'), row[13][:-1].replace(',','.'), row[14].replace(',','.')]
                    else:
                        uptime = str(row[4]) + "-" + str(row[6][:-1])
                        loads = [row[11][:-1].replace(',','.'), row[12][:-1].replace(',','.'), row[13].replace(',','.')]
                else:
                    uptime = "0-" + str(row[4][:-1])
                    loads = [row[9][:-1].replace(',','.'), row[10][:-1].replace(',','.'), row[11].replace(',','.')]
                # print timestamp, uptime, loads
            elif row[0] == "KiB":  # Header 2, GET Memory total, free, used, buff/cache
                current_entry = Entry(timestamp, uptime, loads, row[3], row[5], row[7], row[9])
                # print row[3], row[5], row[7], row[9]
            else:  # Process, GET PID, USER, CPU%, RAM%, CPUTIME, COMMAND
                if not ("grep" in " ".join(row) or "unattended-upgrade" in " ".join(row)):  # Ignore GREPs
                    p = Process(int(row[0]), row[1], row[8].replace(',','.'), row[9].replace(',','.'), row[10], process_command(" ".join(row[11:])))
                    current_entry.append_process(p)
                    # print row[0], row[1], row[8], row[9], row[10], process_command(" ".join(row[11:]))
                # pass
            # line = " ".join(row)
            # print line
        if processes_size > 0 and processes_size != len(current_entry.processes):
            print "WARNING: Discrepancy in the number of processes!"
        current_entry.processes.sort(key=lambda x: x.pid, reverse=True)
        entries.append(current_entry)

    with open("processed-"+str(file)+".csv", 'w') as myfile:
        print "Writing to file..."
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE, delimiter=';')
        wr.writerow(entries[0].header())
        for entry in entries:
            wr.writerow(entry.toRow())

file_name = "teste2"
processData(file_name)

# Year, Month, Day, Hour, Minute, AP, Number os Stations
# time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
