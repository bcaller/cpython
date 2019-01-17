import re
import sys


remainder = re.compile(r"[^\[]*\[(.*)\]$")
operator = re.compile(r"\|0x[^|]+\|0x[^|]+\|([A-Z].+)$")

previous_endlen = None

text = remainder.match(next(sys.stdin)).groups(1)[0]

codes = []

marks = []

line_counter = 0
code_counter = 0
discard_counter = 0
jump_counter = 0

for line in sys.stdin:
    line = line.strip()
    rem = remainder.match(line)
    if rem:
        ops = '; '.join(codes)
        end_len = len(rem.groups(1)[0])
        if end_len == previous_endlen:
            continue
        del codes[:]
        sys.stdout.write(' {}\n'.format(ops))
        if end_len == 0:
            sys.stdout.write("\033[45;1m{}\033[0m".format(text))
        else:
            sys.stdout.write("\033[45;1m{}\033[0m\033[46;1m{}\033[0m".format(text[:-end_len], text[-end_len:]))
        previous_endlen = end_len
        line_counter += 1
        continue
    op = operator.match(line)
    if op:
        code = op.groups(1)[0]
        codes.append(code)
        code_counter += 1
        if code.startswith("JUMP"):
            jump_counter += 1
        elif code.startswith("MARK "):
            position = len(text) - previous_endlen
            mark_index = int(code.split(" ")[1])
            if len(marks) <= mark_index:
                marks.append(position)
            else:
                marks[mark_index] = position
            codes.append("{}".format(marks[:(mark_index + 1)]))
        #print("\033[1m{}\033[0m".format(op.groups(1)[0]))
        continue
    if line.startswith("discard"):
        #print("\033[31mBacktrack\033[0m")
        discard_counter += 1
        continue

print("\n")
print("%d lines" % line_counter)
print("%d codes" % code_counter)
print("%d discards" % discard_counter)
print("%d jumps" % jump_counter)
