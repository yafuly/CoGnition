import sys

src = sys.argv[1]
out = sys.argv[2]
tgt = sys.argv[3]
src_lines = [l.strip() for l in open(src,'r').readlines()]
out_lines = [l.strip() for l in open(out,'r').readlines()]
tgt_lines = [l.strip() for l in open(tgt,'r').readlines()]


hyp_idx = []
for line in out_lines:
    if "H-" in line:
        idx = line.split("\t")[0].replace("H-", "")
        hyp = line.split("\t")[2]
        hyp_idx.append((int(idx), hyp))
hyp_idx = sorted(hyp_idx, key=lambda item: item[0])
for s,t,hi in zip(src_lines,tgt_lines,hyp_idx):
    print("%s\t%s\t%s" % (s,hi[1],t))
