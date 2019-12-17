import sys
sys.path.append("..")
from helper_fn import align_by_symbol

from glob import glob
import os
import codecs
import json

INPUT_DIR   = "data_input"
CONTROL_DIR = "data_control"

def compare_files(name, sep):
    outp = name
    failed = False
    name_input   = INPUT_DIR + os.sep + name
    name_control = CONTROL_DIR + os.sep + name
    with codecs.open(name_input, 'r', encoding = "utf-8") as f:
        data_sample_input = f.read()

    with codecs.open(name_control, 'r', encoding = "utf-8") as f:
        data_sample_control = f.read()

    data_sample_test = align_by_symbol(data_sample_input, sep)

    lines_test    = data_sample_test.splitlines(True)
    lines_control = data_sample_control.splitlines(True)

    for i, pair in enumerate(zip(lines_test, lines_control)):
        if pair[0] != pair[1]:
            failed = True
            outp += f"\nLine {i + 1}\n"
            outp += f"REQUIRED: {pair[1]}"
            outp += f"PROVIDED: {pair[0]}"
    if not failed:
        outp += ": PASSED"
    print(outp)

with codecs.open("seps.json", "r", encoding = "utf-8") as f:
    seps = json.loads(f.read())["seps"]
print(seps)
for k, v in seps.items():
    compare_files(k, v)

"""
fnames = glob(INPUT_DIR + os.sep + "*")
fnames = [x.split(os.sep)[-1] for x in fnames]

for fname in fnames:
    compare_files(fname)
"""