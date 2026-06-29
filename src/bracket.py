"""
Bracket simulation engine for FIFA Oracle 2026.

Wraps the existing predict_match() from src.predictor with:
  - Realistic scoreline generation
  - xG estimates
  - Win-probability display values
  - AI explanation factors
  - Full group-stage and knockout-bracket simulation
"""

import math
from src.predictor import predict_match
from src.data import get_team_info


# ─────────────────────────────────────────────────────────────────────────────
# SINGLE MATCH
# ─────────────────────────────────────────────────────────────────────────────

def simulate_match_detail(team1: str, team2: str, is_knockout: bool = False) -> dict:
    """
    Simulate one match via the ML model and return a rich result dict.

    Args:
        team1:       First / home team.
        team2:       Second / away team.
        is_knockout: When True, draws are resolved to a definite winner.

    Returns:
        {team1, team2, winner, loser, score, prob_t1, prob_draw, prob_t2,
         confidence, xg1, xg2, factors}
    """
    winner, prob = predict_match(team1, team2)

    prob_t1, prob_draw, prob_t2 = _parse_probabilities(prob)

    # Knockout: no draws allowed
    if is_knockout and winner == "Draw":
        winner = team1 if prob_t1 >= prob_t2 else team2

    score = _generate_score(team1, team2, winner)
    xg1, xg2 = _estimate_xg(team1, team2)

    gap = abs(prob_t1 - prob_t2)
    confidence = "High" if gap > 28 else ("Medium" if gap > 12 else "Low")

    info1 = get_team_info(team1)
    info2 = get_team_info(team2)
    factors = _build_factors(team1, team2, winner, info1, info2)

    loser = "Draw" if winner == "Draw" else (team2 if winner == team1 else team1)

    return {
        "team1":      team1,
        "team2":      team2,
        "winner":     winner,
        "loser":      loser,
        "score":      score,
        "prob_t1":    round(prob_t1, 1),
        "prob_draw":  round(prob_draw, 1),
        "prob_t2":    round(prob_t2, 1),
        "confidence": confidence,
        "xg1":        xg1,
        "xg2":        xg2,
        "factors":    factors,
    }


# ─────────────────────────────────────────────────────────────────────────────
# GROUP STAGE
# ─────────────────────────────────────────────────────────────────────────────

def simulate_group_stage(group_teams: list[str]) -> tuple[list, list]:
    """
    Run full round-robin for a group of 4 teams.

    Returns:
        sorted_table : [(team_name, stats_dict), ...] sorted by Pts, GD, GF
        match_results: [match_detail_dict, ...]
    """
    table: dict[str, dict] = {
        t: {"P": 0, "W": 0, "D": 0, "L": 0,
            "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
        for t in group_teams
    }
    matches: list[dict] = []

    for i in range(len(group_teams)):
        for j in range(i + 1, len(group_teams)):
            t1, t2 = group_teams[i], group_teams[j]
            result = simulate_match_detail(t1, t2, is_knockout=False)
            matches.append(result)

            g1, g2 = map(int, result["score"].split("-"))

            table[t1]["P"] += 1
            table[t2]["P"] += 1
            table[t1]["GF"] += g1
            table[t1]["GA"] += g2
            table[t2]["GF"] += g2
            table[t2]["GA"] += g1

            w = result["winner"]
            if w == t1:
                table[t1]["W"] += 1
                table[t1]["Pts"] += 3
                table[t2]["L"] += 1
            elif w == t2:
                table[t2]["W"] += 1
                table[t2]["Pts"] += 3
                table[t1]["L"] += 1
            else:
                table[t1]["D"] += 1
                table[t1]["Pts"] += 1
                table[t2]["D"] += 1
                table[t2]["Pts"] += 1

    for t in group_teams:
        table[t]["GD"] = table[t]["GF"] - table[t]["GA"]

    sorted_table = sorted(
        table.items(),
        key=lambda x: (x[1]["Pts"], x[1]["GD"], x[1]["GF"]),
        reverse=True,
    )
    return sorted_table, matches


def get_qualified_32(group_results: dict) -> list[str]:
    """
    Determine the 32 knockout-stage qualifiers from 12 group results.

    Rules (mirrors actual WC 2026 format):
      - Top 2 from each of 12 groups → 24 teams
      - Best 8 third-place finishers  →  8 teams
      Total = 32 qualified teams

    Args:
        group_results: {group_name: (sorted_table, matches)}

    Returns:
        List of 32 team names (winners first, runners-up, then best thirds).
    """
    firsts, seconds, thirds = [], [], []

    for _, (table, _) in group_results.items():
        if len(table) >= 1:
            firsts.append((table[0][0], table[0][1]["Pts"], table[0][1]["GD"]))
        if len(table) >= 2:
            seconds.append((table[1][0], table[1][1]["Pts"], table[1][1]["GD"]))
        if len(table) >= 3:
            thirds.append((table[2][0], table[2][1]["Pts"], table[2][1]["GD"]))

    thirds.sort(key=lambda x: (x[1], x[2]), reverse=True)
    best_thirds = [t[0] for t in thirds[:8]]

    return [t[0] for t in firsts] + [t[0] for t in seconds] + best_thirds


# ─────────────────────────────────────────────────────────────────────────────
# KNOCKOUT ROUNDS
# ─────────────────────────────────────────────────────────────────────────────

def simulate_knockout_round(teams: list[str]) -> tuple[list[dict], list[str]]:
    """
    Simulate one knockout round; all matches produce a definite winner.

    Args:
        teams: Even-length list paired as (teams[0] vs teams[1]), (teams[2] vs teams[3]), …

    Returns:
        (match_results, winners)
    """
    results: list[dict] = []
    winners: list[str] = []

    pairs = list(zip(teams[::2], teams[1::2]))
    for t1, t2 in pairs:
        result = simulate_match_detail(t1, t2, is_knockout=True)
        results.append(result)
        winners.append(result["winner"])

    return results, winners


def simulate_full_bracket(teams_32: list[str]) -> dict:
    """
    Simulate the complete knockout tournament from Round of 32 to Champion.

    Args:
        teams_32: Ordered list of exactly 32 qualified teams.

    Returns:
        bracket dict:
          "Round of 32"   : [match_detail, ...]
          "Round of 16"   : [match_detail, ...]
          "Quarter Finals": [match_detail, ...]
          "Semi Finals"   : [match_detail, ...]
          "3rd Place"     : [match_detail]
          "Final"         : [match_detail]
          "Champion"      : str
    """
    bracket: dict = {}
    current = list(teams_32[:32])

    r32, r16_teams = simulate_knockout_round(current)
    bracket["Round of 32"] = r32

    r16, qf_teams = simulate_knockout_round(r16_teams)
    bracket["Round of 16"] = r16

    qf, sf_teams = simulate_knockout_round(qf_teams)
    bracket["Quarter Finals"] = qf

    sf, finalists = simulate_knockout_round(sf_teams)
    bracket["Semi Finals"] = sf
    sf_losers = [r["loser"] for r in sf if r["loser"] not in (None, "Draw")]

    if len(sf_losers) >= 2:
        third = simulate_match_detail(sf_losers[0], sf_losers[1], is_knockout=True)
        bracket["3rd Place"] = [third]

    if len(finalists) >= 2:
        final = simulate_match_detail(finalists[0], finalists[1], is_knockout=True)
        bracket["Final"] = [final]
        bracket["Champion"] = final["winner"]
    elif finalists:
        bracket["Champion"] = finalists[0]

    return bracket


# ─────────────────────────────────────────────────────────────────────────────
# PRIVATE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _parse_probabilities(prob) -> tuple[float, float, float]:
    """
    Convert the raw probability array from predict_match() into
    (prob_team1 %, prob_draw %, prob_team2 %) ready for display.

    The trained model uses classes [0=away_win, 1=draw, 2=home_win], so
    predict_proba returns [P(away), P(draw), P(home)].
    The unknown-team fallback returns [0.45, 0.25, 0.30] meaning [home, draw, away].
    Both cases are normalised; we detect the model path by checking that prob[2]
    (home/team1 class) is in a sensible range and default safely.
    """
    try:
        p = [float(x) for x in prob]
        if len(p) == 3 and abs(sum(p) - 1.0) < 0.05:
            # Model output order: [P(away=0), P(draw=1), P(home=2)]
            return p[2] * 100, p[1] * 100, p[0] * 100
    except Exception:
        pass
    return 45.0, 25.0, 30.0


def _generate_score(team1: str, team2: str, winner: str) -> str:
    """
    Generate a realistic, performance-based scoreline.
    Goals are derived from attack vs defense ratings — no randomness.
    """
    i1 = get_team_info(team1)
    i2 = get_team_info(team2)

    # Attack vs opponent defense differential (0–100 scale)
    att1 = i1.get("attack", 70)
    att2 = i2.get("attack", 70)
    def1 = i1.get("defense", 70)
    def2 = i2.get("defense", 70)

    # Expected raw goals: attack advantage over opponent defense
    raw1 = max(0.0, (att1 - def2) / 20.0 + 1.2)
    raw2 = max(0.0, (att2 - def1) / 20.0 + 1.2)

    # Clamp to realistic range 0–4
    g1_f = min(4.0, raw1)
    g2_f = min(4.0, raw2)

    if winner == "Draw":
        # Both teams score the same — use the lower rounded value
        g = max(0, round((g1_f + g2_f) / 2) - 1)
        g = min(g, 2)
        return f"{g}-{g}"

    # Winner scores more; loser scores less
    if winner == team1:
        wg = max(1, round(g1_f))
        lg = max(0, round(g2_f) - 1)
    else:
        wg = max(1, round(g2_f))
        lg = max(0, round(g1_f) - 1)

    if lg >= wg:
        lg = wg - 1

    if winner == team1:
        return f"{wg}-{lg}"
    else:
        return f"{lg}-{wg}"


def _estimate_xg(team1: str, team2: str) -> tuple[float, float]:
    """Estimate xG from attack and defense ratings — no randomness."""
    a1 = get_team_info(team1).get("attack", 70)
    a2 = get_team_info(team2).get("attack", 70)
    d1 = get_team_info(team1).get("defense", 70)
    d2 = get_team_info(team2).get("defense", 70)
    xg1 = round(max(0.3, (a1 - d2) / 20.0 + 1.2), 1)
    xg2 = round(max(0.3, (a2 - d1) / 20.0 + 1.2), 1)
    return xg1, xg2


def _build_factors(team1: str, team2: str, winner: str,
                   info1: dict, info2: dict) -> list[str]:
    """Generate up to 3 plain-English AI explanation factors."""
    if winner == "Draw":
        return ["Evenly matched sides", "Similar form records", "Tactical balance expected"]

    wi = info1 if winner == team1 else info2
    li = info2 if winner == team1 else info1
    factors: list[str] = []

    if wi["fifa_rank"] < li["fifa_rank"]:
        factors.append(f"Higher FIFA ranking (#{wi['fifa_rank']})")
    if wi["elo"] > li["elo"]:
        factors.append(f"Superior Elo rating ({wi['elo']})")
    if wi["strength"] > li["strength"]:
        factors.append("Stronger overall squad")
    if wi["form"].count("W") > li["form"].count("W"):
        factors.append("Better recent form")
    if wi["attack"] > li["defense"] + 5:
        factors.append("Attacking edge over opponent's defense")
    if len(factors) < 2:
        factors.append("Higher model confidence score")

    return factors[:3]
