import os
import re
import csv
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


SELECTED_COLS = [
    "_source.@timestamp",
    "_source.agent.id",
    "_source.data.win.system.eventID",
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine",
    "_source.rule.mitre.id",
    "_source.rule.mitre.technique",
    "_source.rule.mitre.tactic",
]

TEXT_COLS = [
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine",
]

ENCODE_COLS = [
    "_source.agent.id",
    "_source.data.win.system.eventID",
    "_source.data.win.eventdata.image",
    "_source.data.win.eventdata.parentImage",
    "_source.data.win.eventdata.commandLine",
]

FEATURE_COLS = ENCODE_COLS + ["time_diff"]
MITRE_COL = "_source.rule.mitre.id"
TECHNIQUE_PATTERN = r"T\d{4}(?:\.\d{3})?"


def load_event_data(file_path):
    """Load the Windows event CSV and return a DataFrame."""
    rows = []
    with open(file_path, "r", encoding="utf-8", errors="replace", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            rows.append(row)

    df = pd.DataFrame(rows, columns=header)
    missing = [column for column in SELECTED_COLS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required event columns: {missing}")
    return df


def load_manifest_techniques(manifest_path):
    """Extract MITRE technique IDs from the manifest's sixth column."""
    manifest = pd.read_csv(manifest_path)
    if manifest.shape[1] <= 5:
        raise ValueError("The scenario manifest does not contain the expected sixth column.")

    techniques = set()
    for value in manifest.iloc[:, 5].dropna().astype(str):
        techniques.update(re.findall(TECHNIQUE_PATTERN, value))
    return techniques


def extract_event_techniques(value):
    return set(re.findall(TECHNIQUE_PATTERN, str(value)))


def prepare_event_data(df):
    """Select fields, parse timestamps, and sort events chronologically."""
    df_small = df[SELECTED_COLS].copy()
    df_small["_source.@timestamp"] = pd.to_datetime(
        df_small["_source.@timestamp"],
        format="%b %d, %Y @ %H:%M:%S.%f",
        errors="coerce",
    )
    df_small = df_small.sort_values(
        by="_source.@timestamp"
    ).reset_index(drop=True)
    return df_small


def create_labels(df_small, manifest_techniques):
    """Create proxy labels based on matches with manifest MITRE techniques."""
    result = df_small.copy()
    matches_manifest = result[MITRE_COL].apply(
        lambda value: bool(extract_event_techniques(value).intersection(manifest_techniques))
    )
    result["label"] = matches_manifest.astype(int)
    return result


def prepare_model_features(df_small):
    """Remove MITRE label-source fields and prepare categorical features."""
    model_df = df_small.drop(
        columns=[
            "_source.rule.mitre.id",
            "_source.rule.mitre.technique",
            "_source.rule.mitre.tactic",
        ]
    ).copy()

    for column in TEXT_COLS:
        model_df[column] = model_df[column].fillna("missing").astype(str)

    for column in ENCODE_COLS:
        model_df[column] = model_df[column].fillna("missing").astype(str)

    return model_df


def add_time_difference(model_df):
    """Calculate time between consecutive events from the same agent."""
    result = model_df.sort_values(
        by=["_source.agent.id", "_source.@timestamp"]
    ).reset_index(drop=True).copy()
    result["time_diff"] = (
        result.groupby("_source.agent.id")["_source.@timestamp"]
        .diff()
        .dt.total_seconds()
        .fillna(0)
    )
    return result


def split_by_agent(model_df, train_ratio=0.70, validation_ratio=0.15):
    """Split each agent's events chronologically into train/validation/test sets."""
    train_parts, val_parts, test_parts = [], [], []

    for _, group in model_df.groupby("_source.agent.id"):
        group = group.sort_values("_source.@timestamp").reset_index(drop=True)
        n = len(group)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + validation_ratio))
        train_parts.append(group.iloc[:train_end])
        val_parts.append(group.iloc[train_end:val_end])
        test_parts.append(group.iloc[val_end:])

    if not train_parts:
        raise ValueError("No event groups were available for splitting.")

    return (
        pd.concat(train_parts).reset_index(drop=True),
        pd.concat(val_parts).reset_index(drop=True),
        pd.concat(test_parts).reset_index(drop=True),
    )


def encode_and_scale(train_df, val_df, test_df):
    """Fit encoders/scaler on training data and apply them to all splits."""
    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    encoder = OrdinalEncoder(
        handle_unknown="use_encoded_value",
        unknown_value=-1,
    )
    train_df[ENCODE_COLS] = encoder.fit_transform(train_df[ENCODE_COLS])
    val_df[ENCODE_COLS] = encoder.transform(val_df[ENCODE_COLS])
    test_df[ENCODE_COLS] = encoder.transform(test_df[ENCODE_COLS])

    scaler = StandardScaler()
    train_df[FEATURE_COLS] = scaler.fit_transform(train_df[FEATURE_COLS])
    val_df[FEATURE_COLS] = scaler.transform(val_df[FEATURE_COLS])
    test_df[FEATURE_COLS] = scaler.transform(test_df[FEATURE_COLS])

    return train_df, val_df, test_df, encoder, scaler


def run_preprocessing(event_csv_path, manifest_csv_path):
    """Run the complete preprocessing workflow and return its outputs."""
    df = load_event_data(event_csv_path)
    df_small = prepare_event_data(df)
    manifest_techniques = load_manifest_techniques(manifest_csv_path)
    labelled_df = create_labels(df_small, manifest_techniques)
    model_df = prepare_model_features(labelled_df)
    model_df = add_time_difference(model_df)
    train_df, val_df, test_df = split_by_agent(model_df)
    train_df, val_df, test_df, encoder, scaler = encode_and_scale(
        train_df, val_df, test_df
    )

    return {
        "train": train_df,
        "validation": val_df,
        "test": test_df,
        "manifest_techniques": manifest_techniques,
        "encoder": encoder,
        "scaler": scaler,
    }


def main():
    repository_root = Path(__file__).resolve().parent.parent
    data_dir = repository_root / "data"
    event_csv_path = data_dir / "combined.csv"
    manifest_csv_path = data_dir / "scenario_manifest.csv"

    for path in (event_csv_path, manifest_csv_path):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}. Store the CSV files in the repository's data/ folder."
            )

    results = run_preprocessing(event_csv_path, manifest_csv_path)
    print("Preprocessing completed.")
    print("Train:", results["train"].shape)
    print("Validation:", results["validation"].shape)
    print("Test:", results["test"].shape)
    print("Train labels:\n", results["train"]["label"].value_counts())
    print("Validation labels:\n", results["validation"]["label"].value_counts())
    print("Test labels:\n", results["test"]["label"].value_counts())


if __name__ == "__main__":
    main()
