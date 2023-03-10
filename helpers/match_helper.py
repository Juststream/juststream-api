def check_home_team(raw_home_team: str) -> bool:
    return raw_home_team.endswith("]") or raw_home_team[-1].isdigit()


def check_away_team(raw_away_team: str) -> bool:
    return raw_away_team.startswith("[") or raw_away_team[0].isdigit()


def generate_match_id(video_title: str) -> str or None:
    if not video_title:
        return None
    removed_spaces = video_title.replace(" ", "")
    dash_split = removed_spaces.split("-")
    if len(dash_split) < 2:
        return None
    raw_home_team = dash_split[0]
    raw_away_team = dash_split[1]
    if check_home_team(raw_home_team) and check_away_team(raw_away_team):
        raw_home_team_split = raw_home_team.split("[")
        if len(raw_home_team_split) > 1:
            home_team = raw_home_team_split[0]
        else:
            home_team = raw_home_team[:-1]
        raw_away_team_split = raw_away_team.split("]")
        if len(raw_away_team_split) > 1:
            away_team = raw_away_team_split[-1].split(":")[0].split("|")[0]
        else:
            away_team = raw_away_team[1:].split(":")[0].split("|")[0]
    else:
        return None

    return f"{home_team}-{away_team}".lower()
