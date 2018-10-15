from bs4 import BeautifulSoup
import os
import pprint

folder = 'ChatExport_12_10_2018'

users = [
    'Emil',
    'Malcolm',
    'Robin',
    'David',
    'Olav',
    'Hannes',
    'Frans'
]

all_message_contents = { name: [] for name in users }

files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

for file in files:
    filename = os.path.join(folder, file)
    print("Parsing", filename)
    with open(filename) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    messages = soup.find_all(attrs={"class": "message"})

    def user_filter(name):
        def filter_func(message):
            from_name = message.find(attrs = {"class": "from_name"})
            return from_name and name in from_name.text and message.find(attrs = {"class": "text"})
        return filter_func

    for name in users:
        user_messages = list(filter(user_filter(name), messages))
        message_contents = map(lambda m: m.find(attrs = {"class": "text"}).text, user_messages)
        all_message_contents[name] += message_contents

for name in users:
    filename = name + "_messages.py"
    print("Writing", filename)
    with open(filename, "w") as outfile:
        outfile.write("messages = ")
        outfile.write(pprint.pformat(all_message_contents[name]))
