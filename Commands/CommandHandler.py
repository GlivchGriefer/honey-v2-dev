# COMMAND HANDLER CLASS
from bot import ch


class CommandHandler:

    # ON CREATION, RECORD CLIENT VARIABLE
    def __init__(self, client):
        self.client = client

        # CREATE ARRAY TO STORE COMMANDS
        self.commands = []

    def add_command(self, command):

        # ADD A COMMAND TO THE COMMANDS ARRAY
        self.commands.append(command)

    def command_handler(self, message):

        # LOOP THROUGH COMMAND ARRAY
        for command in self.commands:

            # IF MESSAGE STARTS WITH TRIGGER
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        # RETURN RESULTS OF THE FUNCTION
                        return self.client.send_message(message.channel,
                                                        str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            # RETURN RESULTS OF THE FUNCTION
                            return self.client.send_message(message.channel,
                                                            str(command['function'](message, self.client, args)))
                            break
                        else:
                            # RETURN ARGUMENT ERROR
                            return self.client.send_message(message.channel,
                                                            'command "{}" requires {} argument(s) "{}"'.format(
                                                                command['trigger'], command['args_num'],
                                                                ', '.join(command['args_name'])))
                            break
                else:
                    break


# MAIN FUNCTION
def hello_function(message, client, args):
    try:
        return 'Hello {}, Argument One: {}'.format(message.author, args[0])
    except Exception as e:
        return e


# COMMAND DICTIONARY
ch.add_command({
    # IF MESSAGE STARTS WITH TRIGGER
    'trigger': '!hello',

    # CALL MAIN FUNCTION
    'function': hello_function,

    # NUMBER OF ARGUMENTS NEEDED
    'args_num': 1,

    # NAME OF THE ARGUMENT
    'args_name': ['string'],

    # DESCRIBE WHAT FUNCTION DOES
    'description': 'Will respond hello to the caller and show arg 1'
})