import requests
from bs4 import BeautifulSoup
import json

LiveURL = "http://nepl.league.papa.org/pointsByMeet/31"
localURL = "/Users/drubles/Development/code/score-scraper/pointsByMeet31.html"

# r = requests.get(URL)
# soup = BeautifulSoup(r.content)
soup = BeautifulSoup(open(localURL), "html.parser")


# filename = "pointsByMeet31.html"
# with open(filename, 'w') as f:
#     f.write(str(soup))


allPlayers = {}
scoreTable = soup.find('tbody')
firstRow = scoreTable.find('tr')

count = 0

for row in scoreTable.findAll('tr'):
    player = {}
    nameCell = row.find('td')
    scoreCells = firstRow.findAll('td', attrs = {'class':'toggleStyle'})
    player['name'] = nameCell.text
# #  build an array of player scores with 8 elements
    scoreArray = []
    for td in scoreCells:
        scoreArray.append(td.text or "0")
    player['scores'] = scoreArray
    allPlayers[count] = player
    count += 1
    print count

# print "Players found: ", len(allPlayers)
# print "first player: ", allPlayers[0]

print type(allPlayers)

# output of print(row) in for loop
# <td>Aaron Rogers</td>
# <td class="textCenter">100</td>
# <td class="textCenter">100</td>
# <td class="textCenter toggleStyle" data-style="" title=""></td>
# <td class="textCenter toggleStyle" data-style="color:#6040A0" title="Group 8">10</td>
# <td class="textCenter toggleStyle" data-style="color:#6040A0" title="Group 8">17</td>
# <td class="textCenter toggleStyle" data-style="color:#B0B000" title="Group 5">32</td>
# <td class="textCenter toggleStyle" data-style="" title=""></td>
# <td class="textCenter toggleStyle" data-style="color:#009999" title="Group 11">22</td>
# <td class="textCenter toggleStyle" data-style="color:#B0B000" title="Group 69">19</td>
# <td class="textCenter toggleStyle" data-style="" title=""></td>
