import os
import csv
import re
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

folder_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder_path, "combined.csv")

rows = []

with open(file_path, "r", encoding="utf-8", errors="replace", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        rows.append(row)

df = pd.DataFrame(rows, columns=header)

print("Dataset shape:", df.shape)

selected_cols = [
    "_source.@timestamp",
    "_source.agent.id",
    "_source.data.win.system.eventID",
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine",
    "_source.rule.mitre.id",
    "_source.rule.mitre.technique",
    "_source.rule.mitre.tactic"
]

df_small = df[selected_cols].copy()

print("Working dataset shape:", df_small.shape)
print(df_small.head())

df_small["_source.@timestamp"] = pd.to_datetime(
    df_small["_source.@timestamp"],
    format="%b %d, %Y @ %H:%M:%S.%f",
    errors="coerce"
)

print("Total rows:", len(df_small))
print("Valid timestamps:", df_small["_source.@timestamp"].notna().sum())
print("Invalid timestamps:", df_small["_source.@timestamp"].isna().sum())

print("First date:", df_small["_source.@timestamp"].min())
print("Last date:", df_small["_source.@timestamp"].max())

# Sort all events by time
df_small = df_small.sort_values(
    by="_source.@timestamp"
).reset_index(drop=True)

print("Dataset shape:", df_small.shape)

print("\nFirst 5 timestamps:")
print(df_small["_source.@timestamp"].head())

print("\nLast 5 timestamps:")
print(df_small["_source.@timestamp"].tail())

manifest_path = os.path.join(folder_path, "scenario_manifest.csv")
manifest = pd.read_csv(manifest_path)

# Collect all MITRE technique IDs from the scenario manifest
manifest_techniques = set()

for text in manifest.iloc[:, 5].dropna().astype(str):
    manifest_techniques.update(
        re.findall(r"T\d{4}(?:\.\d{3})?", text)
    )

print("Number of unique simulated techniques:", len(manifest_techniques))
print(sorted(manifest_techniques))

mitre_col = "_source.rule.mitre.id"

print("MITRE column:", mitre_col)
print("Column exists:", mitre_col in df_small.columns)

def extract_event_techniques(value):
    return set(re.findall(r"T\d{4}(?:\.\d{3})?", str(value)))

def has_manifest_technique(value):
    event_techs = extract_event_techniques(value)
    return len(event_techs.intersection(manifest_techniques)) > 0


matches_manifest = df_small[mitre_col].apply(has_manifest_technique)

print("Events matching simulated techniques:", matches_manifest.sum())
print("Events not matching simulated techniques:", (~matches_manifest).sum())

df_small["label"] = matches_manifest.astype(int)

print(df_small["label"].value_counts())

print("\nPercentages:")
print(df_small["label"].value_counts(normalize=True) * 100)

model_df = df_small.drop(
    columns=[
        "_source.rule.mitre.id",
        "_source.rule.mitre.technique",
        "_source.rule.mitre.tactic"
    ]
).copy()

print("Model dataset shape:", model_df.shape)
print(model_df.columns.tolist())

text_cols = [
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine"
]

for col in text_cols:
    model_df[col] = model_df[col].fillna("missing").astype(str)

print(model_df[text_cols].isna().sum())
print(model_df[text_cols].head())

encode_cols = [
    "_source.agent.id",
    "_source.data.win.system.eventID",
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine"
]

for col in encode_cols:
    model_df[col] = model_df[col].fillna("missing").astype(str)

print("Categorical columns prepared:")
print(model_df[encode_cols].head())

# Sort by agent and timestamp first
model_df = model_df.sort_values(
    by=["_source.agent.id", "_source.@timestamp"]
).reset_index(drop=True)

# Time difference in seconds between events from the same agent
model_df["time_diff"] = (
    model_df.groupby("_source.agent.id")["_source.@timestamp"]
    .diff()
    .dt.total_seconds()
)

# First event for each agent has no previous event
model_df["time_diff"] = model_df["time_diff"].fillna(0)

print(model_df[[
    "_source.agent.id",
    "_source.@timestamp",
    "time_diff"
]].head(20))

print("\nTime difference statistics:")
print(model_df["time_diff"].describe())

train_parts = []
val_parts = []
test_parts = []

for agent_id, group in model_df.groupby("_source.agent.id"):
    group = group.sort_values("_source.@timestamp").reset_index(drop=True)

    n = len(group)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    train_parts.append(group.iloc[:train_end])
    val_parts.append(group.iloc[train_end:val_end])
    test_parts.append(group.iloc[val_end:])

train_df = pd.concat(train_parts).reset_index(drop=True)
val_df = pd.concat(val_parts).reset_index(drop=True)
test_df = pd.concat(test_parts).reset_index(drop=True)

print("Train:", train_df.shape)
print("Validation:", val_df.shape)
print("Test:", test_df.shape)

print("\nTrain labels:")
print(train_df["label"].value_counts())

print("\nValidation labels:")
print(val_df["label"].value_counts())

print("\nTest labels:")
print(test_df["label"].value_counts())

encoder = OrdinalEncoder(
    handle_unknown="use_encoded_value",
    unknown_value=-1
)

# Fit only on training data
train_df[encode_cols] = encoder.fit_transform(
    train_df[encode_cols]
)

# Apply the same encoder to validation and test data
val_df[encode_cols] = encoder.transform(
    val_df[encode_cols]
)

test_df[encode_cols] = encoder.transform(
    test_df[encode_cols]
)

print("Encoder fitted on training data only.")

print("\nTraining encoded features:")
print(train_df[encode_cols].head())

feature_cols = [
    "_source.agent.id",
    "_source.data.win.system.eventID",
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine",
    "time_diff"
]

scaler = StandardScaler()

train_df[feature_cols] = scaler.fit_transform(train_df[feature_cols])

val_df[feature_cols] = scaler.transform(val_df[feature_cols])

test_df[feature_cols] = scaler.transform(test_df[feature_cols])

print(train_df[feature_cols].head())

print("\nTraining feature means:")
print(train_df[feature_cols].mean())

print("\nTraining feature std:")
print(train_df[feature_cols].std())
