"""Module to handle logging for moderator commands (kick,ban,clear).

Write and read logs in json file.
"""
import json
import os


class CommandLog:
    """Class to handle reading and writing logs in json file."""

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

    def _file_write(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def _get_dates(self, num=10):
        days = list(self.logs.keys())
        return days[:num]

    def _get_channel(self, date, channel):
        try:
            return [(k, v['user'], v['command'])
                    for k, v in self.logs[date].items()
                    if v['channel'] == channel]
        except KeyError:
            return None

    def _get_command(self, date, command):
        try:
            return [(k, v['user'], v['channel'])
                    for k, v in self.logs[date].items()
                    if v['command'] == command]
        except KeyError:
            return None

    def _get_user(self, date, user):
        try:
            return [(k, v["command"], v["channel"])
                    for k, v in self.logs[date].items() if v['user'] == user]
        except KeyError:
            return None

    def _get_log_day(self, date):
        try:
            return [(k, v["user"], v["command"], v["channel"])
                    for k, v in self.logs[date].items()]
        except KeyError:
            return None

    def _get_date_time(self, user, command, channel):
        try:
            return [(k, time) for k, v in self.logs.items()for time in v.keys()
                    if {'channel': channel, 'user': user, 'command': command} in v.values()]  # noqa:E501
        except KeyError:
            return None

    def log_write(self, date, time, channel, command, user):
        """Write logs in json file. All parameters are `str`.

        `date` in format 'dd/mm/yyyy'

        `time` in format '24h60m60s'
        """
        new_entry = {
            date: {time: {"channel": channel, "command": command, "user": user}}  # noqa:E501
        }

        if date in self.logs.keys():
            self.logs[date].update(new_entry[date])
        else:
            self.logs.update(new_entry)
        self._file_write(self.logs)

    def log_latest(self, num=10):
        """Return 'num' latest dates in the log file. Default to 10."""
        return self._get_dates(num)

    def log_read(self, date, user, command, channel):
        """Return logs in a list depending on the parameters passed."""
        # channel, user and command will be called "entries"

        args_list = [user, command, channel]
        bin_array = [int(i is not None) for i in args_list]  # convert ["foo", None, None] to [1, 0, 0]  # noqa:E501
        n = int("".join(str(x) for x in bin_array), 2)  # binary array to int

        if date not in self._get_dates():  # if date is not in the logs, then there are no logs :)
            return None

        elif n == 0:  # [None, None, None]
            # returns list of tuples of when all logged users used the commands in the logged channels of a given date
            return self._get_log_day(date)  # [(time,user,command,channel)]

        elif n == 1:  # [None, None, channel]
            return self._get_channel(date, channel)  # [(time,user,command),(time,user,command)]

        elif n == 2:  # [None, command, None]
            return self._get_command(date, command)  # [(time,user,channel),(time,user,channel)]

        elif n == 3:  # [None, command, channel]
            tmp = self._get_channel(date, channel)  # just to avoid calling the function multiple times
            # below is a list of tuples whose commands only the specified command
            return [tuple_ for tuple_ in tmp if tuple_[2] == command]
            # or :
            # tmp = self._get_command(date, command)
            # # list of tuples whose channels are only the specified channel
            # return [tuple_ for tuple_ in sorry if tuple_[2] == channel]

        elif n == 4:  # [user, None, None]
            return self._get_user(date, user)  # [(time,command,channel),(time,command,channel)]

        elif n == 5:  # [user, None, channel]
            tmp = self._get_channel(date, channel)
            # below is a list of tuples whose users are only the specified user
            return [tuple_ for tuple_ in tmp if tuple_[1] == user]
            # or
            # sorry = self._get_user(date,user)
            # list of tuples whose channels are only the specified channel
            # return [ tuple for tuple in sorry if tuple[2] == channel ]

        elif n == 6:  # [user, command, None]
            tmp = self._get_command(date, command)
            # list of tuples whose users are only the specified user
            return [tuple_ for tuple_ in tmp if tuple_[1] == user]
            # or
            # sorry = self._get_user(date,user)
            # # list of tuples whose commands are only the specified command
            # return [ tuple for tuple in sorry if tuple[1] == command ]

        elif n == 7:  # [user, command, channel]
            return self._get_date_time(user, command, channel)  # return a list of tuple [(date,time),(date,time)]
