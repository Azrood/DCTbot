import json


class GifJson:

    # init is executed when the object is created
    def __init__(self, file):
        self.file = file
        # if file exists
        try:
            f = open(self.file)
            f.close()
        # or not
        except FileNotFoundError:
            print('File does not exist. Creating.')
            init = {}
            with open(file, 'w') as outfile:
                json.dump(init, outfile)

        # read
        self.file_read()

    def file_read(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        self.gifs = data
        return data

    def file_write(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def update_file(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.gifs, outfile, sort_keys=True, indent=4)

    def gif_delete(self, name):
        try:
            self.gifs.pop(name)
            self.update_file()
        except KeyError:
            pass

    def gif_add(self, name, url, public=True):
        new_gif = {name.lower(): {'url': url, 'public': public}}
        self.file_read()
        self.gifs.update(new_gif)
        self.file_write(self.gifs)

    def get_gif(self, name):
        try:
            return self.gifs[name]
        except KeyError:
            return None
