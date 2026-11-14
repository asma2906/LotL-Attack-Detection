# LSTM Model Evaluation and Results

## 1. Evaluation Overview

This section presents the evaluation of two Long Short-Term Memory (LSTM) models developed for Living-off-the-Land (LotL) attack detection. The Short-Sequence LSTM processes sequences of 5 events, while the Long-Sequence LSTM processes sequences of 20 events.

Both models are evaluated using accuracy, precision, recall, F1-score, and false-positive rate to assess their detection performance.

## 2. Model Performance Comparison

| Evaluation Metric | Short-Sequence LSTM | Long-Sequence LSTM |
|---|---:|---:|
| Sequence Length | 5 | 20 |
| Accuracy | 93.66% | 93.72% |
| Precision | 97.61% | 96.87% |
| Recall | 92.69% | 93.55% |
| F1-score | 95.09% | 95.18% |
| False-Positive Rate | 4.45% | 5.94% |

The evaluation results were obtained from the project's model comparison CSV file.

## 3. Confusion Matrix Analysis

The confusion matrices provide a visual representation of the classification results for each model, including true positives, true negatives, false positives, and false negatives.

The corresponding figures are available in:

- `short_sequence_confusion_matrix.png`
- `long_sequence_confusion_matrix.png`

## 4. Evaluation Findings

The Long-Sequence LSTM achieved slightly higher accuracy (93.72%), recall (93.55%), and F1-score (95.18%) compared with the Short-Sequence LSTM. This suggests that processing longer event sequences may improve the model's ability to identify malicious behaviour.

However, the Short-Sequence LSTM achieved higher precision (97.61%) and a lower false-positive rate (4.45%) compared with the Long-Sequence LSTM (5.94%).

This indicates that the Short-Sequence model may be more suitable when reducing false security alerts is a priority, while the Long-Sequence model may be preferable when detecting a higher proportion of attacks is more important.

## 5. Conclusion

Both LSTM models demonstrated strong classification performance, achieving accuracy above 93% and F1-scores above 95%.

The Long-Sequence LSTM achieved marginally better overall accuracy and F1-score, while the Short-Sequence LSTM provided better precision and fewer false positives.

Overall, the results demonstrate a trade-off between attack detection sensitivity and false-alarm reduction. The appropriate model depends on the operational priorities of the cybersecurity monitoring system.
