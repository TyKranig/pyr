Pyr is a Python based script that queries valves API for dota matches in order to obtain match data.
Match data is then inserted into a mongo database hosted on my server.
The script then extracts various records from matches such as,
  Longest match
  Shortest match
  Most Kills in a match
  Most Deaths in a match
  etc.
These records are then uploaded to a google spreadsheet using the gspread library.

Spreadsheet Upload: sheetwriter.py
Api Calls: apicall.py
Mongo Interface: dao.py
Script to call: writer.py

Running this on another machine won't work unless you have a mongo database setup.
After setting up the mongo database you need to set the correct IP for said database in dao.py
Two files also nescassary are .env and a json key for the google sheets api.
Steam api key: https://steamcommunity.com/dev/apikey
Dashboard for google sheets api: https://console.cloud.google.com/apis/dashboard

Put both of those in the io folder in order for the script to run properly

Below is a series of notes I wrote during the development to keep track of where I am at

To build the cdlapi package just run the command
```
python setup.py develop
```
develop setting makes the install faster and doesn't make a copy of each of the files see
```
https://stackoverflow.com/questions/1471994/what-is-setup-py
```

for more information on the arguements

Make sure to create a steam api key at
```
https://steamcommunity.com/dev/apikey
```

The way I implemented the obtaining of the key is probably bad but it works

put your key into a .env file in the cdlapi folder and the init script will find it there

Good luck on your games!



### Goals for first version
    - [] Get records for the entirety of CDL, each record includes the match id associated
        - [x] most kills in a game
        - [x] most assists in a game
        - [x] longest game 
        - [x] highest gpm in a game
        - [x] most deaths in a game
        - [] fastest midas in a game
        - [] highest net worth in a game
    - [] Calculate ELO ratings for each current team, this requires the season id to be passed in

### Struggles
    - getting player names from account id's not easy with everyone changing names all the time
    - certificates based on what network the scritp is ran on

### 9/25/2019
Attempted to hit the api from behind a firewall, didn't work, going to move forward running the api hits on an open network, 

outputing match results to a file then have a second script parse the json files

### 9/27/2019
Writer.py contains some examples for parsing json and getting data, for example loading each of the kill counts into a heap and getting the top 5

For inserting the data into a heap https://stackoverflow.com/questions/42985030/inserting-dictionary-to-heap-python helped a lot

### 10/20/2019
been a while but some progress has been made, I still need to focus on converting the output of the api hits to a google sheet for sharing
I think trying to multithread the script would be very useful as well, those are two milestones that I want to hit before I move onto another project
Last thing I need to setup a crontab job to run the script every now and then

Efficiency is another issue, I don't store the data in a databse right now, that might be a fun project as well

### 10/26/19
Got the google sheets api to work using https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
That page also gives a link to the documentation of the gspread https://gspread.readthedocs.io/en/latest/ documentation which is very handy

### 11/9/2019
Cron job is running and all of the data is being converted to a google sheet
Output of the cron job is at ~/cron.out on the server
Cron run logs can be found using the command grep "cron" /var/log/syslog.1
Add the .1 because the script runs at midnight and the logs also get backed up then
Next task is to get player names using the 32 bit player id, you need to 64 bit id to search
https://dev.dota2.com/showthread.php?t=58317&highlight=teaminfo for getting this

### 12/10/2019
Added mongodb support, still not implemented fully but testing and querying is much faster then hitting an api
The goal at the end, apart from speed, is to add more extensive records such as fasting game in season 3, or 
most deaths on a player whose name starts with a, a database allows for that and I made the choice to use
mongodb because of the ease of setup, I don't have to stand up tables, just manage collections of data, this works
really well for the current system because I can narrow down the collections I need to
games
players
The players collection may come in handy later

### 12/17/2019
The next big change is going to be converting from getting every single match every time the script runs to just grabbing the last few matches
MongoDB does support insert or update so that shouldn't be too big of an issue my only worry is run time
Run time should be fine because we can index using match ids but in another project I ran into run time issues when indexing by string
Few new classes that I need to add are
Match.py
new method to io.py that updates matches in the database

### 1/8/2020
First update of 2020! I added the ability to get records from specific seasons a few days ago whcih was a huge advancement, it should make some more specific records such as Captain statistics easier, I also want to add in specific player records as well in order to get more players interested in the data

### 1/11/2020
While working on some of the DataObjects I realized that I fell into the Java trap on this project. When I started the project I instantly thought that objects would make this process easier but it has turned out that for what this project accomplishes, using objects is like putting a circle in a square hole for some projects, making the project more complicated then it needs to be I'm glad I used objects so I could learn about how OOP can be misused, or overused, in the future I may come back and refactor a ton

### 1/15/2020
Update in mid January, this weekend I finished and released the total wins feature plus seasonal records and got some positive feedback, I think the next big update is going to be win percentage and adding in matches that were not ticketed or played on the wrong ticket for whatever reason. After that update I'm not to sure where the project goes, I'm going to keep developing but move to another python project I think. I also am hoping to expand records to RD2L as well, there are currently 20 seasons of RD2L so that would be a lot more data to parse and not front facing features like performance come into play which could be a bigger task to take on.

### 1/19/20
Ran into a decent road block where old practice matches cannot be pulled from the dota 2 api, this is because if a match isn't ticketed then the match is just counted as a practice match. The only thing I can think of left to add to the app is correcting matches inserted with the wrong season number, due to not quite having the new ticket yet or for some other reason, sometimes a ticket gets used for an inhouse as well.