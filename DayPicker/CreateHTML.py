from colour import Color
from jinja2 import Template
from TextToList import *
import datetime
import math

color_steps = 20
colors = list(Color("#505050").range_to(Color("#00FF00"),color_steps))
def get_color(value, min, max):
    global color_steps, colors
    i = float(value - min) / (max - min) * color_steps
    i = math.floor(i)
    if(i > color_steps-1):
        i = color_steps-1
    if(i < 0):
        i = 0
    return colors[i].hex


def print_to_html(file, schedule, days, agenda):
    if 0:
        print_scoring()
        print("------------------- TOP SCORES -----------------------------------")
        agenda = sort_agenda_by_score(agenda)
        print_schedule(agenda, schedule, False)
        print("------------------- SCORES BY DATE -----------------------------------")
        agenda = sort_agenda_by_date(agenda)
        print_schedule(agenda, schedule, False)
        print("------------------- SCORING DETAIL -----------------------------------")
        agenda = sort_agenda_by_score(agenda)
        print_schedule(agenda, schedule, True)


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
            else:
                color = get_color(0, 22, 35)
            calendar_data.append({'day': date.strftime("%d"), 'color' : '"{}"'.format(color)})
            date += delta

        agenda = sort_agenda_by_score(agenda)
        top = get_schedule(agenda, schedule, False)
        dates = get_schedule(agenda, schedule, False)
        details = get_schedule(agenda, schedule, True)
        days = get_score_days(schedule)

        f = open("spring_training_report.html", "w")
        f.write(template.render(calendar_data=calendar_data, factors=factors, top = top, dates = dates, details = details, days = days, source_file = file))
        f.close()