# HELLO COMMAND
def hello_function(message, client, args):
    try:
        return 'Hello {}, Argument One: {}'.format(message.author, args[0])
    except Exception as e:
        return e
