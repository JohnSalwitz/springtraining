from colour import Color
from jinja2 import Template
from TextToList import *
import datetime
import math



colors = [Color("#FFFFFF"),Color("#E2F7E2"),Color("#E2F7E2"),Color("#E2F7E2"),Color("#C5F0C5"),Color("#A7E8A8"),Color("#8AE08B"),Color("#6DD86E"),Color("#50D151"),Color("#32C934"),Color("#15C117")]

def get_color(value, min, max):
    global colors
    color_steps = len(colors)
    i = float(value - min) / (max - min) * color_steps
    i = math.floor(i)
    if(i > color_steps-1):
        i = color_steps-1
    if(i < 0):
        i = 0
    return colors[i].hex

def get_score_day(s):
  out = ""
  for g in s["games"]:
    out = out + "{0} at {1} ==> {2:.1f} points".format(g["visitor"], g["home"], g["score"])
    if not g["day_game"]:
      out = out + "&nbsp;(night)"
    if g["split_squad"]:
      out = out + "&nbsp;(split)"
    out = out + "<br/>"
  return out

def get_scoring():
  out = []
  for k, v in score_weights.items():
    out.append("{0} = {1}".format(k, v))
  return out

def print_to_html(source_file, report_folder, schedule, agenda):
    with open('./templates/template.html') as file_:
        template = Template(file_.read())
        factors = get_scoring()
        weights = get_score_weights()

        month = weights["earliest_date"].month
        year = weights["earliest_date"].year

        first_day_of_month = datetime.date(year, month, 1).weekday()
        first_day_of_month = (first_day_of_month + 1) % 7   # make sunday 0

        calendar_data = []
        delta = datetime.timedelta(days=1)
        date = weights["earliest_date"]
        date -= datetime.timedelta(days=first_day_of_month)

        while date <= score_weights["latest_date"]:
            schd = next((s for s in schedule if s["date"] == date), None)
            if(schd != None):
                color = get_color(schd["score"], 22, 35)
                games = get_score_day(schd)
            else:
                color = get_color(0, 22, 35)
                games = "no games today"
            calendar_data.append({'day': date.strftime("%d"), 'color' : '"{}"'.format(color), 'games' : games})
            date += delta

        sorted_agenda = sort_agenda_by_score(agenda)
        dates = get_schedule(sorted_agenda, schedule, False)
        top = get_schedule(sorted_agenda, schedule, False)[:10]

        year = get_year_from_schedule_file(source_file)
        fname = 'spring_training_{}.html'.format(year)
        f = open(os.path.join(report_folder, fname), "w")
        f.write(template.render(year = year, calendar_data=calendar_data, factors=factors, top = top, dates = dates, source_file = source_file))
        f.close()
