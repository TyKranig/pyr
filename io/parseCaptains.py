from dataObjects import Captain
from dao import DataWriter
import io
import os

def loadCaptains():
  seasons = []

  input = DataWriter("Captains")

  with open(os.getcwd() + r"\io\static\Captains.txt", "r") as file:
    
    captains = []
    for index, line in enumerate(file):
      if "Season" in line:
        if len(captains) > 0:
          seasons.append(captains.copy())
          captains = []
      else:
        arr = line.split("https://www.dotabuff.com/players/")
        print(arr)
        captains.append({
          "name": arr[0].strip(),
          "playerId": int(arr[1].strip())
        })
  return seasons

if __name__ == "__main__":
    print(loadCaptains())