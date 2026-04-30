def downsample(filename, factor=2):
    with open(filename, 'r') as f:
        data = f.read().strip()
    # parse the scheme list string
    # it's in format '((x y) (x y) ...)
    # let's just use regex or split
    import re
    points = re.findall(r'\((\-?\d+)\s+(\-?\d+)\)', data)
    sampled = points[::factor]
    # make sure to include the last point to close the loop if it was closed
    if points[-1] not in sampled:
        sampled.append(points[-1])
    return sampled

horse = downsample('horse_points.txt', 2)
jockey = downsample('jockey_points.txt', 2)

def to_scheme(name, pts):
    s = f"(define {name} '("
    s += " ".join([f"({p[0]} {p[1]})" for p in pts])
    s += "))"
    return s

with open('final_points.scm', 'w') as f:
    f.write(to_scheme('horse-points', horse) + "\n")
    f.write(to_scheme('jockey-points', jockey) + "\n")

print(f"Horse: {len(horse)}, Jockey: {len(jockey)}")
