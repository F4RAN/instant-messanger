from mongoengine import *


def connectIt():
    connect('instant_messenger', host='127.0.0.1', port=27017)
