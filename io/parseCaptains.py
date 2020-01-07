from dataObjects import Captain
from dao import DataWriter
import io
import os

def loadCaptains():
    seasons = []

    input = DataWriter("Captains")

    with open(os.getcwd() + r"/io/static/.env", "r") as file:
        captains = {}
        for line in file:
            if "Season" in line:
                break