from invoke import run
import time
from numpy import array, average
import shutil
import os
IterationNumber = 10


shutil.rmtree('Data/')
os.mkdir('Data/')

SetupStartFile = open('Data/SetupStartTime.txt', 'a+')
TeardownStopFile = open('Data/TeardownStopTime.txt', 'a+')

#===================================================
for x in range(0, IterationNumber):

    SetupStartTime = time.time()
    SetupStartFile.write(str(SetupStartTime) + '\n')
    run('python Benchmark_Cyclone.py')

    TeardownStopTime = time.time()
    TeardownStopFile.write(str(TeardownStopTime) + '\n')

#===================================================

SetupStopFile = open('Data/SetupStopTime.txt', 'r')
MessageStartFile = open('Data/MessageStartTime.txt', 'r')
MessageStopFile = open('Data/MessageStopTime.txt', 'r')
TeardownStartFile = open('Data/TeardownStartTime.txt', 'r')

s_start = []
s_stop = []
m_start = []
m_stop = []
t_start = []
t_stop = []

SetupStartFile.seek(0)
TeardownStopFile.seek(0)

for y in range(0, IterationNumber):
    s_start.append(float(SetupStartFile.readline()))
    s_stop.append(float(SetupStopFile.readline()))

    m_start.append(float(MessageStartFile.readline()))
    m_stop.append(float(MessageStopFile.readline()))

    t_start.append(float(TeardownStartFile.readline()))

    t_stop.append(float(TeardownStopFile.readline()))

s_start_2 = array(s_start)
s_stop_2 = array(s_stop)
m_start = array(m_start)
m_stop = array(m_stop)
t_start = array(t_start)
t_stop = array(t_stop)

s_diff = s_stop_2 - s_start_2
m_diff = (m_stop - m_start)
t_diff = (t_stop - t_start)

s_avg = average(s_diff)
m_avg = average(m_diff)
t_avg = average(t_diff)


print s_avg
print m_avg
print t_avg