from bs4 import BeautifulSoup
import os
import pprint

all_message_contents = []
folder = 'ChatExport_12_10_2018'

files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

for file in files:
    with open(os.path.join(folder, file)) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    messages = soup.find_all(attrs={"class": "message"})

    def user_filter(name):
        def filter_func(message):
            from_name = message.find(attrs = {"class": "from_name"})
            return from_name and name in from_name.text and message.find(attrs = {"class": "text"})
        return filter_func

    user_messages = list(filter(user_filter("Frans"), messages))
    message_contents = map(lambda m: m.find(attrs = {"class": "text"}).text, user_messages)
    all_message_contents += message_contents

with open("messages.py", "w") as outfile:
    outfile.write("messages = ")
    outfile.write(pprint.pformat(all_message_contents))
