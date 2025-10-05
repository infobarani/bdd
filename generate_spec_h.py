import csv
import os

output_dir = 'lib'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open('spec.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    with open(os.path.join(output_dir, 'spec.h'), 'w') as hf:
        hf.write("#ifndef SPEC_H\n")
        hf.write("#define SPEC_H\n\n")
        for row in reader:
            state, duration_ms = row
            hf.write(f"#define {state}_DURATION_MS {duration_ms}\n")
        hf.write("\n#endif /* SPEC_H */\n")