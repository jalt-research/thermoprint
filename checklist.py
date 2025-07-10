import sys

text_in = list(sys.stdin)
print(text_in)
items = [line.split('.')[1][:-1] for line in text_in[1:]]
out = ':br :br :br +big +em Todos -em :date -big :hr :br '
for item in items:
    out = out + '[ ] ' + item + ' :br :br '
out = out + ' :br '

print(out)
