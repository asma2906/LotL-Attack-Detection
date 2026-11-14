# LSTM Model Evaluation and Results

## 1. Evaluation Overview

This section presents the evaluation of two Long Short-Term Memory (LSTM) models developed for Living-off-the-Land (LotL) attack detection. The Short-Sequence LSTM processes sequences of 5 events, while the Long-Sequence LSTM processes sequences of 20 events.

Both models are evaluated using accuracy, precision, recall, F1-score, and false-positive rate to assess their detection performance.

## 2. Model Performance Comparison

| Evaluation Metric | Short-Sequence LSTM | Long-Sequence LSTM |
|---|---:|---:|
| Sequence Length | 5 | 20 |
| Accuracy | 94.73% | 93.62% |
| Precision | 97.51% | 96.01% |
| Recall | 94.44% | 94.29% |
| F1-score | 95.95% | 95.14% |
| False-Positive Rate | 4.72% | 7.69% |

The evaluation results were obtained from the project's updated LSTM Final Comparison Results Excel file. These results represent a training run performed without a fixed random seed.

## 3. Confusion Matrix Analysis

The confusion matrices provide a visual representation of the classification results for each model, including true positives, true negatives, false positives, and false negatives.

The corresponding figures are available in:

- `short_sequence_confusion_matrix.png`
- `long_sequence_confusion_matrix.png`

The Short-Sequence LSTM achieved a lower false-positive rate of 4.72%, compared with 7.69% for the Long-Sequence LSTM. This indicates that the Short-Sequence model generated fewer false alarms relative to the number of actual negative cases.

Additionally, the Short-Sequence model achieved slightly higher recall (94.44%) than the Long-Sequence model (94.29%), indicating a marginal improvement in detecting actual attacks.

## 4. Evaluation Findings

The Short-Sequence LSTM achieved higher accuracy (94.73%), precision (97.51%), recall (94.44%), and F1-score (95.95%) compared with the Long-Sequence LSTM.

The Short-Sequence model also achieved a lower false-positive rate (4.72%) compared with the Long-Sequence model (7.69%).

These findings suggest that processing shorter sequences of events was more effective for LotL attack detection in this experiment. The Short-Sequence model demonstrated better overall classification performance while reducing false security alerts.

Although longer sequences provide additional temporal context, this did not result in improved performance in the reported experiment. The additional sequence information may not have provided sufficient benefit to outperform the shorter sequence representation.

Overall, the Short-Sequence LSTM demonstrated a better balance between attack detection accuracy, sensitivity, and false-alarm reduction.

## 5. Conclusion

Both LSTM models demonstrated strong classification performance, achieving accuracy above 93% and F1-scores above 95%.

The Short-Sequence LSTM achieved the best overall results, with an accuracy of 94.73%, precision of 97.51%, recall of 94.44%, and F1-score of 95.95%.

Furthermore, its lower false-positive rate of 4.72% indicates that it may be more suitable for cybersecurity monitoring systems where minimizing unnecessary security alerts is important.

Overall, the evaluation results indicate that the Short-Sequence LSTM was the better-performing model in this experiment, demonstrating that shorter event sequences can provide effective detection of Living-off-the-Land attacks without requiring longer temporal inputs.

Since the training was conducted without a fixed random seed, results may vary between runs. Further repeated experiments would be necessary to establish whether the observed performance advantage is consistent.
