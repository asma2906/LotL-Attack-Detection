 Dataset and Preprocessing

 1. Dataset Files

The preprocessing workflow uses two CSV files:

- `combined.csv`: Contains Windows event log data used in the project\.
- `scenario_manifest.csv`: Contains information about the simulated
  attack scenarios\.

The original dataset files are not included in this repository\.

2. Selected Features

The following fields are selected from the event logs:

- Timestamp
- Agent ID
- Windows Event ID
- Process image
- Parent process image
- Command line
- MITRE technique ID
- MITRE technique
- MITRE tactic

The MITRE fields are used during label creation and are removed from the
model input afterward\.

3. Label Creation

The labels are created by comparing MITRE technique IDs in the event
logs with the techniques listed in the scenario manifest\.

- An event is assigned label `1` when its MITRE technique ID matches a
  technique in the scenario manifest\.
- An event is assigned label `0` when no matching technique ID is
  found\.

**Important limitation:** These labels are proxy labels based on MITRE
technique matching\. They are not confirmed event\-level ground\-truth
labels\. Therefore, an event assigned label `0` should not automatically
be considered benign\.

4. Data Preprocessing

The preprocessing steps include:

- Converting the timestamp field to datetime format\.
- Sorting the events by timestamp\.
- Replacing missing values in the process image, parent process image,
  and command\-line fields\.
- Converting categorical features to string values\.
- Sorting events by agent ID and timestamp\.
- Calculating the time difference between consecutive events from the
  same agent\.
- Encoding categorical features using `OrdinalEncoder`\.
- Scaling numerical features using `StandardScaler`\.

The encoders and scaler are fitted using the training data and then
applied to the validation and testing data\.

5. Data Splitting

The data is sorted by agent ID and timestamp\. It is then divided
chronologically within each agent:

- 70% training data
- 15% validation data
- 15% testing data

This preserves the chronological order within each agent’s events\.

6. Sequence Preparation

The processed event data is used by the model workflow to prepare two
sequence lengths:

- Short sequences: 5 events\.
- Long sequences: 20 events\.

The label of each sequence is assigned using the label of its final
event\. Sequence generation is part of the model workflow; it is not
performed by `src/preprocessing.py`\.

7. Important Notes

- The preprocessing script is available in `src/preprocessing.py`\.
- The original dataset files are not included in this repository\.
- The label\-generation method has the proxy\-label limitation described
  above\.
