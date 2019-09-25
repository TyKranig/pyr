To build the cdlapi package just run the command

python setup.py develop

develop setting makes the install faster and doesn't make a copy of each of the files see
https://stackoverflow.com/questions/1471994/what-is-setup-py
for more information on the arguements

Make sure to create a steam api key at
https://steamcommunity.com/dev/apikey
The way I implemented the obtaining of the key is probably bad but it works
put your key into a .env file in the cdlapi folder and the init script will find it there

Good luck on your games!



Goals for first version
    - Get records for the entirety of CDL, each record includes the match id associated
        - most kills in a game
        - most assists in a game
        - longest game 
        - highest gpm in a game
        - most deaths in a game
        - fastest midas in a game
        - highest net worth in a game
    - Calculate ELO ratings for each current team, this requires the season id to be passed in

Struggles
    - getting player names from account id's not easy with everyone changing names all the time
    - certificates based on what network the scritp is ran on

    9/25/2019
Attempted to hit the api from behind a firewall, didn't work, going to move forward running the api hits on an open network, outputing match results to a file then have a second script parse the json files