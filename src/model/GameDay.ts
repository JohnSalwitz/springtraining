import {TeamAbreviationType} from "./TeamData";
import Game from "./Game";

export interface IGameData {
    index: number,
    name: string,
    location: string,
    startDate: string,
    away: TeamAbreviationType,
    home: TeamAbreviationType,
}


export const SCORE_WEIGHTS = {
    "base_game_score" : 10,
    "home_bonus" : {"SF": 25, "CHC": 25, "MIL": 13, "OAK": 10, "LAA": 10, "COL": 8, "AZ": 8},
    "away_bonus" : {"SF": 15, "CHC": 15},
    "game_weights" : [0.4, 0.3, 0.2],
    "night_game_penalty" : -15,
    "split_squad_penalty" : -13,
    "not_a_weekend_penalty" : -15,
}

/*
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

 */


export default class GameDay {
    private _date: Date;
    private _schedule: Array<IGameData>;

    constructor(seasonSchedule: Array<IGameData>, date: Date) {
        this._date = date;
        this._schedule = seasonSchedule.filter(
            (r: IGameData) => new Date(r.startDate+"Z").toDateString() === date.toDateString());
    }

    get date() : Date {
        return this._date;
    }

    get isWeekend(): boolean {
        return this.date.getDay() === 0 || this.date.getDay() === 6;
    }

    /**
     * Returns sorted list of games on this day (sorted by score)
     */
    get games() : Array<Game> {
        let _games = this._schedule.map((r: IGameData) => {
            const awaySplitSquad =
                this._schedule.filter((r2: IGameData) => [r2.away, r2.home].includes(r.away)).length > 1;
            const homeSplitSquad =
                this._schedule.filter((r2: IGameData) => [r2.away, r2.home].includes(r.home)).length > 1;
            return new Game(r, awaySplitSquad, homeSplitSquad);
        });
        _games= _games.sort((a, b) => b.score-a.score);
        return _games;
    }

    get score() : number {
        let dayScores = this.games.map(g => g.score);

        // fill to 3
        dayScores = dayScores.fill(0, dayScores.length-1, 3-1);
        dayScores = dayScores.slice(0, 3);

        // sum of top 3 games (weighted)
        let score =  dayScores.reduce((a, b, inx) =>
            a + b * SCORE_WEIGHTS.game_weights[inx] , 0);

        // not a weekend penalty
        if (!this.isWeekend) {
            score += SCORE_WEIGHTS.not_a_weekend_penalty;
        }

        return Math.round(score);

    }

    toString() : string {
        return this.games.map(g => g.toString()).join("\n");
    }
}


