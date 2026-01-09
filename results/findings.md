## Results

### BIOASQ – RAG PERFORMANCE

(50 questions per setting)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.68    | 0.44           | 0.74             | 1.00          |
| 7B    | 0.92    | 0.74           | 0.96             | 1.00          |
| 14B   | 0.92    | 0.46           | 0.98             | 1.00          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.64    | 0.42           | 0.76             | 1.00          |
| 7B    | 0.92    | 0.70           | 0.98             | 1.00          |
| 14B   | 0.88    | 0.38           | 0.98             | 1.00          |

### PUBMED – RAG PERFORMANCE

(50 questions per setting)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.66    | 0.54           | 0.68             | 0.98          |
| 7B    | 0.96    | 0.52           | 0.96             | 0.98          |
| 14B   | 0.86    | 0.34           | 0.88             | 0.98          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.70    | 0.42           | 0.66             | 0.98          |
| 7B    | 0.96    | 0.52           | 0.96             | 0.98          |
| 14B   | 0.82    | 0.30           | 0.86             | 0.98          |

### CLASHEVAL – CONTRADICTION SETTING

(50 questions)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.10    | 0.00           | 0.42             | 0.34          |
| 7B    | 0.10    | 0.00           | 0.54             | 0.30          |
| 14B   | 0.10    | 0.00           | 0.40             | 0.34          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.10    | 0.00           | 0.38             | 0.30          |
| 7B    | 0.16    | 0.00           | 0.50             | 0.32          |
| 14B   | 0.04    | 0.00           | 0.36             | 0.36          |

## Findings

### With Context Accuracy Analysis

- 0.5B Model constantly performs worse than larger models when provided with context.
- 7BM Model performs more stably than 14B Model across datasets and temperatures.

### Without Context Accuracy Analysis

- 14B Model shows a significant drop in accuracy without context, indicating dependence on retrieved information.
- 7B Model and 0.5B Model show more consistent performance without context.

### Temperature Analysis

- Higher temperature generally decreases accuracy.
- The 7B Model is less affected by temperature changes compared to 0.5B and 14B Models.

### Counterfactual Analysis

- Retrieval accuracy is low ⇒ model is under epistemic stress, meaning the model’s usual mechanisms for producing
  correct answers are put under strain (available information sources conflict).
- RAG accuracy is not really helpful here.
- Model with no context is consistently bad (0%). This tells us that 1.) the questions cannot be solved with internal
  knowledge, it is actually misleading, and 2.) larger models are not better at this than smaller models.
- Overall accuracy with context is low, indicating that models struggle with the contradictions.
- There is a U shape in performance as the model size increases (7B is better than both 0.5B and 14B).