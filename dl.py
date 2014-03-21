import requests

n = 22
url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/march-madness-predictions/bracket-{}.csv"
resp = requests.get(url.format(n))
while resp.status_code == 200:
    lastgood = resp
    n += 1
    print n
    resp = requests.get(url.format(n))

# file comes with windows newlines... replace with unix
text = lastgood.text.replace('\r', '\n')
open("natesilver.csv", 'w').write(text)
