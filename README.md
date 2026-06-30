# FIFA WC'26 Predictor

**AI-Powered FIFA World Cup 2026 Prediction Platform**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fifa-wc-26-predictor.streamlit.app/)

> Live Demo → **[fifa-wc-26-predictor.streamlit.app](https://fifa-wc-26-predictor.streamlit.app/)**

---

## Overview

FIFA WC'26 Predictor simulates the complete FIFA World Cup 2026 — from Group Stage through to the Final — using an **XGBoost classifier** trained on 150+ years of international football results. Predictions are entirely performance-driven with no randomness involved.

---

## Features

- **Group Stage** — All 12 official groups, full round-robin simulation, live standings tables with rectangular flag images
- **Round of 32** — Complete knockout bracket: R32 → R16 → QF → SF → Final → Champion
- **Performance-Based Predictions** — Winner decided by the ML model's highest-probability class
- **Deterministic Scores** — Goals derived from attack vs defense ratings
- **Real Flag Images** — Rectangular country flags for all 48 teams via flagcdn.com
- **Tournament Journey** — Follow your chosen team's path through every round
- **AI Explanation** — Elo rating, FIFA rank, squad strength, and recent form factors

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.56 |
| ML Model | XGBoost Classifier |
| Historical Data | 150+ years of international matches |
| Flag Images | flagcdn.com CDN |
| Language | Python 3.11 |

---

## Project Structure

```
FIFA-WC-26/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies (pinned)
├── .streamlit/
│   └── config.toml         # Streamlit Cloud configuration
├── models/
│   └── match_model.pkl     # Trained XGBoost model
├── data/
│   └── matches.csv         # Historical match dataset
└── src/
    ├── data.py             # Team data, ISO codes, flag_img()
    ├── predictor.py        # Deterministic ML prediction engine
    ├── bracket.py          # Group stage & knockout simulation
    └── train.py            # Model training script
```

---

## Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Samarpan-7/FIFA-WC-26-Predictor.git
cd FIFA-WC-26-Predictor

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (first time only)
python src/train.py

# 5. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Official WC 2026 Groups

| Group | Teams |
|---|---|
| A | Mexico, South Africa, South Korea, Czechia |
| B | Switzerland, Canada, Bosnia & Herz, Qatar |
| C | Brazil, Morocco, Scotland, Haiti |
| D | United States, Australia, Paraguay, Türkiye |
| E | Germany, Côte d'Ivoire, Ecuador, Curaçao |
| F | Netherlands, Japan, Sweden, Tunisia |
| G | Belgium, Egypt, Iran, New Zealand |
| H | Spain, Cabo Verde, Uruguay, Saudi Arabia |
| I | France, Norway, Senegal, Iraq |
| J | Argentina, Austria, Algeria, Jordan |
| K | Colombia, Portugal, DR Congo, Uzbekistan |
| L | England, Croatia, Ghana, Panama |

---

## How Predictions Work

1. **ML Model** — XGBoost `predict_proba()` picks the highest-probability outcome (win / draw / loss). Fully deterministic.
2. **Elo Fallback** — For teams outside the training set, a composite of Elo (60%), FIFA rank (20%), and squad strength (20%) decides the winner.
3. **Scorelines** — Calculated from `(attack − opponent_defense) / 20 + 1.2`. No random number generation.

---

*Built with Python, Streamlit, and XGBoost.*
