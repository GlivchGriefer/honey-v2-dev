# IMPORTS
from bot import ch


# HELLO
def hello_function(message, args):
    try:
        return 'Hello {}, Argument One: {}'.format(message.author, args[0])
    except Exception as e:
        return e


ch.add_command({
    # IF MESSAGE STARTS WITH TRIGGER
    'trigger': '-hello',

    # CALL MAIN FUNCTION
    'function': hello_function,

    # NUMBER OF ARGUMENTS NEEDED
    'args_num': 1,

    # NAME OF THE ARGUMENT
    'args_name': ['string'],

    # DESCRIBE WHAT FUNCTION DOES
    'description': 'Will respond hello to the caller and show arg 1'
})