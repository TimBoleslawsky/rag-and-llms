## Limitations

### Single retrieval configuration

All experiments rely on a fixed retrieval pipeline (all-MiniLM-L6-v2 embeddings, fixed chunk size and overlap). While
this ensures controlled comparisons across model sizes, the observed scaling effects may vary under alternative
retrievers or document segmentation strategies.

### Accuracy-focused evaluation without explicit faithfulness metrics

The study evaluates answer correctness but does not explicitly measure whether generated answers are grounded in the
retrieved context. As a result, correct answers may occasionally be produced based on parametric knowledge rather than
retrieved evidence, particularly for larger models.

### Limited analysis of retrieval quality under contradiction

In the ClashEval setting, retrieval accuracy is relatively low, which introduces ambiguity between model resistance to
external evidence and appropriate skepticism toward incorrect retrievals. The study does not disentangle these two
factors.

### Restricted range of model sizes

The analysis considers three model scales (0.5B, 7B, and 14B). While sufficient to reveal non-monotonic scaling trends,
the results may not extrapolate to substantially larger models or instruction-tuned models with different training
regimes.

### Single prompt per task setting

Each dataset is evaluated using a fixed prompt template. Although this isolates model size effects, alternative
prompting strategies—particularly those explicitly encouraging deference to retrieved evidence—may influence
contradiction handling behavior.

### Limited dataset size per configuration

Each configuration is evaluated on 50 questions, which is enough to observe consistent trends but may limit
statistical power for fine-grained comparisons between closely performing models.

### Domain specificity

The experiments focus on biomedical QA and counterfactual factual tasks. The extent to which the observed scaling and
contradiction-handling behaviors generalize to other domains remains an open question.