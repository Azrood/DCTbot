"""Module to handle !gif command (gifs are stored in json file)."""
import json
import os


class GifJson:
    """Class to handle reading gifs url from json file."""

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
        self.gifs = data
        return data

    def _file_write(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def _update_file(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.gifs, outfile, sort_keys=True, indent=4)

    def gif_delete(self, name):
        """Delete gif entry and update file."""
        try:
            self.gifs.pop(name)
            self._update_file()
        except KeyError:
            pass

    def gif_add(self, name, url, public=True):
        """Add gif entry and update file."""
        new_gif = {name.lower(): {'url': url, 'public': public}}
        self._file_read()
        self.gifs.update(new_gif)
        self._file_write(self.gifs)

    def get_gif(self, name):
        """Get gif corresponding to 'name'."""
        try:
            return self.gifs[name]
        except KeyError:
            return None

    def get_names_string(self, private=True):
        """Get multiline string of gifs names.

        If private is true, only public gifs are returned.

        """
        if private:
            new_dict = {k: v for k, v in self.gifs.items() if v['public']}
        else:
            new_dict = self.gifs
        # Return multiline string with names
        return '\n'.join(new_dict.keys())
