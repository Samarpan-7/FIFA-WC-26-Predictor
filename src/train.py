import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/matches.csv")

# Create target
df["result"] = df.apply(
    lambda x: 2 if x.home_score > x.away_score
    else 0 if x.home_score < x.away_score
    else 1,
    axis=1
)

# Encode teams
teams = pd.concat([df.home_team, df.away_team]).unique()

le = LabelEncoder()
le.fit(teams)

df["home"] = le.transform(df.home_team)
df["away"] = le.transform(df.away_team)

X = df[["home", "away"]]
y = df["result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

joblib.dump((model, le), "models/match_model.pkl")

print("Model Saved")