# FIFA WC'26 Predictor

**AI-Powered FIFA World Cup 2026 Prediction Platform**

A production-ready Machine Learning web application that simulates the full FIFA World Cup 2026 — from Group Stage to the Final — using an XGBoost classifier trained on 150+ years of international football data.

---

## Features

- **Group Stage Simulation** — All 12 official groups with real-team data, round-robin matches, standings tables with rectangular flag images
- **Round of 32 Knockout Bracket** — Full bracket from R32 → R16 → QF → SF → Final → Champion
- **Performance-Based Predictions** — Winner decided by the ML model's highest-probability class (never random)
- **Deterministic Scores** — Goals generated from attack vs defense ratings
- **Real Flag Images** — Rectangular country flags via flagcdn.com CDN
- **Tournament Journey Tracker** — Follow your favourite team's path through every round
- **AI Explanation Factors** — Elo, FIFA rank, squad strength, recent form
- **Official-Style UI** — Georgia serif font, white background, clean professional layout

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.56 |
| ML Model | XGBoost Classifier |
| Data | 150+ years international match history |
| Flag Images | flagcdn.com CDN |
| Language | Python 3.10+ |

---

## Project Structure

```
FIFA-WC-26/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── models/
│   └── match_model.pkl  # Trained XGBoost model + label encoder
├── data/                # Historical match datasets
└── src/
    ├── data.py          # Team data, ISO codes, flag_img()
    ├── predictor.py     # Deterministic ML prediction engine
    ├── bracket.py       # Group stage & knockout simulation
    └── train.py         # Model training script
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Samarpan-7/FIFA-WC-26-Predictor.git
cd FIFA-WC-26-Predictor
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the model (first time only)
```bash
python src/train.py
```

### 5. Run the app
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## How Predictions Work

1. **ML Model Path** — If both teams are in the training set, the XGBoost model's `predict_proba()` output is used. The class with the highest probability wins. No randomness.

2. **Deterministic Fallback** — For teams outside the training set, a composite score is calculated:
   - Elo rating (60%)
   - FIFA ranking (20%)
   - Squad strength (20%)

3. **Score Generation** — Goals are derived from `(attack_rating - opponent_defense) / 20 + 1.2`. No `random.choices()`.

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

## License

MIT License — free to use, modify, and distribute.

---

*Built with Python, Streamlit, and XGBoost.*
