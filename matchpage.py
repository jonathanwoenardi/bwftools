import json
import sys
import re
import requests
import js2py
from bs4 import BeautifulSoup

address = "https://bwf.tournamentsoftware.com/sport/"
regex = "statsGraphSeries = {.*};"

def getSeries(stat):
    return stat[len("statsGraphSeries = "):-1]

def jsonify(jsmap):
    # convert map where keys are not enclosed with quotes to proper json
    command = "JSON.stringify(%s)" % jsmap
    jsobj = js2py.eval_js(command)
    return jsobj

def getScore(point):
    return int(point["meta"][len("Player ?: "):])

def getScores(player):
    scores = []
    for point in player:
        scores.append(getScore(point))
    return scores

def parseSeries(dictio):
    series = dictio["series"]
    player1 = series[0]["data"]
    player2 = series[1]["data"]
    p1 = getScores(player1)
    p2 = getScores(player2)
    return [p1, p2]

def cutProfilePath(path):
    return path[len("/player-profile/"):]

def getPlayerID(linkTag):
    r = requests.get(address + linkTag["href"])
    soup = BeautifulSoup(r.text, "html.parser")
    subtitle = soup.find("div", {"class": "subtitle"})
    profile = subtitle.find("a")
    playerID = cutProfilePath(profile["href"])
    return playerID

def parseMatchPage(path):
    games = []
    r = requests.get(path)
    # players
    soup = BeautifulSoup(r.text, "html.parser")
    p1 = soup.find("a", {"id": "lnk1"})
    id1 = getPlayerID(p1)
    p2 = soup.find("a", {"id": "lnk3"}) # why lnk3 :/
    id2 = getPlayerID(p2)
    # scores
    stats = re.findall(regex, r.text)
    for stat in stats:
        series = getSeries(stat)
        jsobj = jsonify(series)
        dictio = json.loads(jsobj)
        parsed = parseSeries(dictio)
        games.append(parsed)
    return id1, id2, games

if __name__ == "__main__":
    path = sys.argv[1]
    player1, player2, games = parseMatchPage(path)
    print(player1)
    print(player2)
    print(games)
