# -*- coding: utf8 -*-

import json, csv

kenpom = {}
with open("kenpom_2016.csv") as kp:
    rows = csv.reader(kp)
    header = next(rows)
    for row in rows:
        teamdata = dict(zip(header, row))
        kenpom[teamdata["TeamName"]] = {
            "name": teamdata["TeamName"],
            "rating": float(teamdata["Pythag"])
        }

kenpom_names = {
#    "North Carolina St.": "NC State"
}

for name in kenpom:
    if name in kenpom_names:
        newname = kenpom_names[name]
        kenpom[newname] = kenpom[name]
        kenpom[newname]["name"] = newname
        del kenpom[name]

combined = {}

natesilver_names = {
    "Michigan State": "Michigan St.",
    "Wichita State": "Wichita St.",
    "Ohio State": "Ohio St.",
    "Iowa State": "Iowa St.",
    "Oklahoma State": "Oklahoma St.",
    "Virginia Commonwealth": "VCU",
    "San Diego State": "San Diego St.",
    "Arizona State": "Arizona St.",
    "Kansas State": "Kansas St.",
    "Brigham Young": "BYU",
    "Massachusetts": "UMass",
    "North Dakota State": "North Dakota St.",
    "New Mexico State": "New Mexico St.",
    "North Carolina Central": "NC Central",
    "Louisiana-Lafayette": "Louisiana Lafayette",
    "American University": "American",
    "Weber State": "Weber St.",
    "Massachusetts": "UMass",
    "North Carolina State": "NC State",
    "Georgia State": "Georgia St.",
    "Virginia Commonwealth": "VCU",
    "Boise State": "Boise St.",
    "Louisiana State": "LSU",
    "North Carolina State": "North Carolina St.",
    "Southern Methodist": "SMU",
    "Ole Miss": "Mississippi",
    "Miami (FL)": "Miami FL",
    "St. Joseph's": "Saint Joseph's",
    "Southern California": "USC",
    "Arkansas-Little Rock": "Arkansas Little Rock",
    "South Dakota State": "South Dakota St.",
    "North Carolina-Wilmington": "UNC Wilmington",
    "Oregon State": "Oregon St.",
    "Fresno State": "Fresno St.",
    "Cal State Bakersfield": "Cal St. Bakersfield",
    "North Carolina-Asheville": "UNC Asheville",
    "Florida State": "Florida St.",
    "Mississippi State": "Mississippi St.",
    "Albany (NY)": "Albany",
    "St. John's (NY)": "St. John's",
    "South Dakota State": "South Dakota St.",
    "Colorado State": "Colorado St.",
    "Pennsylvania": "Penn",
    "Missouri State": "Missouri St.",
    "Alabama State": "Alabama St.",
}

natesilver = {}
with open("natesilver.csv") as ns:
    rows = csv.reader(ns)
    header = next(rows)
    for row in rows:
        # skip women's tourney data
        if row[0] != "mens": continue

        teamdata = dict(zip(header, row))
        teamdata["team"] = natesilver_names.get(teamdata["team_name"], teamdata["team_name"])
        if teamdata["team"] not in kenpom:
            print("missing {}".format(teamdata["team"]))
        for key in ["rd2_win", "rd3_win", "rd4_win", "rd5_win", "rd6_win", "rd7_win"]:
            teamdata[key] = float(teamdata[key])
        natesilver[teamdata["team"]] = teamdata

def maketeam(name, seed):
    team = kenpom[name]
    team["seed"] = seed
    team["round1"] = natesilver[name]["rd2_win"]
    team["round2"] = natesilver[name]["rd3_win"]
    team["round3"] = natesilver[name]["rd4_win"]
    team["round4"] = natesilver[name]["rd5_win"]
    team["round5"] = natesilver[name]["rd6_win"]
    team["round6"] = natesilver[name]["rd7_win"]
    return team

bracket = json.loads(open("bracket.json").read())
for region, teams in bracket.items():
    combined[region] = {}
    for seed, team in teams.items():
        seed = int(seed)
        if isinstance(team, list):
            for t in team:
                assert t in kenpom, "{} not in kenpom".format(t)
                assert t in natesilver, "{} not in natesilver".format(t)
            # for now, ignore the first four... pick the higher ranked team to win
            if kenpom[team[0]]["rating"] > kenpom[team[1]]["rating"]:
                combined[region][seed] = maketeam(team[0], seed)
            else:
                combined[region][seed] = maketeam(team[1], seed)
        else:
            assert team in kenpom, "{} not in kenpom".format(team)
            assert team in natesilver, "{} not in natesilver".format(team)
            combined[region][seed] = maketeam(team, seed)

shortnames = {
    "Stephen F. Austin": "SF Austin",
    "Louisiana Lafayette": "Louisiana Laf.",
    "Western Michigan": "Western Mich.",
    "Eastern Kentucky": "Eastern Ky.",
    "North Dakota St.": "ND State",
    "New Mexico St.": "NM State",
    "George Washington": "George Wash.",
    "Coastal Carolina": "Coast. Car.",
    "Eastern Washington": "E Washington",
}
for region in combined:
    for seed in combined[region]:
        if combined[region][seed]["name"] in shortnames:
            combined[region][seed]["name"] = shortnames[combined[region][seed]["name"]]

json.dump(combined, open("teams.json", 'w'))
json.dump(combined, open("teams_pretty.json", "w"), indent=2)
