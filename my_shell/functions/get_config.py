#! /usr/bin/env python3
import yaml
import sys

def get_config():
    # import config yaml file for static variables
    # requirements could change at a later date and easy to use same configs for test cases
    # a file path is not provided throught the command line then use the default values
    with open("./configs/config.yaml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    return config