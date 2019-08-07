import json


class Gif_json:

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
            init = []
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
            json.dump(data, outfile)

    def update_file(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.gifs, outfile)

    def gif_delete(self, name):
        self.gifs = [i for i in self.gifs if not (i['name'] == name)]
        self.update_file()

    def gif_add(self, name, url, public=True):
        new_gif = {
            'name': name.lower(),
            'url': url,
            'public': public
        }
        self.file_read()
        # delete if already exists
        self.gif_delete(name)
        self.gifs.append(new_gif)
        self.file_write(self.gifs)

    def get_gif(self, name):
        try:
            return next(item for item in self.gifs if item["name"] == name.lower())
        except Exception:
            return None

            




