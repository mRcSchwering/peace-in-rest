# this python file uses the following encoding: utf-8
from fastapi import Query
from typing import List, Dict


name = Query(..., description='Whats your name?')
seconds = Query(..., description='How long should I sleep?')
