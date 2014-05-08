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
with open("silver.csv") as ns:
    rows = csv.reader(ns)
    header = rows.next()
    for row in rows:
        for i in [0,4,5,6,7,8,9,10,11,12]:
            if row[i] == "--": row[i] == -1
            else:              row[i] = float(row[i])

        teamdata = dict(zip(header, row))
        teamdata["team_name"] = natesilver_names.get(teamdata["team_name"], teamdata["team_name"])
        natesilver[teamdata["team_name"]] = teamdata

def maketeam(name, seed):
    team = natesilver[name]
    team = {
        "name": team["team_name"],
        "seed": seed,
        "round1": team["rd2_win"], #nate counts the play round as the first
        "round2": team["rd3_win"], #round, I don't... hence the mismatch
        "round3": team["rd4_win"],
        "round4": team["rd5_win"],
        "round5": team["rd6_win"],
        "round6": team["rd7_win"],
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
