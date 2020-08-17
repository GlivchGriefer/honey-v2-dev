# COMMAND HANDLER CLASS
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
