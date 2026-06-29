from src.predictor import predict_match

def create_table(teams):
    table = {}

    for team in teams:
        table[team] = {
            "Played": 0,
            "Wins": 0,
            "Draws": 0,
            "Losses": 0,
            "Points": 0
        }

    return table


def simulate_group(group_teams):
    table = create_table(group_teams)

    for i in range(len(group_teams)):
        for j in range(i + 1, len(group_teams)):

            team1 = group_teams[i]
            team2 = group_teams[j]

            winner, _ = predict_match(team1, team2)

            table[team1]["Played"] += 1
            table[team2]["Played"] += 1

            if winner == team1:
                table[team1]["Wins"] += 1
                table[team2]["Losses"] += 1
                table[team1]["Points"] += 3

            elif winner == team2:
                table[team2]["Wins"] += 1
                table[team1]["Losses"] += 1
                table[team2]["Points"] += 3

            else:
                table[team1]["Draws"] += 1
                table[team2]["Draws"] += 1
                table[team1]["Points"] += 1
                table[team2]["Points"] += 1

    sorted_table = sorted(
        table.items(),
        key=lambda x: x[1]["Points"],
        reverse=True
    )

    return sorted_table