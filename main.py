from invoke import run
import time
from numpy import array, average
import shutil
import os


class SockJsBenchmarking():

    def __init__(self):
        '''This method sets up the '_data/' directory
         for use.  it clears all existing files and
         then recreates the new directory.'''

        self.library = ''
        self.verbose = False

        self.s_avg = 0
        self.m_avg = 0
        self.t_avg = 0
        self.total = 0

        self.tornado_sum = []
        self.cyclone_sum = []
        self.twisted_sum = []

        self.iteration_number = 5

        print '========================================='
        print 'Welcome to SockJS benchmarking!'
        print '=========================================\n'

        #self.get_user_input()
        self.library = 'tornado'
        self.iterate()

    def get_user_input(self):
        '''This method gets the user's input as to which
        library they want to test.'''

        print 'There are 3 libraries to test:'
        print '- tornado'
        print '- cyclone'
        print '- twisted\n'
        print 'Which would you like to test?'

        #self.library = raw_input()

        #TODO(kmjungersen) - Provide a way to easily turn on/off verbose
        #TODO                output from each library being tested

        if self.library == 'tornado' or \
           self.library == 'cyclone' or \
           self.library == 'twisted':

            self.directory_setup()

        else:

            self.get_user_input()

    def directory_setup(self):

        #TODO - comments

        shutil.rmtree('data/')
        os.mkdir('data/')

        with open('.gitignore', 'r') as infile,\
             open('data/.gitignore', 'w+') as outfile:

            f = infile.read()
            outfile.write(f)

        self.setup_start_file = open('data/setup_start_time.txt', 'a+')
        self.teardown_stop_file = open('data/teardown_stop_time.txt', 'a+')

        self.iterate()

    def iterate(self):
        '''This 'for' loop will iterate over a number
        of setup/messaging/teardown operations. the
        user can customize this to run however many
        times they want.'''

        for x in range(0, self.iteration_number):

            #marks the start time and then writes to file
            setup_start_time = time.time()
            self.setup_start_file.write(str(setup_start_time) + '\n')

            run('python benchmark_' + self.library + '.py')

            teardown_stop_time = time.time()
            self.teardown_stop_file.write(str(teardown_stop_time) + '\n')

        self.analyze_data()

    def analyze_data(self):
        setup_stop_file = open('data/setup_stop_time.txt', 'r')
        message_start_file = open('data/message_start_time.txt', 'r')
        message_stop_file = open('data/message_stop_time.txt', 'r')
        teardown_start_file = open('data/teardown_start_time.txt', 'r')

        s_start = []
        s_stop = []
        m_start = []
        m_stop = []
        t_start = []
        t_stop = []

        self.setup_start_file.seek(0)
        self.teardown_stop_file.seek(0)

        for y in range(0, self.iteration_number):
            s_start.append(float(self.setup_start_file.readline()))
            s_stop.append(float(setup_stop_file.readline()))

            m_start.append(float(message_start_file.readline()))
            m_stop.append(float(message_stop_file.readline()))

            t_start.append(float(teardown_start_file.readline()))

            t_stop.append(float(self.teardown_stop_file.readline()))

        s_start_2 = array(s_start)
        s_stop_2 = array(s_stop)
        m_start = array(m_start)
        m_stop = array(m_stop)
        t_start = array(t_start)
        t_stop = array(t_stop)

        s_diff = s_stop_2 - s_start_2
        m_diff =(m_stop - m_start)
        t_diff =(t_stop - t_start)

        self.s_avg = average(s_diff)
        self.m_avg = average(m_diff)
        self.t_avg = average(t_diff)
        self.total = self.s_avg + self.m_avg + self.t_avg

        self.setup_start_file.close()
        setup_stop_file.close()
        message_start_file.close()
        message_stop_file.close()
        teardown_start_file.close()
        self.teardown_stop_file.close()

        if self.library == 'tornado':

            self.tornado_sum.append(self.s_avg)
            self.tornado_sum.append(self.m_avg)
            self.tornado_sum.append(self.t_avg)
            self.tornado_sum.append(self.total)

            self.library = 'cyclone'
            self.iterate()

        elif self.library == 'cyclone':

            self.cyclone_sum.append(self.s_avg)
            self.cyclone_sum.append(self.m_avg)
            self.cyclone_sum.append(self.t_avg)
            self.cyclone_sum.append(self.total)

            self.library = 'twisted'
            self.iterate()

        else:

            self.twisted_sum.append(self.s_avg)
            self.twisted_sum.append(self.m_avg)
            self.twisted_sum.append(self.t_avg)
            self.twisted_sum.append(self.total)

            self.report()

    def report(self):

        print '========================================================='
        print 'SockJS Benchmark Report - ' + self.library.upper()
        print '=========================================================\n'
        # print 'After ' + str(self.iteration_number) + ' iterations of the '
        # print self.library + ' library, the following metrics were obtained:\n'

        print '_________________________________________________________'
        print '            |                  Time (s)                  '
        print '   Phase    |--------------------------------------------'
        print '            |    Tornado   |   Cyclone    |   Twisted    '
        print '------------|--------------|--------------|--------------'
        print ' Startup    |    {:.4f}    |   {:.4f}     |   {:.4f}     '.\
            format(self.tornado_sum[0],
                   self.cyclone_sum[0],
                   self.twisted_sum[0])
        print ' Messaging  |    {:.4f}    |   {:.4f}     |   {:.4f}     '.\
            format(self.tornado_sum[1],
                   self.cyclone_sum[1],
                   self.twisted_sum[1])
        print ' Teardown   |    {:.4f}    |   {:.4f}     |   {:.4f}     '.\
            format(self.tornado_sum[2],
                   self.cyclone_sum[2],
                   self.twisted_sum[2])
        print '------------|--------------|--------------|--------------'
        print ' Total      |    {:.4f}    |   {:.4f}     |   {:.4f}     '.\
            format(self.tornado_sum[3],
                   self.cyclone_sum[3],
                   self.twisted_sum[3])

        print '\n'


if __name__ == '__main__':
    SockJsBenchmarking()