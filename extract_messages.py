# -*- coding: utf-8 -*-
# Extract all incoming messages for every chat

import json
import os
import io
import utils

default_self_name = 'Ferdinand_Mütsch'
default_input_path = './telegram-history-dump/output/json/'
default_output_file = './data/filtered_dump.json'

messages = {}

def extract(input_path, self_name):
    input_files = os.listdir(input_path)   
    messages[self_name] = []     

    for f in input_files:
        with open(input_path + f) as data_file:
            dump_lines = data_file.readlines()
            dump_json = [utils.byteify(json.loads(l)) for l in dump_lines]
            name = f.replace('.jsonl', '')
            messages[name] = [m['text'].lower() for m in dump_json if 'text' in m and m['out'] == False]
            messages[self_name].extend([m['text'].lower() for m in dump_json if 'text' in m and m['out'] == True])

    return messages

def stats():
    for key in messages: 
        print key + ": " + str(len(messages[key]))

def dump(output_file):
    with io.open(output_file, 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(messages, encoding='utf8', ensure_ascii=False)))

def main():
    extract(default_input_path, default_self_name)
    stats()
    dump(default_output_file)

# Dump to file if started standalone
if __name__ == "__main__": main()