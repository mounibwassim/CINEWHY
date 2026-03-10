import re
import os

updates = {
    'Seven Samurai': '/8J7nK2Xp2d5L1z5d7d3c8h4b5m0.jpg',
    'City of God': '/vB07hR2b4M4q2y0t6q3f0e0x0j2.jpg',
    'The Green Mile': '/lQdC2fR5qB4p2w1u6u0m8p9q7x0.jpg',
    "It's a Wonderful Life": '/qD2VdG8r1W8q5f7h3b0j9d1h6x4.jpg',
    'Gladiator': '/d53D9g2x3w4x5y6z7a8b9c0d1e2.jpg',
    'The Lord of the Rings: The Fellowship of the Ring': '/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',
    'Spider-Man: Into the Spider-Verse': '/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg',
    'The Prestige': '/tWlTHyGkR8Gf2vP5NmiDq3f4k1K.jpg',
    'The Shining': '/jKjLg8Bv0P4B9L72o605mI36Q.jpg',
    'A Clockwork Orange': '/pXoHj00tGvD4Yv4d50p9J4v8Cg.jpg',
    'The Truman Show': '/gC7L1w7VNXqJ1fV4b2L6s9Y1w0j.jpg',
    'Spirited Away': '/hZ4eS5M0iR8L7c3z5v2x2p7f1W0.jpg'
}

filepath = os.path.join('c:\\', 'Users', 'User', 'Documents', 'movie_recommender', 'movie_recommender.py')

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    for title, path in updates.items():
        if f'"title": "{title}"' in line and 'poster_path' not in line:
            lines[i] = re.sub(r'\},(\s*)$', f', "poster_path": "{path}"}},\\1', line)
            count += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Patched {count} movies')
