"""
Performance-based match predictor for FIFA WC'26 Predictor.
Uses XGBoost ML model. For unknown teams, falls back to
deterministic Elo-based ranking — NO random outcomes.
"""
import joblib
from src.data import get_team_info

model, le = joblib.load("models/match_model.pkl")
known_teams = set(le.classes_)


def predict_match(team1: str, team2: str):
    """
    Predict a match outcome between two teams.

    Returns (winner, [prob_home, prob_draw, prob_away]).
    Winner is decided deterministically by the highest probability.
    If both teams are known to the model, the ML model decides.
    If one or both are unknown, falls back to Elo-based comparison.
    """
    # ── ML model path (both teams in training set) ───────────────────
    if team1 in known_teams and team2 in known_teams:
        a = le.transform([team1])[0]
        b = le.transform([team2])[0]
        prob = model.predict_proba([[a, b]])[0]

        # Model classes: [0=away_win, 1=draw, 2=home_win]
        p_home = float(prob[2])
        p_draw = float(prob[1])
        p_away = float(prob[0])

        # Deterministic: pick highest probability class
        best = max(p_home, p_draw, p_away)
        if best == p_home:
            winner = team1
        elif best == p_away:
            winner = team2
        else:
            winner = "Draw"

        return winner, [p_home, p_draw, p_away]

    # ── Elo-based deterministic fallback ─────────────────────────────
    info1 = get_team_info(team1)
    info2 = get_team_info(team2)

    elo1 = info1.get("elo", 1500)
    elo2 = info2.get("elo", 1500)
    rank1 = info1.get("fifa_rank", 50)
    rank2 = info2.get("fifa_rank", 50)
    str1 = info1.get("strength", 70)
    str2 = info2.get("strength", 70)

    # Composite score: Elo (60%), FIFA rank (20%), strength (20%)
    score1 = (elo1 / 2200) * 60 + ((100 - rank1) / 100) * 20 + (str1 / 100) * 20
    score2 = (elo2 / 2200) * 60 + ((100 - rank2) / 100) * 20 + (str2 / 100) * 20

    diff = score1 - score2
    total = score1 + score2

    if total == 0:
        p_home, p_away, p_draw = 0.40, 0.35, 0.25
    else:
        p_home = round(score1 / total * 0.75 + 0.10, 4)  # max 85%
        p_away = round(score2 / total * 0.75 + 0.10, 4)
        p_draw = round(max(0.05, 1.0 - p_home - p_away), 4)
        # renormalise
        s = p_home + p_draw + p_away
        p_home /= s; p_draw /= s; p_away /= s

    # Deterministic decision
    if abs(diff) < 2.0:          # very close → draw
        winner = "Draw"
    elif score1 > score2:
        winner = team1
    else:
        winner = team2

    return winner, [p_home, p_draw, p_away]