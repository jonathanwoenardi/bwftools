import sys
from bs4 import BeautifulSoup

def parseSVGChart(filename):
    player1, player2 = [], []
    with open(filename) as f:
        svg = f.read()
        soup = BeautifulSoup(svg, 'xml')
        lines = soup.find_all("line", class_="ct-point")
        for line in lines:
            meta = line["ct:meta"]
            if getPlayerID(meta) == "1":
                player1.append(getScore(meta))
            else:
                player2.append(getScore(meta))

    return player1, player2

def getPlayerID(meta):
    return meta[7]

def getScore(meta):
    return int(meta[10:])             

if __name__ == "__main__":
    filename = sys.argv[1]
    player1, player2 = parseSVGChart(filename)
    print(player1)
    print(player2)
