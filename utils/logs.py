"""Module to handle logging for moderator commands (kick,ban,clear) and reading logs (logs are stored in json file)"""
import json
import datetime
import os

class CommandLog:
    """Class to handle reading from and writing in json file."""

    # init is executed when the object is created
    def __init__(self, filename):
        """Init object.

        Read (or create) json file.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.file = os.path.join(dir_path, filename)
        # if file exists
        try:
            f = open(self.file)
            f.close()
        # or not
        except FileNotFoundError:
            print('File does not exist. Creating.')
            init = {}
            with open(self.file, 'w') as outfile:
                json.dump(init, outfile)

        # read
        self._file_read()

    def _file_read(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        self.logs = data
        return data
    
    def _file_write(self,data):
        with open(self.file) as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def log_write(self,date,time,channel,command,user):
        new_entry = {date:{time:{"channel": channel,"command":command,"user":user}}}
        self.logs.update(new_entry)
        self._file_write(self.logs)
