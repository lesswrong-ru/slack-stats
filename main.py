#!/usr/bin/env python3

import json
import os
import re
import os.path
from collections import defaultdict
from termcolor import colored

ROOT = '/Users/berekuk/Downloads/slack'

class Stat:
    def __init__(self):
        self.emoji = defaultdict(lambda: defaultdict(int))

    def add_emoji(self, target, emoji):
        self.emoji[target][emoji] += 1

    def top_users(self, emoji, n):
        top = []
        for user in self.emoji.keys():
            top.append({
                'user': user,
                'count': self.emoji[user][emoji]
            })

        top.sort(key=lambda e: e['count'], reverse=True)
        return top[:n]

    def print_top(self, emoji, n):
        print()
        print(colored('*Top {} :{}:*'.format(n, emoji), 'red'))

        for e in self.top_users(emoji, n):
            print('@{}\t{}'.format(e['user'], e['count']))

    def print(self):
        self.print_top('+1', 10)
        self.print_top('-1', 10)
        self.print_top('heavy_plus_sign', 10)
        self.print_top('heavy_minus_sign', 10)
        self.print_top('delta', 10)


def load_users():
    users_file = ROOT + '/users.json'
    users_data = json.load(open(users_file))
    users = {}

    for user in users_data:
        users[user['id']] = user['name']

    return users


def load_channels():
    channels_file = ROOT + '/channels.json'
    channels = []
    for channel in json.load(open(channels_file)):
        channels.append(channel['name'])
    return channels


def process_channel_file(filename, users, stat):
    log = json.load(open(filename))
    for message in log:
        if not 'user' in message:
            continue
        if not message['user'] in users:
            print('{} not found'.format(message['user']))
            continue
        author = users[message['user']]

        if 'reactions' in message:
            for reaction in message['reactions']:
                emoji = reaction['name']
                emoji = re.sub(r'::.*', '', emoji)
                for rater_id in reaction['users']:
                    rater = users[rater_id]
                    stat.add_emoji(author, emoji)


def process_channel(name, users, stat):
    print('processing channel ' + name)
    directory = ROOT + '/' + name
    for filename in os.listdir(directory):
        full_name = os.path.join(directory, filename)
        if not os.path.isfile(full_name):
            continue
        process_channel_file(full_name, users, stat)

def main():
    users = load_users()

    stat = Stat()
    for channel in load_channels():
        process_channel(channel, users, stat)

    print()

    stat.print()

main()
