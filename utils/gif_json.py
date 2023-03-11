"""Module to handle !gif command (gifs are stored in json file)."""

import contextlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class GifJson:
    """Class to handle reading gifs url from json file."""

    # init is executed when the object is created
    def __init__(self, filename):
        """Init object.

        Read (or create) json file.
        """
        self.file = Path(__file__).parent / filename
        self.gifs = {}

        # create file if doesn't exist
        if not self.file.is_file():
            logger.warning('File does not exist. Creating.')
            with open(self.file, 'w') as outfile:
                json.dump({}, outfile)

        # read
        self._file_read()

    def _file_read(self) -> dict:
        with open(self.file) as json_file:
            data = json.load(json_file)
        self.gifs: dict = data
        return data

    def _file_write(self, data: dict):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def _update_file(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.gifs, outfile, sort_keys=True, indent=4)

    def gif_delete(self, name: str):
        """Delete gif entry and update file."""
        with contextlib.suppress(KeyError):
            self.gifs.pop(name)
            self._update_file()

    def gif_add(self, name: str, url: str, public=True):
        """Add gif entry and update file."""
        new_gif = {name.lower(): {'url': url, 'public': public}}
        self._file_read()
        self.gifs.update(new_gif)
        self._file_write(self.gifs)

    def get_gif(self, name: str):
        """Get gif corresponding to 'name'."""
        return self.gifs.get(name)

    def get_names_string(self, private=True) -> str:
        """Get multiline string of gifs names.

        If private is true, only public gifs are returned.

        """
        if private:
            new_dict = {k: v for k, v in self.gifs.items() if v['public']}
        else:
            new_dict = self.gifs
        # Return multiline string with names
        return '\n'.join(new_dict.keys())
