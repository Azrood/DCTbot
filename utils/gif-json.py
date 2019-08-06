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

    def print_data(self):
        for l in self.gifs:
            print(l['name'])
            print(l['url'])
            print(l['public'])
            print('............')

# Tests


# Creation of object (ie : execution of __init__)
gifs_json = Gif_json("gifs.txt")

print("========================")

# add test
gifs_json.gif_add('sergei', 'Sergei Url')

gifs_json.print_data()

print("========================")

gifs_json.gif_add('ludo', 'ludo_gif_url')
gifs_json.gif_add('sergei', 'Sergei_gif_2.0')
gifs_json.gif_add('karnage', 'Karnage url', False)

gifs_json.print_data()

print("========================")

gifs_json.gif_delete('karnage')
gifs_json.gif_delete('ludo')

gifs_json.print_data()

# This is what will be called when we will want to get a gif for a name :
print("========================")
print("I try to get gif for sergei")
gif = gifs_json.get_gif('sergei')
if gif:
    print(gif['url'])
else:
    print("Invalid name")

print("========================")
print("I try to get gif for toto")
gif = gifs_json.get_gif('toto')
if gif:
    print(gif['url'])
else:
    print("Invalid name")
