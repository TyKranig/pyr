from dataObjects import Captain
import io
import os

def loadCaptains():
    seasons = []

    with open(os.getcwd() + r"/io/static/.env", "r") as file:
        captains = {}
        for line in file:
            if "Season" in line:
                break