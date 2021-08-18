
echo "learn_bpe.py on ${TRAIN}..."
src='en'
tgt='zh'
tmp='bpe'
prep='bpe/out'
mkdir $tmp
mkdir $prep
BPEROOT="PATH_TO_subword_nmt"
BPE_CODE=$prep/code
BPE_TOKENS=2000

TRAIN=$tmp/train.en-zh
for l in $src $tgt; do
    cat $tmp/train.$l >> $TRAIN
done

python $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

for f in train.$tgt valid.$tgt test.$tgt; do
    echo "apply_bpe.py to ${f}..."
    python $BPEROOT/apply_bpe.py -c $BPE_CODE < $tmp/$f > $prep/$f
done