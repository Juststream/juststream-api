import requests
from fastapi import APIRouter

router = APIRouter(
    prefix='/livescore'
)


def get_players_from_team(team):
    players = []
    for player in team['Ps']:
        if player.get('Pon') == 'COACH':
            continue
        players.append(
            {
                'name': player['Snm'],
                'shirt_number': player['Snu']
            }
        )
    return players


@router.get('/match/{match_id}')
def get_match_details(match_id: str):
    response = requests.get(
        f'https://www.livescore.com/_next/data/dl1aBUxUep6IgIw9DWru5/en/football/_/_/_/{match_id}.json')
    match_data = response.json()['pageProps']['initialData']
    current_time_raw = match_data.get('Eps')
    current_time = int(current_time_raw.rstrip("'")) if current_time_raw[0].isdigit() else None
    line_ups = match_data['Lu']
    return {
        'home_team': {
            'team_name': match_data['T1'][0]['Nm'],
            'players': get_players_from_team(line_ups[0]),
            'score': match_data.get('Tr1')
        },
        'away_team': {
            'team_name': match_data['T2'][0]['Nm'],
            'players': get_players_from_team(line_ups[1]),
            'score': match_data.get('Tr2')
        },
        'current_time': current_time
    }
