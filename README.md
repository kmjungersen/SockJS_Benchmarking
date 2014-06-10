SockJS Benchmarking
===================

This is a tool to test 3 separate SockJS libraries:
- Tornado
- Cyclone
- Twisted

This tool will test one library at a time. Each will set up a SockJS connection, iterate over a certain number of messages echoed back and forth between a server and a client, and then tear down.  You can choose the number of messages to be sent back and forth, as well as the number of times this process is repeated.  

The resulting metrics will tell you:
- Average setup time
- Average messaging time
- Average teardown time

There will soon be options for a verbose output, which will enable you to see each data point outputed, as well as the averages at the end. 