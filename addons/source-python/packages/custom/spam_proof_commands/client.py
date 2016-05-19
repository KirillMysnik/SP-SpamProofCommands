from time import time

from commands.client import client_command_manager

from spam_proof_commands import anti_spam_message, BaseSpamProofCommand


class ClientCommand(BaseSpamProofCommand):
    _manager_class = client_command_manager

    def __call__(self, callback):
        def new_callback(command, index):
            current_time = time()
            client_time = self.client_timestamps.get(index, 0)

            if current_time - client_time < self.timeout:
                anti_spam_message.send(index)
            else:
                callback(command, index)

            self.client_timestamps[index] = current_time

        self.callback = new_callback

        self._manager_class.register_commands(
            self.names, new_callback, *self.args, **self.kwargs)

        # Return original callback
        return callback
