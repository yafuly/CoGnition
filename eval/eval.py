import sys
import re
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("text_path", type=str, help="path to texts with test sentences, compounds and sentence translations, separted by '\t'")
parser.add_argument("lexicon_path", type=str, help="path to povided lexicon")
args = parser.parse_args()

lexicon_lines = open(args.lexicon_path).readlines()
lexicon = {}
for line in lexicon_lines:
    src, trans = line.strip().split("\t")
    lexicon[src] = trans

# atom list
P = ["about", "around", "before", "behind", "except", "for", "from", "inside", "like", "near", "on", "to", "toward", "towards", "under", "with", "without"]
V = ["asked","visited","heard","lost","hated","stopped","woke","found","watched","took","saw","told","caught","liked","left","gave","invited","met","chose",]
DET = ["the","every","any","another","each"]
ADJ = ["small","red","dirty","lazy","smart","large","special","silly","quiet","empty","fake"]
N = ["dog","doctor","sandwich","hat","waiter","lawyer","peanut","farmer","car","girl","boyfriend","child","chair","building","clown","bee","apartment","farm","airplane"]
MOD = ["mod0","mod1","mod2",]
ATOM_TYPE2LIST = {"P":P, "V":V, "DET":DET, "ADJ":ADJ, "N":N, "MOD":MOD}

# regularize modifiers
def _reg_mod(ph):
    mods = {"he liked":"mod0", "at the store":"mod1", "on the floor":"mod2"}
    for k,v in mods.items():
        ph = ph.replace(k, v)
    return ph.split()

def _get_atom_state(compound, hyp, state):
    for atom in compound:
        for k,v in ATOM_TYPE2LIST.items():
            if atom in v:
                atype = k
        trans = lexicon[atom]
        state[atype] = dict.fromkeys(["trans", "pos"]) 
        if trans == "/":
            state[atype]["trans"] = "P1"
            state[atype]["pos"] = []
        else:
            pos_list = []
            for t in trans.split("/"):
                pos_list += [m.start() for m in re.finditer(t, hyp)]
            if len(pos_list) > 0:
                state[atype]["trans"] = "P1"
                state[atype]["pos"] =  [min(pos_list), max(pos_list)] 
            else:
                state[atype]["trans"] = "P0"
                state[atype]["pos"] = []
            
def _obtain_pos(typ, state):    
    if state[typ] is not None:
        return state[typ]["pos"]
    else:
        return []

def _get_order_flag(pos1, pos2):
    # return "P1" if pos1 < pos2 or either of them is None
    if len(pos1) > 0 and len(pos2) > 0:
        os = "P1" if min(pos1) < max(pos2) else "P0"
    else:
        os = "P1"
    return os

text_lines = open(args.text_path, 'r').readlines()
compound_flag = []
for line in text_lines:
    line = line.strip()
    src, compound, hyp = line.split("\t")
    assert compound in src, "Compound can not be found in given sentence."
    compound = _reg_mod(compound)
    hyp = hyp.replace("@@ ","").replace(" ","") # squeeze cn chars
    atom_types = ["P", "V", "DET", "ADJ", "N", "MOD"]
    atom_state = dict.fromkeys(atom_types)
    _get_atom_state(compound, hyp, atom_state)

    # 1. All atom translation should be included
    trans_flag = []
    for k,v in atom_state.items():
        if v is not None:
            trans_flag.append(v["trans"])
    # if there exists atom that is not translated, then translation order is no longer needed to be considerd.
    if "P0" in trans_flag:
        compound_flag.append("-".join(trans_flag)+"/P0")
        continue
        
    # 2. Typical word order should be adjusted or maintained
    # Position: DET/ADJ/MOD < N
    V_pos = _obtain_pos("V", atom_state)
    DET_pos = _obtain_pos("DET", atom_state)
    ADJ_pos = _obtain_pos("ADJ", atom_state)
    MOD_pos = _obtain_pos("MOD", atom_state)
    N_pos = _obtain_pos("N", atom_state)
    order_flag = []
    order_flag.append(_get_order_flag(DET_pos, N_pos))
    order_flag.append(_get_order_flag(ADJ_pos, N_pos))
    if len(V_pos) == 0:
        # In some cases of verb-phrases, MOD can also be interpreted as modifiers of verbs, e.g., 'bought the car at the store' . Therefore, 'MOD_pos < N_pos' position does not strictly hold for VP.
        order_flag.append(_get_order_flag(MOD_pos, N_pos))
    _flag = "-".join(trans_flag) + "/" + "-".join(order_flag)
    compound_flag.append(_flag)
    
# Print result
# Flag "P0" denotes error in compound translation.
# Error in atom trasnlation and translation order is separated by "/".
for h,m in zip(text_lines, compound_flag):
    h = h.strip()
    m = m.strip()
    print("%s\t%s" % (h,m))

# Compute instance-level and aggregate-level error rate
num_contexts = 5
instance_flag = []
aggregation_flag = []
cache = []
for i,cflag in enumerate(compound_flag):
    iflag = 0 if "P0" in cflag else 1
    instance_flag.append(iflag)
    cache.append(iflag)
    # aggregating all 5 contexts
    # correct only if compound translations are correct under all 5 contexts
    if len(cache) > 4:
        aflag = 1 if sum(cache) == 5 else 0
        aggregation_flag.append(aflag)
        cache = []

def _err_rate(l):
    return (len(l)-sum(l))/len(l)
ins_err_rate = _err_rate(instance_flag)
print("=============================================")
print("# of test samples: %d" % (len(compound_flag)))
print("Instance-level error rate:" + "{0:.3%}".format(ins_err_rate))
agg_err_rate = _err_rate(aggregation_flag)
print("Aggregate-level error rate:" + "{0:.3%}".format(agg_err_rate))

