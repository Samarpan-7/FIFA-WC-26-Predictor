from predictor import predict_match
import random

def simulate_tournament(teams):

    teams = teams[:]

    while len(teams) > 1:

        winners = []

        for i in range(0, len(teams), 2):

            winner, _ = predict_match(teams[i], teams[i+1])

            if winner == "Draw":
                winner = random.choice([teams[i], teams[i+1]])

            winners.append(winner)

        teams = winners

    return teams[0]