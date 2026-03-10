import re
import json
import urllib.request
import urllib.parse
import time

filepath = "movie_recommender.py"
api_key = "15d2ea6d0dc1d476efbca3eba2b9bbfb"

corrupted_titles = [
    "Se7en", "The Lion King", "Howl's Moving Castle", "Zodiac", 
    "Everything Everywhere All at Once", "Avengers: Endgame", 
    "Life Is Beautiful", "Das Boot", "Braveheart", "Catch Me If You Can", 
    "Wind River", "The Imitation Game", "Kubo and the Two Strings", 
    "Schindler's List", "The Matrix", "Forrest Gump", 
    "The Silence of the Lambs", "The Departed", "Spirited Away", 
    "Parasite", "Goodfellas", "Seven Samurai", "City of God", 
    "The Green Mile", "It's a Wonderful Life", "Interstellar", 
    "Gladiator", "12 Angry Men", "Fight Club", 
    "The Lord of the Rings: The Fellowship of the Ring", 
    "Spider-Man: Into the Spider-Verse", "Whiplash", "The Prestige", 
    "Back to the Future", "Alien", "Terminator 2", "The Shining", 
    "A Clockwork Orange", "The Truman Show", "Jurassic Park"
]

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    for title in corrupted_titles:
        if f'"title": "{title}"' in line:
            # Re-fetch from TMDB
            query = urllib.parse.quote(title)
            url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=5)
                data = json.loads(resp.read())
                
                if data.get('results') and len(data['results']) > 0:
                    real_poster = data['results'][0].get('poster_path')
                    if real_poster:
                        # Strip any existing poster path from string
                        clean_line = re.sub(r',\s*"poster_path":\s*"[^"]+"', '', line)
                        # Inject new poster path
                        lines[i] = re.sub(r'\},(\s*)$', f', "poster_path": "{real_poster}"}},\\1', clean_line)
                        count += 1
                        print(f"REPAIRED: {title} -> {real_poster}")
            except Exception as e:
                print(f"ERR {title}: {str(e)}")
            time.sleep(0.1)
            break # Once matched, move to next line

if count > 0:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"\nSaved {count} repaired posters to DB!")
