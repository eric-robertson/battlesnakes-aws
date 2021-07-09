from os import system
import json
from flask import Flask, request
import Snake
import Packager

f = open('./states/a.json')
data = json.load( f )

Packager.from_json(data).log()