import numpy as np

def generate_spline(pts, num_points=5):
    pts = np.array(pts)
    out = []
    for i in range(len(pts)-1):
        p0 = pts[max(i-1, 0)]
        p1 = pts[i]
        p2 = pts[i+1]
        p3 = pts[min(i+2, len(pts)-1)]
        
        for t in np.linspace(0, 1, num_points, endpoint=False):
            t2 = t*t
            t3 = t2*t
            v = 0.5 * ((2 * p1) +
                       (-p0 + p2) * t +
                       (2*p0 - 5*p1 + 4*p2 - p3) * t2 +
                       (-p0 + 3*p1 - 3*p2 + p3) * t3)
            out.append(v)
    out.append(pts[-1])
    return np.array(out)

horse_rough = [
    (240, 90), (220, 110), (200, 140), (180, 145), (140, 130), # head and upper neck
    (60, 120), (-50, 115), (-150, 110), (-220, 100), # back
    (-280, 70), (-350, 60), (-380, 50), (-350, 30), (-280, 40), # tail
    (-250, 20), (-270, -40), (-320, -100), (-380, -160), (-404, -180), # hind leg down
    (-380, -200), (-360, -180), (-340, -140), (-270, -80), (-200, -40), # hind leg up
    (-100, -50), (0, -55), (60, -50), # belly
    (100, -80), (130, -130), (100, -170), (110, -190), (130, -180), # front leg down
    (140, -150), (160, -100), (170, -50), (180, -10), # front leg up
    (190, 40), (210, 60), (230, 75), (240, 90) # chest to jaw to nose
]

smooth_horse = generate_spline(horse_rough, 3)

scheme_list = "'" + "(" + " ".join([f"({int(p[0])} {int(p[1])})" for p in smooth_horse]) + ")"
print("Horse points:", len(smooth_horse))
with open('horse_points.txt', 'w') as f:
    f.write(scheme_list)

jockey_rough = [
    (-30, 115), (-10, 160), (10, 200), (30, 220), (50, 210), (45, 190), 
    (30, 175), (50, 150), (80, 120), (100, 110), (70, 130), (40, 150),
    (10, 120), (30, 90), (40, 60), (30, 40), (10, 80), (-30, 115)
]
smooth_jockey = generate_spline(jockey_rough, 3)
jockey_list = "'" + "(" + " ".join([f"({int(p[0])} {int(p[1])})" for p in smooth_jockey]) + ")"
with open('jockey_points.txt', 'w') as f:
    f.write(jockey_list)

print("Done")
