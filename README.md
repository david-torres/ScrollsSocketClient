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
	
	email = 'user@example.com'
	password = 'password'
	
	
    def run(message):
        """ This function is executed upon receiving the 'SignIn' event """

        # unsubscribe from the SignIn event
        scrolls.unsubscribe('SignIn')

        # subscribe to the LibraryView event with function library_view()
        scrolls.subscribe('LibraryView', library_view)
        scrolls.send({'msg': 'LibraryView'})

        # subscribe to the DeckCards event with function deck()
        scrolls.subscribe('DeckCards', deck)
        scrolls.send({'msg': 'DeckCards', 'deck': 'Growth Preconstructed'})


    def library_view(message):
        """ This function is executed upon receiving the 'LibraryView' event """

        # unsubscribe from the LibraryView event
        scrolls.unsubscribe('LibraryView')
        print message


    def deck(message):
        """ This function is executed upon receiving the 'DeckCards' event """

        # unsubscribe from the DeckCards event
        scrolls.unsubscribe('DeckCards')
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
