"""Module to handle logging for moderator commands (kick,ban,clear) and reading logs (logs are stored in json file)"""
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
        with open(self.file,'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def _get_dates(self, num=10):
            days = list(self.logs.keys())
            return days[:num]

    def _get_channel(self, date, channel):
        try:
            return [ (k,v['user'],v['command']) for k,v in self.logs[date].items() if v['channel'] == channel ]
        except KeyError:
            return None

    def _get_command(self, date, command):
        try:
            return [ (k,v['user'],v['channel']) for k,v in self.logs[date].items() if v['command'] == command ]
        except KeyError:
            return None

    def _get_user(self, date, user):
        try:
            return [ (k,v["command"],v["channel"]) for k,v in self.logs[date].items() if v['user'] == user ]
        except KeyError:
            return None
    
    def _get_log_day(self, date):
        try:
            return [ (k,v["user"],v["command"],v["channel"]) for k,v in self.logs[date].items()]
        except KeyError:
            return None

    def _get_date_time(self,user,command,channel):
        try:
            return [(k,time) for k,v in self.logs.items() for time in v.keys()  if {'channel':channel,'user':user,'command':command} in v.values() ]
        except KeyError:
            return None

    def log_write(self, date, time, channel, command,user):
        """write logs in json file. All parameters are `str`
        
        `date` in format \'dd/mm/yyyy\' 

        `time` in format \'24h60m60s\'
        """
        new_entry = {date:{time:{"channel": channel,"command":command,"user":user}}}
        if date in self.logs.keys() :
            self.logs[date].update(new_entry[date])
        else:
            self.logs.update(new_entry)
        self._file_write(self.logs)
    
    def log_latest(self, num=10):
        """return 'num' latest dates in the log file. Default to 10"""
        return self._get_dates(num)

    def log_read(self, date, user, command, channel):
        """returns logs in a list depending on the parameters passed."""
        if date not in self._get_dates():
            return None
        elif channel is not None and user is not None and command is not None:
            return self._get_date_time(user, command, channel) #[(date,time),(date,time)]
        elif channel is not None :
            if user is None and command is None:
                return self._get_channel(date,channel) #[(time,user,command),(time,user,command)]
            elif user is None:
                tired=[]
                sorry = self._get_channel(date,channel)
                for tuple in sorry:
                    if tuple[2] == command:
                        tired.append(tuple)
            elif command is None:
                tired = []
                sorry = self._get_channel(date,channel)
                for tuple in sorry:
                    if tuple[1] == user:
                        tired.append(tuple) 
            return tired
        elif command is not None:
            if user is None and channel is None:
                return self._get_command(date,command) #[(time,user,channel),(time,user,channel)]
            elif channel is None:
                tired=[]
                sorry = self._get_command(date,command)
                for tuple in sorry:
                    if tuple[1] == user:
                        tired.append(tuple)
            elif user is None:
                tired = []
                sorry = self._get_command(date,command)
                for tuple in sorry:
                    if tuple[2] == channel:
                        tired.append(tuple)
            return tired
        elif user is not None :
            if channel is None and command is None:
                return self._get_user(date,user) #[(time,command,channel),(time,command,channel)]
            elif channel is None:
                tired=[]
                sorry = self._get_user(date,user)
                for tuple in sorry:
                    if tuple[2] == channel :
                        tired.append(tuple)
            elif command is None:
                tired = []
                sorry = self._get_user(date,user)
                for tuple in sorry:
                    if tuple[1] == command:
                        tired.append(tuple)
            return tired
        else:
            return self._get_log_day(date) #[(time,user,command,channel)]
            