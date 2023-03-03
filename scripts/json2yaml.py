#!/usr/bin/env python3

import sys, yaml, json

# source: https://stackoverflow.com/a/33300001
def str_presenter(dumper, data):
  if len(data.splitlines()) > 1: 
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

if __name__ == '__main__':
    json_data = json.load(sys.stdin)
    yaml_text = yaml.dump(json_data)
    print(yaml_text)
