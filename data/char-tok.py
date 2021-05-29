def _chartok(line):
    new_line = re.sub(r'(?<=[\u4e00-\u9fff]{1})([\u4e00-\u9fff])', r' \1', line)
    new_line = re.sub(r'(?<=[^ ])(\<\<unk\>\>)', r' \1', new_line)
    return new_line

for t in ['trian.zh', 'valid.zh', 'test.zh']: