# LotL-Attack-Detection Using LSTM

## 1. Project Overview

This project aims to detect Living-off-the-Land (LotL) attack patterns through the analysis of Windows event logs. By using LSTM networks, the project examines sequences of Windows events to identify patterns that match simulated MITRE ATT&CK techniques.

This project examines both a Short-Sequence LSTM (analyzing 5 Windows events) and a Long-Sequence LSTM (analyzing 20 Windows events).

## 2. Project Objectives

- Detect suspicious patterns through sequences of Windows events.
- Create a Short-Sequence LSTM.
- Create a Long-Sequence LSTM.
- Compare both models.
- Assess both models using various evaluation metrics.

## 3. Models

- **Short-Sequence LSTM:** Analyzes a sequence of 5 Windows events.
- **Long-Sequence LSTM:** Analyzes a sequence of 20 Windows events.

Both models use LSTM networks to analyze sequences of Windows events.

## 4. Dataset

This project uses a dataset consisting of Windows event logs stored in `combined.csv`. A scenario manifest is also used to determine the labels by matching events with simulated MITRE ATT&CK techniques.

A MITRE ATT&CK match does not necessarily confirm an actual attack. Therefore, the labels should be interpreted carefully.

Only anonymized or synthetic test data should be included in this repository. Sensitive event logs must not be uploaded.

## 5. Evaluation Metrics

The models were evaluated using the following metrics:

- Accuracy
- Precision
- Recall
- F1-score
- False-positive rate (FPR)
- Confusion matrix

## 6. Repository Structure

- `data/` - Documentation regarding the dataset and approved test data.
- `notebooks/` - Jupyter notebooks used for preprocessing, training, and evaluation.
- `reports/` - Project documentation, evaluation results, and reports.
- `src/` - Source code and supporting scripts.
- `tests/` - Automated tests for preprocessing, sequence creation, and model input/output shapes.
- `requirements.txt` - List of required Python packages.

## 7. Technologies Used

- Python
- TensorFlow / Keras
- Pandas
- NumPy
- Scikit-learn
- Jupyter Notebook

## 8. Installation and Setup

First, clone the repository:

```bash
git clone https://github.com/asma2906/LotL-Attack-Detection.git
cd LotL-Attack-Detection
```

Next, install the required dependencies:

```bash
pip install -r requirements.txt
```

Run Jupyter Notebook:

```bash
jupyter notebook
```

Finally, navigate to the appropriate notebook in the `notebooks/` directory.

## 9. Running Automated Tests

To run the automated tests, execute:

```bash
python -m unittest discover -s tests -v
```

This command discovers and runs the test files inside the `tests/` directory.

## 10. Team

This is a group project for the CSCY413 Special Topics in Cybersecurity course.

## 11. Data Privacy

Only synthetic or anonymized data should be included in this repository. Sensitive or confidential Windows event logs must not be uploaded. This helps protect privacy and prevent unauthorized access to sensitive information.
