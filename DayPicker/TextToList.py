
# Reads a text file and stores in list...
import re, collections
import os
from datetime import *


file_re = re.compile("Schedule_([0-9]{4})")
date_re = re.compile("([A-Za-z]+) ([0-9]+)")
night_game_re = re.compile("([A-Z]+) at ([A-Z]+)\*")
day_game_re = re.compile("([A-Z]+) at ([A-Z]+)")

this_year = 0
score_weights = collections.OrderedDict()

weekend_days = [5, 6]

def text_file_to_list(full_path):
    with open(full_path, 'r') as file:
        build_weights(full_path)
        schedule_list = [line.strip() for line in file.readlines()]
        return schedule_list

# the weights (that drive scores) for various things...
def build_weights(full_path):
    global this_year, score_weights
    fname = os.path.basename(full_path);
    m = file_re.match(fname)
    if not m:
        raise NameError("File name of schedule file needs to be Schedule_YYYY.txt")
    this_year = int(m.group(1))

    score_weights["earliest_date"] = date(this_year, 2, 1)
    score_weights["latest_date"] = date(this_year, 3, 31)
    score_weights["base_game_score"] = 10
    score_weights["home_bonus"] = {"SF": 25, "CHC": 25, "OAK": 10, "LAA": 10, "MIL": 10, "COL": 8, "AZ": 8}
    score_weights["visitor_bonus"] = {"SF": 15, "CHC": 15}
    score_weights["game_weights"] = [0.6, 0.3, 0.1]
    score_weights["st_patricks_day"] = {date(2017, 3, 17): 5}
    score_weights["night_game_penalty"] = -15
    score_weights["split_squad_penalty"] = -13
    score_weights["not_a_weekend_penalty"] = -25


# reads/parses the text schedule file
def schedule_parser(schedule_list):
    global this_year, score_weights
    schedule = []
    days = []
    todays_games = None

    for s in schedule_list:
        m = date_re.match(s)
        if m:
            todays_date = datetime.strptime(str(this_year) + " "+ m.group(0), "%Y %B %d").date()
            if todays_date >= score_weights["earliest_date"] and todays_date <= score_weights["latest_date"]:
                days.append(todays_date)
                if todays_games:
                    check_split_squad(todays_games)
                    schedule.append(todays_games)
                todays_games = {"date" : todays_date, "games":[]}

        if todays_games:
            m = night_game_re.match(s)
            if m:
                todays_games["games"].append({"home":m.group(2), "visitor": m.group(1), "day_game": False})
                continue

            m = day_game_re.match(s)
            if m:
                todays_games["games"].append({"home":m.group(2), "visitor": m.group(1), "day_game": True})
                continue

    # append last day...
    if todays_games:
        check_split_squad(todays_games)
        schedule.append(todays_games)

    return schedule, days

def check_split_squad(todays_games):
    # mark split squad
    if todays_games:
        teams = [g["visitor"] for g in todays_games["games"]]
        teams += [g["home"] for g in todays_games["games"]]

        for g in todays_games["games"]:
            g["split_squad"] = teams.count(g['home']) > 1 or teams.count(g['visitor']) > 1

# scores each game and each day.
def score_schedule(schedule, days, length_of_stay):
    for s in schedule:
        # all teams playing that day...
        teams = [g["visitor"] for g in s["games"]]
        teams += [g["home"] for g in s["games"]]

        for g in s["games"]:
            score = score_weights["base_game_score"]
            if not g["day_game"]:
                score += score_weights["night_game_penalty"]
            if g['home'] in score_weights["home_bonus"]:
                score += score_weights["home_bonus"][g['home']]
            if g['visitor'] in score_weights["visitor_bonus"]:
                score += score_weights["visitor_bonus"][g['visitor']]

            # split squad game!
            if g["split_squad"]:
                score += score_weights["split_squad_penalty"]

            g["score"] = score

        s["games"] = sorted(s["games"], key=lambda day: -day["score"])  # sort by age

        if len(s["games"]) > 0:
            top_3 = [g["score"] for g in s["games"][:3]]
            top_3 += [0 for i in range(3 - len(top_3))]
            top_3_weighted = [t[0] * t[1] for t in zip(top_3, score_weights["game_weights"])]
            s["score"] = sum(top_3_weighted)
        else:
            s["score"] = 0

        if s["date"] in score_weights["st_patricks_day"]:
            s["score"] += score_weights["st_patricks_day"][s["date"]]

    # now also score date ranges
    agendas = []
    for i in range(0, len(days)-length_of_stay):
        date_range = days[i: i + length_of_stay]
        dates = [s for s in schedule if s["date"] in date_range]
        tot_score = sum([s['score'] for s in dates])
        wds = [d for d in date_range if d.weekday() in weekend_days]
        if len(wds) < 2:
            tot_score += score_weights["not_a_weekend_penalty"]
        agendas.append((date_range, tot_score))

    return schedule, agendas

def sort_agenda_by_score(agenda):
    sorted_agenda = sorted(agenda, key=lambda day: -day[1])  # sort by age
    return sorted_agenda

def sort_agenda_by_date(agenda):
    sorted_agenda = sorted(agenda, key=lambda day: day[0][0])  # sort by age
    return sorted_agenda

def date_to_string(dt):
   return dt.strftime('%A, %b %d')

def get_score_weights():
    return score_weights

def get_scoring():
    out = []
    for k, v in score_weights.items():
        out.append("{0} = {1}".format(k, v))
    return out

def get_score_days(schedule):
    out = []
    for s in schedule:
        dt = s["date"]
        out.append("{0} ==> {1:.1f} points".format(date_to_string(dt), s["score"]))
        for g in s["games"]:
            str = "&nbsp;&nbsp;&nbsp;&nbsp;{0} at {1} ==> {2:.1f} points".format(g["visitor"], g["home"], g["score"])
            if not g["day_game"]:
                str = str + "&nbsp;(night)"
            if g["split_squad"]:
                str = str + "&nbsp;(split)"
            out.append(str)
    return out

def get_schedule(agenda, schedule, detail = True):
    out = []
    for weekend in agenda:
        out.append("{0} thru {1} ==> {2:.1f} points".format(date_to_string(weekend[0][0]),
                                                       date_to_string(weekend[0][-1]),
                                                       weekend[1]))
        if detail:
            weekend_dates = [s for s in schedule if s["date"] in weekend[0]]
            for s in weekend_dates:
                dt = s["date"]
                out.append("&nbsp;&nbsp;&nbsp;&nbsp;{0} ==> {1:.1f} points".format(date_to_string(dt), s["score"]))
                for g in s["games"]:
                    str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0} at {1} ==> {2:.1f} points".format(g["visitor"], g["home"], g["score"])
                    if not g["day_game"]:
                        str = str + "&nbsp;(night)"
                    if g["split_squad"]:
                        str = str + "&nbsp;(split)"
                    out.append(str)
            out.append("")
    return out

def print_scoring():
    print("")
    print("----------------------------------------------------------------------")
    print("Scoring Factors...")
    for k, v in score_weights.items():
        print("   {0} = {1}".format(k, v))
    print("----------------------------------------------------------------------")
    print("")

def print_schedule(agenda, schedule, detail = True):

    for weekend in agenda:
        print("{0} thru {1} ==> {2:.1f} points".format(date_to_string(weekend[0][0]),
                                                       date_to_string(weekend[0][-1]),
                                                       weekend[1]))
        if detail:
            weekend_dates = [s for s in schedule if s["date"] in weekend[0]]
            for s in weekend_dates:
                dt = s["date"]
                print("   {0} ==> {1:.1f} points".format(date_to_string(dt), s["score"]))
                for g in s["games"]:
                    str = "      {0} at {1} ==> {2:.1f} points".format(g["visitor"], g["home"], g["score"])
                    if not g["day_game"]:
                        str = str + " (night)"
                    if g["split_squad"]:
                        str = str + " (split)"
                    print(str)
            print("")
    print("----------------------------------------------------------------------")
    print("")
    print("")







