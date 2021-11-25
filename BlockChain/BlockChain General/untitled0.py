#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 16:04:46 2021

@author: blackmoney
"""
import datetime
import hashlib
import json
from flask import jsonify, Flask


class Blockchain:
    def __init__(self):
        