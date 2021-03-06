About
=====

This project is a multi-threaded, event-based socket client for talking to the Scrolls socket server. I've never written anything multi-threaded or socket based before so critique is not only welcome, it is encouraged.


Prerequisites
===============

Install Requests

	pip install requests


Usage
======

    from ScrollsSocketClient import ScrollsSocketClient

    email = 'user@gexample.com'
    password = 'password'


    def connect(message):
        """ This function is executed upon receiving the 'FirstConnect' event """

        # unsubscribe from the FirstConnect event
        scrolls.unsubscribe('FirstConnect')

        # subscribe to the OverallStats event with function overall_stats()
        scrolls.subscribe('OverallStats', overall_stats)
        scrolls.send({'msg': 'OverallStats'})


    def overall_stats(message):
        """ This function is executed upon receiving the 'OverallStats' event """
        # print some server info
        print message

        # quit
        print 'Exiting...'
        scrolls.quit()

    # give the client our username/password
    scrolls = ScrollsSocketClient(email, password)

    # subscribe to the FirstConnect event with function connect()
    scrolls.subscribe('FirstConnect', connect)

    # login to the server
    scrolls.login()



Commands
=========

See [COMMANDS.md](COMMANDS.md)


In-depth Example
=================

For a full-featured example of how you can make a bot using this client, see [PriceBot](https://github.com/david-torres/PriceBot)


Known Issues
=============
This has never handled disconnects very well. If you know anything about sockets, please help me fix this.
