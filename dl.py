import os, glob
import requests

os.chdir("../fivethirtyeight-data/march-madness-predictions")
os.system("git pull")
fname = list(sorted(glob.glob("*.csv")))[-1]
os.system("cp {} ../../roundbracket/natesilver.csv".format(fname))
os.chdir("../../roundbracket")

# file comes with windows newlines... replace with unix
text = file("natesilver.csv", "r").read().replace('\r', '\n')
open("natesilver.csv", 'w').write(text)
