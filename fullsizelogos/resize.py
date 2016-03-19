import os
from glob import glob

def sh(cmd):
    print(cmd)
    os.system(cmd)

#for logo in glob("*.png") + glob("*.jpg") + glob("*.gif"):
for logo in ["Holy Cross.png"]:
    name = logo[:-4]
    sh('convert "{}" -resize 50x50 "../logos/{}.png"'.format(logo, name))
