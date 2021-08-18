data=PATH_TO_FAIRSEQ_DATABIN
subset=cg-test
model=PATH_TO_MODEL # model name, e.g., PATH_TO_MODEL/checkpoint_best.pt
run_path=PATH_TO_FAIRSEQ_CLI # fairseq_cli path
eval_path=PATH_TO_COGNITION_EVAL # e.g., PATH_TO_COGNITION/eval

# inference with fairseq
CUDA_VISIBLE_DEVICES=0 python $run_path/generate.py $data \
    --gen-subset $subset \
    -s 'en' \
    -t 'zh' \
    --path $model \
    --dataset-impl 'raw' \
    --batch-size 512 --beam 5 --remove-bpe  > $data/$subset.en-zh.en.out

# reorder outputs to original order
python _reorder.py $data/$subset.en-zh.en $data/$subset.en-zh.en.out $data/$subset.en-zh.zh > $data/$subset.en-zh.en.src-hyp-tgt

# compute scarebleu score
cut -f2 $data/$subset.en-zh.en.src-hyp-tgt | tee $data/$subset.en-zh.en.hyp | sed -e 's/ //g' > $data/$subset.en-zh.en.hyp.detok
cut -f3 $data/$subset.en-zh.en.src-hyp-tgt > $data/$subset.en-zh.en.ref
sacrebleu $data/$subset.en-zh.en.ref -i $data/$subset.en-zh.en.hyp.detok -l en-zh -b > $data/$subset.bleu

# compute compound translation error rate
cut -f1,2 $data/$subset.en-zh.en.src-hyp-tgt > $data/$subset.en-zh.en.src-hyp
paste $data/$subset.en-zh.en.src-hyp $data/$subset.compound | awk -F"\t" '{print $1"\t"$3"\t"$2}' > $data/$subset.merge
python $eval_path/eval.py  $data/$subset.merge $eval_path/lexicon > $data/$subset.error-rate
