import re
import json
import urllib.request
import urllib.parse
import os
import time

filepath = "c:/Users/User/Documents/movie_recommender/movie_recommender.py"
api_key = "15d2ea6d0dc1d476efbca3eba2b9bbfb"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines):
    if '"id":' in line and '{"id":' in line:
        if '"poster_path"' not in line:
            # Extract title
            title_match = re.search(r'"title":\s*"([^"]+)"', line)
            year_match = re.search(r'"year":\s*(\d+)', line)
            if title_match:
                title = title_match.group(1)
                year = year_match.group(1) if year_match else None
                
                query = urllib.parse.quote(title)
                url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
                if year:
                    url += f"&year={year}"
                
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    resp = urllib.request.urlopen(req)
                    data = json.loads(resp.read())
                    if data.get('results') and len(data['results']) > 0:
                        poster = data['results'][0].get('poster_path')
                        if poster:
                            # Inject into line
                            lines[i] = re.sub(r'\},(\s*)$', f', "poster_path": "{poster}"}},\\1', line)
                            count += 1
                            print(f"Patched: {title} -> {poster}")
                        else:
                            print(f"No poster found for: {title}")
                    else:
                        print(f"No results for: {title}")
                        
                    time.sleep(0.1) # Rate limit protection
                except Exception as e:
                    print(f"Error querying {title}: {str(e)}")

if count > 0:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"\nSuccessfully patched {count} movies!")
else:
    print("\nNo movies needed patching or zero successes.")
