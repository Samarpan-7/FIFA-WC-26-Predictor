import random

def create_groups(teams):

    random.shuffle(teams)

    groups = {}

    teams_per_group = 4
    total_groups = len(teams) // 4

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    index = 0

    for i in range(total_groups):

        group_name = f"Group {letters[i]}"

        groups[group_name] = teams[index:index+4]

        index += 4

    return groups