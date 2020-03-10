import requests
from bs4 import BeautifulSoup
import json

liveURL = "http://nepl.league.papa.org/pointsByMeet/31"
localURL = "/Users/drubles/Development/code/score-scraper/pointsByMeet31.html"

# r = requests.get(URL)
# soup = BeautifulSoup(r.content)
soup = BeautifulSoup(open(localURL), "html.parser")

# Todo: remove this comment block used for writing liveUrl to local file
# filename = "pointsByMeet31.html"
# with open(filename, 'w') as f:
#     f.write(str(soup))

# pageDigest will collect all of the parsed page data into a dict with 3 keys
# "seasonTitle", "accessLink", and "playerData"
pageDigest = {}

pageTitle = soup.find('title').text
# Find just the relevant text to assign to seasonTitle Key
seasonTitle = pageTitle.split(':')[0]
pageDigest['seasonTitle'] = seasonTitle

accessLink = soup.find('a', attrs = {'accesskey':'r'})
pageDigest['accessLink'] = accessLink['href']

scoreTable = soup.find('tbody')
firstRow = scoreTable.find('tr')

playerData = {}
count = 0
for row in scoreTable.findAll('tr'):
    player = {}
    nameCell = row.find('td')
    scoreCells = firstRow.findAll('td', attrs = {'class':'toggleStyle'})
    player['name'] = nameCell.text
#  build an array of player scores with 8 elements
    scoreArray = []
    for td in scoreCells:
        scoreArray.append(td.text or "0")
    player['scores'] = scoreArray
    playerData[count] = player
    count += 1

pageDigest['playerData'] = playerData

filename = seasonTitle.replace(" ", "_")
result_json = json.dumps(playerData)

# Write json to file named after season title
with open('%s.json' % filename, 'w') as outfile:
    json.dump(pageDigest, outfile)

# Todo: also write result to a CSV file with a similar name
#  Headers should be 'Player Name', 'Match 1', 'Match 2' etc depending on
# number of matches in a playerScore
