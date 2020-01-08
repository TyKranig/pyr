from dataObjects import Captain
from dao import DataWriter
import io
import os

def loadCaptains():
  seasons = []

  input = DataWriter("Captains")

  with open(os.getcwd() + r"/io/static/.env", "r") as file:
    captains = []
    for line in file:
      if "Season" in line:
        seasons.append(captains.copy())
        captains = []
      else:
        arr = line.split("\t")
        captains.append({
          "name": arr[0],
          "playerId": arr[1].split("https://www.dotabuff.com/players/")[1]
        })
