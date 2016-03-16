import os, glob
import requests

def sh(cmd):
    print(cmd)
    os.system(cmd)

sh("wget http://projects.fivethirtyeight.com/march-madness-api/2016/fivethirtyeight_ncaa_forecasts.csv -O natesilver.csv")
