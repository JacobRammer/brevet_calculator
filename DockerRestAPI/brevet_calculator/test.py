import os
import sys
import inspect
import os
from flask import Flask, redirect, url_for, request, render_template, session
import flask
from pymongo import MongoClient
import arrow

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

def test_submit(message):
    assert(message == "Cannot submit data! At least one input is missing")
    
def test_display(message):
    """
    Tests display on no data, does not return an error, just 
    renders blank page
    """
    
    assert(message == "Nothing to display")