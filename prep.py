# -*- coding: utf8 -*-

import json, csv

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
    "Saint Joseph's": "St. Joseph's",
    "Brigham Young": "BYU",
    "North Carolina State": "NC State",
    "Massachusetts": "UMass",
    "North Dakota State": "North Dakota St.",
    "New Mexico State": "New Mexico St.",
    "North Carolina Central": "NC Central",
    "Louisiana-Lafayette": "Louisiana Lafayette",
    "American University": "American",
    "Weber State": "Weber St.",
    "Massachusetts": "UMass",
    "North Carolina State": "NC State",
}

natesilver = {}
with open("natesilver.csv") as ns:
    rows = csv.reader(ns)
    header = rows.next()
    for row in rows:
        # parse the percentages
        for rowi in [4,5,6,7,8,9]:
            if row[rowi] == "√": row[rowi] = "100%"
            if row[rowi] == "–": row[rowi] = "0%"
            pct = row[rowi][:-1]
            if pct.startswith("<"):
                row[rowi] = .001
            else:
                row[rowi] = float(pct)/100
        teamdata = dict(zip(header, row))
        teamdata["team"] = natesilver_names.get(teamdata["team"], teamdata["team"])
        for key in ["round1", "round2", "round3", "round4", "round5", "round6"]:
            teamdata[key] = float(teamdata[key])
        natesilver[teamdata["team"]] = teamdata

def maketeam(name, seed):
    team = natesilver[name]
    team = {
        "name": team["team"],
        "seed": seed,
        "round1": team["round1"],
        "round2": team["round2"],
        "round3": team["round3"],
        "round4": team["round4"],
        "round5": team["round5"],
        "round6": team["round6"],
    }
    return team

combined = {}

bracket = json.loads(file("bracket.json").read())
for region, teams in bracket.iteritems():
    combined[region] = {}
    for seed, team in teams.iteritems():
        seed = int(seed)
        assert team in natesilver, "couldn't find team {}".format(team)
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
}
for region in combined:
    for seed in combined[region]:
        if combined[region][seed]["name"] in shortnames:
            combined[region][seed]["name"] = shortnames[combined[region][seed]["name"]]

json.dump(combined, open("teams.json", 'w'))
