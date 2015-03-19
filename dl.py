import os, glob
import requests

def sh(cmd):
    print cmd
    os.system(cmd)

os.chdir("../fivethirtyeight-data/march-madness-predictions-2015/mens")
sh("git pull")
fname = list(sorted(glob.glob("*.tsv")))[-1]
sh("cp {} ../../../roundbracket/natesilver.tsv".format(fname))
