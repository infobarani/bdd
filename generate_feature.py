import csv
import re

durations = {}
with open('spec.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        state, duration_ms = row
        durations[f"{state}_DURATION_SECONDS"] = str(int(duration_ms) // 1000)

with open('features/traffic_light.feature.in', 'r') as f_in:
    content = f_in.read()

def replace_placeholders(match):
    expression = match.group(1)
    for placeholder, value in durations.items():
        expression = re.sub(r'\b' + placeholder + r'\b', value, expression)
    return str(eval(expression))

# The regex should find anything between { and }
content = re.sub(r'\{([^}]+)\}', replace_placeholders, content)

with open('features/traffic_light.feature', 'w') as f_out:
    f_out.write(content)