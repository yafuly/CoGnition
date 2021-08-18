# CoGnition: a Compositional Generalization Machine Translation Dataset


CoGnition is a dataset decicated for evaluating compositional generailziation in machine translation, containing parallel corpus of 216,246 sentence pairs and a CG test set of 10,800 sentence pairs.

Split | # Samples
------------ | -------------
Training set | 196,246
Validation set | 10,000
Random test set | 10,000
CG test set | 10,800

To evaluate your model's ability of compositonal generalization, train your model on training and validation sets and evaluate on both the **random test set** and the **CG test set**. Either human evaluation or the provided automatic evaluation tool can be employed to evalaute the correctness of compound translations.

This work is accepted to appear at the ACL 2021 main conference. You may find the paper here: [https://arxiv.org/abs/2105.14802](https://arxiv.org/abs/2105.14802).

## Data
All splits of CoGnitnion dataset are included in '/data', which contains the randomly split training, validation and test sets, along with the CG test set ('/data/cg-test') for evaluating compositonal genernalization.

Samples from the training, validation and random test sets:

Src | Ref
------------ | -------------
taylor pulled over and fixed the man 's car in less than an hour . | 泰勒 靠边 停车 ， 不到 一个 小时 就 修好 了 那 人 的 车 。
she kept asking her husband , but they did n't have enough money . | 她 一直 问 她 丈夫 ， 但 他们 没有 足够 的 钱 。
i went to the kitchen to make a sandwich . | 我 去 厨房 做 三明治 。
but when she looked in the mirror only her face was young . | 但 当 她 照镜子 时 ， 只有 她 的 脸 是 年轻 的 。
she had to go and buy more . | 她 不得不 去 买 更 多 的 东西 。
taylor had a small house in the country . |  泰勒 在 乡下 有 一所 小 房子 。
taylor screamed with joy . | 泰勒 高兴 得 尖叫 起来 。
she could n't wait to use the new words . |  她 迫不及待 地想用 这些 新词 。

The target side Chinese is segmented using [Jieba segmenter](https://github.com/fxsjy/jieba).

Samples from the **CG test set**:

Src | Compound | Ref
------------ | ------------- | -------------
all the sudden the waiter screamed in pain . | the waiter | 突然，服务员痛苦地尖叫起来。
one day another lazy lawyer snapped and broke every window in the car . | another lazy lawyer | 一天，另一个懒惰的律师啪地一声打碎了车里的每一扇窗户。
each doctor he liked was talking to a friend on the phone . | each doctor he liked | 他喜欢的每一个医生都在和一个朋友通电话。
every smart lawyer at the store decided to go back next week . | every smart lawyer at the store | 店里每个聪明的律师都决定下周再去。
she said she liked the building ! | liked the building | 她说她喜欢这栋楼！
he soon met the special girl named taylor . | met the special girl | 他很快就遇到了那个特别的女孩，名叫泰勒。
she took the child he liked out to enjoy the snow . | took the child he liked | 她带着他喜欢的孩子出去赏雪。
when taylor saw the dirty car he liked , he was amazed . | saw the dirty car he liked | 当泰勒看到他喜欢的脏车时，他惊叹不已。
taylor felt really awful about the bee . | about the bee | 泰勒对蜜蜂的事感到很难过。
inside the small apartment were some of my old toys . | inside the small apartment | 小公寓里放着我的一些旧玩具。
taylor forgot about the chair on the floor ! | about the chair on the floor | 泰勒忘了地板上的椅子！
he jumped from the bench towards the large airplane on the floor . | towards the large airplane on the floor | 他从长凳上跳向地板上的大飞机。

The corresponding compounds are listed in '/data/cg-test/*.compound'.

## Automatic Evaluation
Besides human evaluation, we provide an automatic evaluation tool as an alternative. With the human annotation as ground truth, our automatic evaluation tool achieves a precision of 94.80% and a recall of 87.05%. To automatically evaluate the ability of compositional generalization for MT models, run '/eval/eval.py' on model results:
`python eval.py 'path_to_results' 'path-to-lexicon'`
where 'path_to_results' refers to the path of model results and 'path-to-lexicon' refers to the provided lexicon, i.e., '/eval/lexicon'. Note that the model results should contain test sentences, **corresponding compounds** and model translations, separated by '\t', e.g., "the lawyer ended up winning second place !'\t'the lawyer'\t'律师 最终 得 了 第二名 ！".

## Baseline
'/eval/paper_results' lists the model results along with human evaluation in the paper, based on which we conduct quantitative anylysis. As we asked expert translators to further examine the data of the CG-test set, there are minor differences between the data in '/data/cg-test' and the one used in the paper: a) some illegal sentences are replaced with legal ones (less than 1%); b) some reference translations are further revised.

We use the same model in the paper to perform inference on the test data in '/data/cg-test' and use the **automatic evaluation tool** for evaluation:
Test Set | Instance-level Error Rate | Aggregate-level Error Rate | BLEU 
------------ | ------------- | ------------- | ------------- 
Random-test | - | - | 69.58
CG-test | 24.99% | 58.06% | 60.6
CG-test-NP | 19.31% | 49.03% | -
CG-test-VP | 22.48% | 54.17% | -
CG-test-PP | 33.25% | 70.97% | -

This can serve as an NMT **baseline** for the CoGnition dataset **under automatic evaluation**. Note that the BLEU score on the CG-test set is different from the results in our paper due to mistakes in handling Chinese puncutations.

## Acknowledgment
We thank colleagues from [Lan-bridge](http://www.lan-bridge.com/) for examining data and evaluating results. 
Major contributors include Xianchao Zhu, Guohui Chen, Jing Yang, Jing Li, Feng Chen, Jun Deng and Jiaxiang Xiang.