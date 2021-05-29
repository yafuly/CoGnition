# CoGnition: a Compositional Generalization Machine Translation Dataset


CoGnition is a dataset decicated for evaluating compositional generailziation in machine translation, consisting of altogether 227,046 parallel sentences:
Split | # Samples
------------ | -------------
Training set | 196,246
Validation set | 10,000
Random test set | 10,000
CG test set | 10,800

Besides human evaluation, we provide an automatic evaluation tool as an alternative.

This work is accepted by main conference of ACL 2021. You may find the paper here: <>.

## Data
All splits of CoGnitnion dataset are included in /data, which contains randomly split training, validation and test sets, along with a CG test set for evaluating compositonal genernalization.

## Automatic Evaluation
To automatically evaluate the ability of compositional generalization for MT models, run 'eval/eval.py' on model results:
`python eval.py path_to_results lexicon`
where 'path_to_results' refers to the path of model results and 'lexicon' refers to the provided lexicon, i.e., 'eval/lexicon'. Note that the model results should contain test sentences, **corresponding compounds** and model translations.

## Acknowledgment
We thank colleagues from [Lan-bridge]{http://www.lan-bridge.com/} for examining data and evaluating results. 
Major contributors include Xianchao Zhu, Guohui Chen, Jing Yang, Jing Li, Feng Chen, Jun Deng and Jiaxiang Xiang.