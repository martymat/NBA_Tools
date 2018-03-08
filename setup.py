from flask import Flask, render_template, request
from operator import itemgetter
from nba_py import player, team

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/five", methods=["POST"])
def five():

    quarter = request.form["Quarter"]
    opponent = request.form["Opponent"]
    last = request.form["Last"]
    location = request.form["Location"]
    time = request.form["Time"]
    point_diff = request.form["Point_Diff"]

    intime = int(time)

    if intime >= 10:
        mins_or_secs = "SECONDS"
    else:
        mins_or_secs = "MINUTE(S)"
    str_time = str(intime)

    best_six = choose_best_six(quarter, time, point_diff, last, opponent, location)

    return render_template("five.html",
                           best_six=best_six,
                           quarter=quarter,
                           last=last,
                           opponent=opponent,
                           location=location,
                           mins_or_secs=mins_or_secs,
                           str_time=str_time,
                           point_diff=point_diff)


def get_all_nets_players_info():
    player_info = {}
    players = []

    # GETTING INFO ABOUT NETS ROSTER
    nets_team = team.TeamCommonRoster('1610612751', '2017-18').roster()

    for info in nets_team:
        player_info["PLAYER_NAME"] = info["PLAYER"]
        player_info["PLAYER_NUM"] = info["NUM"]
        player_info["PLAYER_POSITION"] = info["POSITION"]
        player_info["PLAYER_HEIGHT"] = info["HEIGHT"]
        player_info["PLAYER_WEIGHT"] = info["WEIGHT"]
        player_info["PLAYER_AGE"] = info["AGE"]
        player_info["PLAYER_SCHOOL"] = info["SCHOOL"]
        player_info["PLAYER_ID"] = info["PLAYER_ID"]
        player_info["PLAYER_PHOTO"] = img_getter(info["PLAYER_ID"])

        player_info["2018_PLUS_MINUS"] = nets_player_plus_minus_by_year(info["PLAYER_ID"])

        player_info["1Q_PLUS_MINUS"] = nets_player_plus_minus_by_period(info["PLAYER_ID"], 1)
        player_info["2Q_PLUS_MINUS"] = nets_player_plus_minus_by_period(info["PLAYER_ID"], 2)
        player_info["3Q_PLUS_MINUS"] = nets_player_plus_minus_by_period(info["PLAYER_ID"], 3)
        player_info["4Q_PLUS_MINUS"] = nets_player_plus_minus_by_period(info["PLAYER_ID"], 4)

        player_info["5_5DOWN_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 5, -5)
        player_info["3_5DOWN_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 3, -5)
        player_info["1_5DOWN_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 1, -5)
        player_info["30_3DOWN_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], .3, -3)
        player_info["10_3DOWN_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], .1, -3)
        player_info["5_5UP_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 5, 5)
        player_info["3_5UP_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 3, 5)
        player_info["1_5UP_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], 1, 5)
        player_info["30_5UP_PLUS_MINUS"] = nets_player_plus_minus_by_crunchtime(info["PLAYER_ID"], .3, 5)

        player_info["LAST_5_PLUS_MINUS"] = nets_player_plus_minus_by_previous_games(info["PLAYER_ID"], 5)
        player_info["LAST_10_PLUS_MINUS"] = nets_player_plus_minus_by_previous_games(info["PLAYER_ID"], 10)
        player_info["LAST_15_PLUS_MINUS"] = nets_player_plus_minus_by_previous_games(info["PLAYER_ID"], 15)

        player_info["HOME_PLUS_MINUS"] = nets_player_plus_location(info["PLAYER_ID"], "Home")
        player_info["AWAY_PLUS_MINUS"] = nets_player_plus_location(info["PLAYER_ID"], "Road")

        player_info["VS_HAWKS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Atlanta Hawks")
        player_info["VS_CELTICS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Boston Celtics")
        player_info["VS_HORNETS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Charlotte Hornets")
        player_info["VS_BULLS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Chicago Bulls")
        player_info["VS_CAVALIERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Cleveland Cavaliers")
        player_info["VS_MAVERICKS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Dallas Mavericks")
        player_info["VS_NUGGETS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Denver Nuggets")
        player_info["VS_PISTONS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Detroit Pistons")
        player_info["VS_WARRIORS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Golden State Warriors")
        player_info["VS_ROCKETS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Houston Rockets")
        player_info["VS_PACERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Indiana Pacers")
        player_info["VS_CLIPPERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "LA Clippers")
        player_info["VS_LAKERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Los Angeles Lakers")
        player_info["VS_GRIZZLIES_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Memphis Grizzlies")
        player_info["VS_HEAT_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Miami Heat")
        player_info["VS_BUCKS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Milwaukee Bucks")
        player_info["VS_TIMBERWOLVES_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Minnesota Timberwolves")
        player_info["VS_PELICANS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "New Orleans Pelicans")
        player_info["VS_KNICKS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "New York Knicks")
        player_info["VS_THUNDER_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Oklahoma City Thunder")
        player_info["VS_MAGIC_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Orlando Magic")
        player_info["VS_76ERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Philadelphia 76ers")
        player_info["VS_SUNS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Phoenix Suns")
        player_info["VS_TRAIL_BLAZERS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Portland Trail Blazers")
        player_info["VS_KINGS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Sacramento Kings")
        player_info["VS_SPURS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "San Antonio Spurs")
        player_info["VS_RAPTORS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Toronto Raptors")
        player_info["VS_JAZZ_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Utah Jazz")
        player_info["VS_WIZARDS_PLUS_MINUS"] = nets_player_plus_minus_by_opponent(info["PLAYER_ID"], "Washington Wizards")

        players.append(player_info)
        player_info = {}

    return players


def nets_player_plus_minus_by_year(player_id):
    id = player_id
    player_year_info = player.PlayerYearOverYearSplits(id).by_year()
    plus_minus = "N/A"
    for info in player_year_info:
        if info["GROUP_VALUE"] == "2017-18":
            plus_minus = info["PLUS_MINUS"]
        else:
            continue

    return plus_minus


def nets_player_plus_minus_by_period(player_id, period):
    id = player_id
    player_period_info = player.PlayerInGameSplits(id).by_period()

    plus_minus = "N/A"
    for info in player_period_info:
        if info["GROUP_VALUE"] == period:
            plus_minus = info["PLUS_MINUS"]
        else:
            continue

    return plus_minus

def nets_player_plus_minus_by_crunchtime(player_id, time_left, score):
    id = player_id
    plus_minus = "N/A"

    if time_left == 0 and score == 0:
        plus_minus = 0
    elif time_left == 5 and score == -5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last5min_deficit_5point()
    elif time_left == 3 and score == -5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last3min_deficit_5point()
    elif time_left == 1 and score == -5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last1min_deficit_5point()
    elif time_left == .3 and score == -3:
        player_crunchtime_info = player.PlayerClutchSplits(id).last30sec_deficit_3point()
    elif time_left == .1 and score == -3:
        player_crunchtime_info = player.PlayerClutchSplits(id).last10sec_deficit_3point()
    elif time_left == 5 and score == 5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last5min_deficit_5point()
    elif time_left == 3 and score == 5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last3min_plusminus_5point()
    elif time_left == 1 and score == 5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last1min_plusminus_5point()
    elif time_left == .3 and score == 5:
        player_crunchtime_info = player.PlayerClutchSplits(id).last30sec_plusminus_5point()

    for info in player_crunchtime_info:
        plus_minus = info["PLUS_MINUS"]

    return plus_minus


def nets_player_plus_minus_by_previous_games(player_id, num_of_games):
    id = player_id
    if num_of_games == 5:
        player_previous_games_info = player.PlayerLastNGamesSplits(id).last5()
    elif num_of_games == 10:
        player_previous_games_info = player.PlayerLastNGamesSplits(id).last10()
    elif num_of_games == 15:
        player_previous_games_info = player.PlayerLastNGamesSplits(id).last15()

    plus_minus = "N/A"
    for info in player_previous_games_info:
        if info["GROUP_VALUE"] == "2017-18" and info["GROUP_SET"] == "Last " + str(num_of_games) + " Games":
            plus_minus = info["PLUS_MINUS"]
        else:
            continue

    return plus_minus


def nets_player_plus_minus_by_opponent(player_id, team_name):
    id = player_id
    player_previous_games_info = player.PlayerOpponentSplits(id).by_opponent()

    plus_minus = "N/A"
    for info in player_previous_games_info:
        if info["GROUP_VALUE"] == team_name:
            plus_minus = info["PLUS_MINUS"]
        else:
            continue

    return plus_minus


def nets_player_plus_location(player_id, location):
    id = player_id
    player_location_info = player.PlayerGeneralSplits(id).location()

    plus_minus = "N/A"
    for info in player_location_info:
        if info["GROUP_VALUE"] == location:
            plus_minus = info["PLUS_MINUS"]
        else:
            continue

    return plus_minus


def calculate_weighted_plus_minus(yearly, quarterly, lastly, opponently, locationly, clutchtime):
    if yearly == "N/A":
        floated_yearly = 0
    else:
        floated_yearly = float(yearly)

    if quarterly == "N/A":
        floated_quarterly = 0
    else:
        floated_quarterly = float(quarterly)

    if lastly == "N/A":
        floated_lastly = 0
    else:
        floated_lastly = float(lastly)

    if opponently == "N/A":
        floated_opponently = 0
    else:
        floated_opponently = float(opponently)

    if locationly == "N/A":
        floated_locationly = 0
    else:
        floated_locationly= float(locationly)

    if locationly == "N/A":
        floated_clutchtime = 0
    else:
        floated_clutchtime = float(clutchtime)

    if clutchtime == 0:
        weighted_plus_minus = ((floated_yearly * 0.4) + (floated_quarterly * 0.1) + (floated_opponently * 0.2)
                               + (floated_locationly * 0.2) + (floated_lastly * .1)) / 5
    else:
        weighted_plus_minus = ((floated_yearly * 0.3) + (floated_quarterly * 0.15) + (floated_clutchtime * 0.2)
                               + (floated_opponently * 0.1) + (floated_locationly * 0.15) + (floated_lastly * 0.1)) / 6

    rounded = round(weighted_plus_minus, 2)

    return rounded


def choose_best_six(quarter, time, point_diff, last, opponent, location):
    reg_time = time
    int_time = int(time)
    if int_time == 0:
        fourth_quarter = False
    elif int_time > 0:
        fourth_quarter = True

    nets_players = get_all_nets_players_info()
    intPoints = int(point_diff)
    if intPoints < 0:
        behind = True
    else:
        behind = False

    calculations = {}
    calculated = []

    abs_points = abs(intPoints)
    string_abs_points = str(abs_points)

    if behind and not fourth_quarter:
        for players in nets_players:
            calculations["CALC_PLUS_MINUS"] = \
                calculate_weighted_plus_minus(players["2018_PLUS_MINUS"],
                                              players[quarter + "Q_PLUS_MINUS"],
                                              players["LAST_" + last + "_PLUS_MINUS"],
                                              players["VS_" + opponent + "_PLUS_MINUS"],
                                              players[location + "_PLUS_MINUS"],
                                              int_time)

            calculations["PLAYER_NAME"] = players["PLAYER_NAME"]
            calculations["PLAYER_PHOTO"] = players["PLAYER_PHOTO"]
            calculations["YEAR_PLUS_MINUS"] = players["2018_PLUS_MINUS"]
            calculations["QUARTER_PLUS_MINUS"] = players[quarter + "Q_PLUS_MINUS"]
            calculations["LAST_GAMES_PLUS_MINUS"] = players["LAST_" + last + "_PLUS_MINUS"]
            calculations["OPPONENT_PLUS_MINUS"] = players["VS_" + opponent + "_PLUS_MINUS"]
            calculations["LOCATION_PLUS_MINUS"] = players[location + "_PLUS_MINUS"]
            calculated.append(calculations)
            calculations = {}
    elif not behind and not fourth_quarter:
        for players in nets_players:
            calculations["CALC_PLUS_MINUS"] = \
                calculate_weighted_plus_minus(players["2018_PLUS_MINUS"],
                                            players[quarter + "Q_PLUS_MINUS"],
                                            players["LAST_" + last + "_PLUS_MINUS"],
                                            players["VS_" + opponent + "_PLUS_MINUS"],
                                            players[location + "_PLUS_MINUS"],
                                            int_time)

            calculations["PLAYER_NAME"] = players["PLAYER_NAME"]
            calculations["PLAYER_PHOTO"] = players["PLAYER_PHOTO"]
            calculations["YEAR_PLUS_MINUS"] = players["2018_PLUS_MINUS"]
            calculations["QUARTER_PLUS_MINUS"] = players[quarter + "Q_PLUS_MINUS"]
            calculations["LAST_GAMES_PLUS_MINUS"] = players["LAST_" + last + "_PLUS_MINUS"]
            calculations["OPPONENT_PLUS_MINUS"] = players["VS_" + opponent + "_PLUS_MINUS"]
            calculations["LOCATION_PLUS_MINUS"] = players[location + "_PLUS_MINUS"]
            calculated.append(calculations)
            calculations = {}
    elif behind and fourth_quarter:
        for players in nets_players:
            calculations["CALC_PLUS_MINUS"] = \
                calculate_weighted_plus_minus(players["2018_PLUS_MINUS"],
                                            players[quarter + "Q_PLUS_MINUS"],
                                            players["LAST_" + last + "_PLUS_MINUS"],
                                            players["VS_" + opponent + "_PLUS_MINUS"],
                                            players[location + "_PLUS_MINUS"],
                                            players[str(time) + "_" + string_abs_points + "DOWN_PLUS_MINUS"])

            calculations["PLAYER_NAME"] = players["PLAYER_NAME"]
            calculations["PLAYER_PHOTO"] = players["PLAYER_PHOTO"]
            calculations["YEAR_PLUS_MINUS"] = players["2018_PLUS_MINUS"]
            calculations["QUARTER_PLUS_MINUS"] = players[quarter + "Q_PLUS_MINUS"]
            calculations["LAST_GAMES_PLUS_MINUS"] = players["LAST_" + last + "_PLUS_MINUS"]
            calculations["OPPONENT_PLUS_MINUS"] = players["VS_" + opponent + "_PLUS_MINUS"]
            calculations["LOCATION_PLUS_MINUS"] = players[location + "_PLUS_MINUS"]
            calculations["CLUTCH_PLUS_MINUS"] = players[str(time) + "_" + string_abs_points + "DOWN_PLUS_MINUS"]
            calculated.append(calculations)
            calculations = {}

    elif not behind and fourth_quarter:
        for players in nets_players:
            calculations["CALC_PLUS_MINUS"] = \
                calculate_weighted_plus_minus(players["2018_PLUS_MINUS"],
                                              players[quarter + "Q_PLUS_MINUS"],
                                              players["LAST_" + last + "_PLUS_MINUS"],
                                              players["VS_" + opponent + "_PLUS_MINUS"],
                                              players[location + "_PLUS_MINUS"],
                                              players[str(time) + "_" + string_abs_points + "UP_PLUS_MINUS"])

            calculations["PLAYER_NAME"] = players["PLAYER_NAME"]
            calculations["PLAYER_PHOTO"] = players["PLAYER_PHOTO"]
            calculations["YEAR_PLUS_MINUS"] = players["2018_PLUS_MINUS"]
            calculations["QUARTER_PLUS_MINUS"] = players[quarter + "Q_PLUS_MINUS"]
            calculations["LAST_GAMES_PLUS_MINUS"] = players["LAST_" + last + "_PLUS_MINUS"]
            calculations["OPPONENT_PLUS_MINUS"] = players["VS_" + opponent + "_PLUS_MINUS"]
            calculations["LOCATION_PLUS_MINUS"] = players[location + "_PLUS_MINUS"]
            calculations["CLUTCH_PLUS_MINUS"] = players[str(time) + "_" + string_abs_points + "UP_PLUS_MINUS"]
            calculated.append(calculations)
            calculations = {}

    sorted_calculations = sorted(calculated, key=itemgetter('CALC_PLUS_MINUS'), reverse=True)

    return sorted_calculations[0:6]


def img_getter(id):
    url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + str(id) + ".png"

    return url

if __name__ == "__main__":
    app.run(debug=True)