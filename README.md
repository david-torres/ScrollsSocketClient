About
=====

This project is a multi-threaded, event-based socket client for talking to the Scrolls socket server. I've never written anything multi-threaded or socket based before so critique is not only welcome, it is encouraged.


Prerequisites
===============

Install PyCrypto

	pip install pycrypto



Usage
======

    from ScrollsSocketClient import ScrollsSocketClient

    email = 'user@gexample.com'
    password = 'password'


    def run(message):
        """ This function is executed upon receiving the 'SignIn' event """

        # unsubscribe from the SignIn event
        scrolls.unsubscribe('SignIn')

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

    # subscribe to the SignIn event with function run()
    scrolls.subscribe('SignIn', run)

    # login to the server
    scrolls.login()



Commands
=========

See [COMMANDS.md](COMMANDS.md)
