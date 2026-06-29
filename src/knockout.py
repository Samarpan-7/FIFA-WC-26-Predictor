from src.predictor import predict_match
import random


def play_round(teams):

    winners = []
    teams = teams[:]

    # If odd number, give bye
    if len(teams) % 2 == 1:
        bye_team = random.choice(teams)
        winners.append(bye_team)
        teams.remove(bye_team)

    for i in range(0, len(teams), 2):

        team1 = teams[i]
        team2 = teams[i + 1]

        winner, _ = predict_match(team1, team2)

        if winner == "Draw":
            winner = random.choice([team1, team2])

        winners.append(winner)

    return winners


def simulate_knockout(teams):

    round_teams = teams[:]

    while len(round_teams) > 1:
        round_teams = play_round(round_teams)

    return round_teams[0]