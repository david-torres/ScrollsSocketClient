from ScrollsSocketClient import ScrollsSocketClient

email = 'user@example.com'
password = 'password'


def run(message):
    # unsubscribe from the SignIn event
    scrolls.unsubscribe('SignIn')

    # subscribe to the LibraryView event with function library_view()
    scrolls.subscribe('LibraryView', library_view)
    scrolls.send({'msg': 'LibraryView'})

    # subscribe to the DeckCards event with function deck()
    scrolls.subscribe('DeckCards', deck)
    scrolls.send({'msg': 'DeckCards', 'deck': 'Growth Preconstructed'})


def library_view(message):
    # unsubscribe from the LibraryView event
    scrolls.unsubscribe('LibraryView')
    print message


def deck(message):
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
