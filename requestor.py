import requests
from bs4 import BeautifulSoup
import json
import csv
# import os.path



liveURL = "http://nepl.league.papa.org/pointsByMeet/"
localURL = "/Users/drubles/Development/code/score-scraper/pointsByMeet31.html"



def getSoup(num):
    print "Sending GET request to %s" % liveURL + str(num)
    r = requests.get(liveURL + str(num))
    print "Response: " + str(r.status_code)
    if r.status_code != 200:
        print "Exiting now..."

    else:
        print "Scraping site for scores."

    soup = BeautifulSoup(r.content, "html5lib")
    # soup = BeautifulSoup(open(liveURL), "html5lib")

    # Todo: remove this comment block used for writing liveUrl to localURL
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

    # Store the accessLink from this URL in the JSON file for reference
    accessLink = soup.find('a', attrs = {'accesskey':'r'})
    pageDigest['accessLink'] = accessLink['href']

    # Scores are kept in a single table on this page: Collecting names and scores here
    scoreTable = soup.find('tbody')
    firstRow = scoreTable.find('tr')
    playerData = {}
    count = 0
    for row in scoreTable.findAll('tr'):
        # Loop return objects shaped => {"0": {"name": "Dru Edmondson", "scores": [0,1,2,3]}}
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
    print "Total players and their scores being saved: " + str(count+1)

    # Write json to file named after season title
    filename = seasonTitle.replace(" ", "_")
    result_json = json.dumps(playerData)
    with open('json/%s.json' % filename, 'w') as outfile:
        json.dump(pageDigest, outfile)
        print "Saved %s.json" % filename

    # Also write data to csv file of the same name:
    # first make csv header depending on number of matches on score page
    header = ['playerName']
    count = 0
    for i in playerData[0]['scores']:
        string = 'match' + str(count + 1)
        count += 1
        header.append(string)

    with open('json/%s.json' % filename) as json_file:
        data = json.load(json_file)

    playersToWrite =  playerData.values()
    csvFile = open('csv/%s.csv' % filename, 'w')
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(header)
    for player in playersToWrite:
        row = []
        row.append(player['name'])
        row.extend(player['scores'])
        csvWriter.writerow(row)
    csvFile.close()
    print "Saved %s.csv" % filename

# 
for num in range(0, 32):
    try:
        getSoup(num)
    except:
        continue
    finally:
        print "%s complete." % liveURL + str(num)
print "All Done"
