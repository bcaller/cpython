import re
import sys


remainder = re.compile(r"[^\[]*\[(.*)\]$")
operator = re.compile(r"\|0x[^|]+\|0x[^|]+\|([A-Z].+)$")
colors = ["\033[45;1m", "\033[43;1m", "\033[41;1m", "\033[42;1m"]

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
        sys.stdout.write(' {}\n'.format(ops[:120]))
        head, tail = (
            (text, '')
            if end_len == 0 else
            (text[:-end_len], text[-end_len:])
        )
        split_head = [[x, False] for x in head]
        for m in marks:
            if m is not None and m != 0 and m < len(split_head):
                split_head[m][1] = True
        merged_head = ""
        current_m = 0
        for letter, is_mark in split_head:
            if is_mark:
                current_m += 1
            merged_head = "{0}{1}{2}".format(merged_head, colors[current_m % len(colors)], letter)
        merged_tail = tail
        sys.stdout.write("\033[38;2;255;255;255m\033[48;2;255;0;255m{}\033[0m\033[46;1m{}\033[0m".format(merged_head, merged_tail))
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
            marks = [(m if m is not None and m <= (len(text) - previous_endlen) else None) for m in marks]
        elif code.startswith("MARK "):
            position = len(text) - previous_endlen
            mark_index = int(code.split(" ")[1])
            if len(marks) > mark_index:
                marks[mark_index] = position
            else:
                while len(marks) < mark_index:
                    marks.append(None)
                marks.append(position)
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
