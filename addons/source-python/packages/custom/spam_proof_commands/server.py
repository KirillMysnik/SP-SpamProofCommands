from time import time

from commands.server import server_command_manager
from core import echo_console
from entities.constants import WORLD_ENTITY_INDEX

from spam_proof_commands import ANTI_SPAM_TEXT, BaseSpamProofCommand


class ServerCommand(BaseSpamProofCommand):
    _manager_class = server_command_manager

    def __call__(self, callback):
        def new_callback(command):
            index = WORLD_ENTITY_INDEX

            current_time = time()
            client_time = self.client_timestamps.get(index, 0)

            if current_time - client_time < self.timeout:
                echo_console(ANTI_SPAM_TEXT)
            else:
                callback(command)

            self.client_timestamps[index] = current_time

        self.callback = new_callback

        self._manager_class.register_commands(
            self.names, new_callback, *self.args, **self.kwargs)

        # Return original callback
        return callback
