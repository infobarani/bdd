import csv
import re
import os
import glob

durations = {}
with open('spec.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        state, duration_ms = row
        durations[f"{state}_DURATION_SECONDS"] = str(int(duration_ms) // 1000)

def replace_placeholders(match):
    expression = match.group(1)
    for placeholder, value in durations.items():
        expression = re.sub(r'\b' + placeholder + r'\b', value, expression)
    return str(eval(expression))

for in_file in glob.glob(os.path.join('..', 'features', '*.feature.in')):
    with open(in_file, 'r') as f_in:
        content = f_in.read()

    # The regex should find anything between { and }
    content = re.sub(r'\{([^}]+)\}', replace_placeholders, content)

    out_file = os.path.splitext(in_file)[0] + '.feature'
    with open(out_file, 'w') as f_out:
        f_out.write(content)