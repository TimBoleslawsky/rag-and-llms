## Results

### BIOASQ

(50 questions)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.68    | 0.44           | 0.74             | 1.00          |
| 3B    | 0.62    | 0.66           | 0.88             | 1.00          |
| 7B    | 0.92    | 0.74           | 0.96             | 1.00          |
| 14B   | 0.92    | 0.46           | 0.98             | 1.00          |
| 32B   | 0.90    | 0.72           | 0.98             | 1.00          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.64    | 0.42           | 0.76             | 1.00          |
| 3B    | 0.68    | 0.58           | 0.90             | 1.00          |
| 7B    | 0.92    | 0.70           | 0.98             | 1.00          |
| 14B   | 0.88    | 0.38           | 0.98             | 1.00          |
| 32B   | 0.8     | 0.64           | 0.90             | 1.00          |

### PUBMED 

(50 questions)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.66    | 0.54           | 0.68             | 0.98          |
| 3B    | 0.28    | 0.50           | 0.30             | 0.98          |
| 7B    | 0.96    | 0.52           | 0.96             | 0.98          |
| 14B   | 0.86    | 0.34 (44)      | 0.88             | 0.98          | 
| 32B   | 0.88    | 0.44           | 0.90             | 0.98          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.70    | 0.42           | 0.66             | 0.98          |
| 3B    | 0.30    | 0.48           | 0.36             | 0.98          |
| 7B    | 0.96    | 0.52           | 0.96             | 0.98          |
| 14B   | 0.82    | 0.30           | 0.86             | 0.98          |
| 32B   | 0.84    | 0.44           | 0.82             | 0.98          |

### CLASHEVAL

(50 questions)

Temperature = 0.1

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.12    | 0.00           | 0.40             | 0.34          |
| 3B    | 0.18    | 0.02           | 0.56             | 0.34          |
| 7B    | 0.14    | 0.02           | 0.64             | 0.32          |
| 14B   | 0.14    | 0.02           | 0.64             | 0.32          |
| 32B   | 0.12    | 0.02           | 0.54             | 0.32          |

Temperature = 1.0

| Model | RAG Acc | No Context Acc | With Context Acc | Retrieval Acc |
|-------|---------|----------------|------------------|---------------|
| 0.5B  | 0.10    | 0.00           | 0.38             | 0.32          |
| 3B    | 0.12    | 0.02           | 0.54             | 0.32          |
| 7B    | 0.14    | 0.02           | 0.62             | 0.30          |
| 14B   | 0.18    | 0.02           | 0.64             | 0.30          |
| 32B   | 0.18    | 0.02           | 0.56             | 0.32          |

## Findings

### Language Model Efficacy 

- Context consistently improves performance. 
- Model efficacy with and without context consistently increases with size until about 7B parameters (3B model with pubmed dataset seems to be an outlier). 
- Model efficacy seems to fall off a bit when increasing the model size past 7B parameters. Especially without context. Interesting here is, that the 14B model is significantly worse than the 7B and the 32B model. 
- Increasing the temperature seems to decrease the efficacy a bit, with the 7B model being the most stable.

### Counterfactual Performance

- Retrieval accuracy is low ⇒ model is under epistemic stress, meaning the model’s usual mechanisms for producing
  correct answers are put under strain (available information sources conflict).
- RAG accuracy is not really helpful here.
- Model with no context is consistently bad (0.00 - 0.02%). This tells us that 1.) the questions cannot be solved with internal
  knowledge, it is actually misleading, and 2.) larger models are not better at this than smaller models.
- Overall accuracy with context is low, indicating that models struggle with the contradictions.
- 7B and 14B models perform the best. Still a monotonous increase in efficacy from 0.5-7B, slight decline with 32B model. 

## Explanations

TBD

## Limitations

### Single consistent configuration

All experiments work with one fixed configuration, for example for the retrieval pipeline (all-MiniLM-L6-v2 embeddings, fixed chunk size and overlap). 
This ensures controlled comparisons across model sizes, but the observed effects may be different under different configurations or retrievers.
The configuration is also not tuned to the specific model size but is constant. 

### Accuracy-focused evaluation without explicit faithfulness metrics

The study evaluates answer correctness but does not explicitly measure whether generated answers are grounded in the
retrieved context. As a result, correct answers may occasionally be produced based on parametric knowledge rather than
retrieved evidence, particularly for larger models.

### Single prompt per task setting

Each dataset is evaluated using a fixed prompt template. This isolates model size effects, but alternative
prompting strategies, especially those fine-tuned to specific models, might change the behavior of the models significantly. 

### Domain specificity

The experiments focus on biomedical QA and counterfactual factual tasks. The extent to which the observed scaling and
contradiction-handling behaviors generalize to other domains remains unanswered.
