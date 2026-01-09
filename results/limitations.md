## Limitations

### Single consistent configuration

All experiments work with one fixed configuration, for example for the retrieval pipeline 
(all-MiniLM-L6-v2 embeddings, fixed chunk size and overlap). 
This ensures controlled comparisons across model sizes, but the observed effects may be different under different configurations or retrievers.
The configuration is also not tuned to the specific model size but is constant. 

### Accuracy-focused evaluation without explicit faithfulness metrics

The study evaluates answer correctness but does not explicitly measure whether generated answers are grounded in the
retrieved context. As a result, correct answers may occasionally be produced based on parametric knowledge rather than
retrieved evidence, particularly for larger models.

### Restricted range of model sizes

The analysis considers three model scales (0.5B, 7B, and 14B). While sufficient to reveal non-monotonic scaling trends,
the results may not extrapolate to substantially larger models or instruction-tuned models with different training
regimes.

### Single prompt per task setting

Each dataset is evaluated using a fixed prompt template. Although this isolates model size effects, alternative
prompting strategies—particularly those explicitly encouraging deference to retrieved evidence—may influence
contradiction handling behavior.

### Domain specificity

The experiments focus on biomedical QA and counterfactual factual tasks. The extent to which the observed scaling and
contradiction-handling behaviors generalize to other domains remains an open question.