from time import time

from commands.say import say_command_manager

from spam_proof_commands.command import anti_spam_message, BaseSpamProofCommand


class SayCommand(BaseSpamProofCommand):
    _manager_class = say_command_manager

    def __call__(self, callback):
        def new_callback(command, index, team_only):
            current_time = time()
            client_time = self.client_timestamps.get(index, 0)

            if current_time - client_time < self.timeout:
                anti_spam_message.send(index)
            else:
                callback(command, index, team_only)

            self.client_timestamps[index] = current_time

        self.callback = new_callback

        self._manager_class.register_commands(
            self.names, new_callback, *self.args, **self.kwargs)

        # Return original callback
        return callback
