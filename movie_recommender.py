"""
=======================================================
  CineLogic — Rule-Based Movie Recommendation System
  Pure Python · No ML · No file imports required
  220 curated films hardcoded · Forward-chaining engine
=======================================================
"""

from typing import List, Dict, Any, Optional, Tuple, cast

# =====================================================================
# SECTION 1 — HARDCODED MOVIE DATABASE (220 films)
# =====================================================================
# Fields: id, title, year, genres, rating (0-10), votes, runtime (min), popularity

MOVIES: List[Dict[str, Any]] = [
    {"id": 1,   "title": "The Godfather",                         "year": 1972, "genres": ["Drama","Crime"],                              "rating": 9.2, "votes": 1900000, "runtime": 175, "poster_path": "/3bhkrj0eFv469S9YmS1S96v9v6p.jpg"},
    {"id": 2,   "title": "The Shawshank Redemption",              "year": 1994, "genres": ["Drama"],                                     "rating": 9.3, "votes": 2700000, "runtime": 142, "poster_path": "/q6y0Go1tsMnUjk6YRsFYqU83pS8.jpg"},
    {"id": 3,   "title": "Schindler's List",                      "year": 1993, "genres": ["Drama","History","War"],                     "rating": 9.0, "votes": 1400000, "runtime": 195, "poster_path": "/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"},
    {"id": 4,   "title": "The Dark Knight",                       "year": 2008, "genres": ["Action","Crime","Drama"],                    "rating": 9.0, "votes": 2700000, "runtime": 152, "poster_path": "/qJ2tW6WMUDp9p1u3TUMXnO30IEV.jpg"},
    {"id": 5,   "title": "Pulp Fiction",                          "year": 1994, "genres": ["Crime","Drama","Thriller"],                  "rating": 8.9, "votes": 2100000, "runtime": 154, "poster_path": "/d5iIl9h9btztp90Y0Y0Y0Y0Y0Y0.jpg"},
    {"id": 6,   "title": "Inception",                             "year": 2010, "genres": ["Action","Adventure","Sci-Fi"],               "rating": 8.8, "votes": 2400000, "runtime": 148, "poster_path": "/edv5CZvfk0YRMjbPVogyzPbPQTM.jpg"},
    {"id": 7,   "title": "Fight Club",                            "year": 1999, "genres": ["Drama","Thriller"],                         "rating": 8.8, "votes": 2100000, "runtime": 139, "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"},
    {"id": 8,   "title": "Interstellar",                          "year": 2014, "genres": ["Adventure","Drama","Sci-Fi"],                "rating": 8.7, "votes": 1900000, "runtime": 169, "poster_path": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"},
    {"id": 9,   "title": "Goodfellas",                            "year": 1990, "genres": ["Crime","Drama"],                            "rating": 8.7, "votes": 1100000, "runtime": 146, "poster_path": "/9OkCLM73MIU2CrKZbqiT8Ln1wY2.jpg"},
    {"id": 10,  "title": "The Matrix",                            "year": 1999, "genres": ["Action","Sci-Fi"],                          "rating": 8.7, "votes": 1900000, "runtime": 136, "poster_path": "/p96dm7sCMn4VYAStA6siNz30G1r.jpg"},
    {"id": 11,  "title": "Forrest Gump",                          "year": 1994, "genres": ["Drama","Romance"],                          "rating": 8.8, "votes": 2000000, "runtime": 142, "poster_path": "/saHP97rTPS5eLmrLQEcANmKrsFl.jpg"},
    {"id": 12,  "title": "The Silence of the Lambs",              "year": 1991, "genres": ["Crime","Drama","Thriller"],                  "rating": 8.6, "votes": 1500000, "runtime": 118, "poster_path": "/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg"},
    {"id": 13,  "title": "Se7en",                                 "year": 1995, "genres": ["Crime","Drama","Mystery","Thriller"],        "rating": 8.6, "votes": 1700000, "runtime": 127, "poster_path": "/191nKfP0ehp3uIvWqgPbFmI4lv9.jpg"},
    {"id": 14,  "title": "The Departed",                          "year": 2006, "genres": ["Crime","Drama","Thriller"],                  "rating": 8.5, "votes": 1400000, "runtime": 151, "poster_path": "/nT97ifVT2J1yMQmeq20Qblg61T.jpg"},
    {"id": 15,  "title": "Spirited Away",                         "year": 2001, "genres": ["Animation","Adventure","Family","Fantasy"],  "rating": 8.6, "votes": 750000,  "runtime": 125, "poster_path": "/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"},
    {"id": 16,  "title": "Parasite",                              "year": 2019, "genres": ["Drama","Thriller"],                         "rating": 8.5, "votes": 780000,  "runtime": 132, "poster_path": "/4DGPORlVIDIQvsuSDnM4uXKMjWS.jpg"},
    {"id": 17,  "title": "Whiplash",                              "year": 2014, "genres": ["Drama","Music"],                            "rating": 8.5, "votes": 830000,  "runtime": 107, "poster_path": "/7fn624j5lj3xTme2SgiLCeuedmO.jpg"},
    {"id": 18,  "title": "The Grand Budapest Hotel",              "year": 2014, "genres": ["Adventure","Comedy","Crime"],                "rating": 8.1, "votes": 810000,  "runtime": 99, "poster_path": "/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg"},
    {"id": 19,  "title": "No Country for Old Men",                "year": 2007, "genres": ["Crime","Drama","Thriller","Western"],        "rating": 8.2, "votes": 1000000, "runtime": 122, "poster_path": "/6d5XOczc226jECq0LIX0siKtgHR.jpg"},
    {"id": 20,  "title": "There Will Be Blood",                   "year": 2007, "genres": ["Drama","Western"],                          "rating": 8.2, "votes": 530000,  "runtime": 158, "poster_path": "/fa0RDkAlCec0STeMNAhPaF89q6U.jpg"},
    {"id": 21,  "title": "2001: A Space Odyssey",                 "year": 1968, "genres": ["Adventure","Sci-Fi"],                       "rating": 8.3, "votes": 670000,  "runtime": 149, "poster_path": "/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg"},
    {"id": 22,  "title": "Blade Runner",                          "year": 1982, "genres": ["Action","Drama","Sci-Fi","Thriller"],        "rating": 8.1, "votes": 750000,  "runtime": 117, "poster_path": "/63N9uy8nd9j7Eog2axPQ8lbr3Wj.jpg"},
    {"id": 23,  "title": "Blade Runner 2049",                     "year": 2017, "genres": ["Action","Drama","Sci-Fi"],                  "rating": 8.0, "votes": 560000,  "runtime": 164, "poster_path": "/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"},
    {"id": 24,  "title": "Mad Max: Fury Road",                    "year": 2015, "genres": ["Action","Adventure","Sci-Fi"],              "rating": 8.1, "votes": 1000000, "runtime": 120, "poster_path": "/hA2ple9q4qnwxp3hKVNhroipsir.jpg"},
    {"id": 25,  "title": "The Thing",                             "year": 1982, "genres": ["Horror","Mystery","Sci-Fi"],                "rating": 8.1, "votes": 450000,  "runtime": 109, "poster_path": "/tzGY49kseSE9QAKk47uuDGwnSCu.jpg"},
    {"id": 26,  "title": "Alien",                                 "year": 1979, "genres": ["Horror","Sci-Fi"],                          "rating": 8.5, "votes": 870000,  "runtime": 117, "poster_path": "/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg"},
    {"id": 27,  "title": "Aliens",                                "year": 1986, "genres": ["Action","Adventure","Sci-Fi","Thriller"],   "rating": 8.4, "votes": 720000,  "runtime": 137, "poster_path": "/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg"},
    {"id": 28,  "title": "Terminator 2",                          "year": 1991, "genres": ["Action","Sci-Fi"],                          "rating": 8.6, "votes": 1100000, "runtime": 137, "poster_path": "/jFTVD4XoWQTcg7wdyJKa8PEds5q.jpg"},
    {"id": 29,  "title": "Back to the Future",                    "year": 1985, "genres": ["Adventure","Comedy","Sci-Fi"],              "rating": 8.5, "votes": 1200000, "runtime": 116, "poster_path": "/vN5B5WgYscRGcQpVhHl6p9DDTP0.jpg"},
    {"id": 30,  "title": "E.T.",                                  "year": 1982, "genres": ["Adventure","Family","Sci-Fi"],              "rating": 7.9, "votes": 400000,  "runtime": 115, "poster_path": "/an0nD6uq6byfxXCfk6lQBzdL2J1.jpg"},
    {"id": 31,  "title": "Jurassic Park",                         "year": 1993, "genres": ["Action","Adventure","Sci-Fi","Thriller"],   "rating": 8.2, "votes": 970000,  "runtime": 127, "poster_path": "/maFjKnJ62hDQ9E66dKqDZgbUy0H.jpg"},
    {"id": 32,  "title": "Raiders of the Lost Ark",               "year": 1981, "genres": ["Action","Adventure"],                       "rating": 8.4, "votes": 970000,  "runtime": 115, "poster_path": "/ceG9VzoRAVGwivFU403Wc3AHRys.jpg"},
    {"id": 33,  "title": "Star Wars: A New Hope",                 "year": 1977, "genres": ["Action","Adventure","Fantasy","Sci-Fi"],    "rating": 8.6, "votes": 1300000, "runtime": 121, "poster_path": "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg"},
    {"id": 34,  "title": "The Empire Strikes Back",               "year": 1980, "genres": ["Action","Adventure","Fantasy","Sci-Fi"],    "rating": 8.7, "votes": 1200000, "runtime": 124, "poster_path": "/nNAeTmF4CtdSgMDplXTDPOpYzsX.jpg"},
    {"id": 35,  "title": "Apocalypse Now",                        "year": 1979, "genres": ["Drama","War"],                             "rating": 8.4, "votes": 680000,  "runtime": 153, "poster_path": "/gQB8Y5RCMkv2zwzFHbUJX3kAhvA.jpg"},
    {"id": 36,  "title": "Full Metal Jacket",                     "year": 1987, "genres": ["Drama","War"],                             "rating": 8.3, "votes": 740000,  "runtime": 116, "poster_path": "/kMKyx1k8hWWscYFnPbnxxN4Eqo4.jpg"},
    {"id": 37,  "title": "Saving Private Ryan",                   "year": 1998, "genres": ["Drama","War"],                             "rating": 8.6, "votes": 1400000, "runtime": 169, "poster_path": "/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg"},
    {"id": 38,  "title": "Dunkirk",                               "year": 2017, "genres": ["Action","Drama","History","Thriller","War"],"rating": 7.9, "votes": 760000,  "runtime": 106, "poster_path": "/b4Oe15CGLL61Ped0RAS9JpqdmCt.jpg"},
    {"id": 39,  "title": "1917",                                  "year": 2019, "genres": ["Drama","Thriller","War"],                   "rating": 8.3, "votes": 500000,  "runtime": 119, "poster_path": "/iZf0KyrE25z1sage4SYFLCCrMi9.jpg"},
    {"id": 40,  "title": "Hacksaw Ridge",                         "year": 2016, "genres": ["Drama","History","War"],                    "rating": 8.1, "votes": 430000,  "runtime": 139, "poster_path": "/fnOMP6mjmOmZwmlC1n0K7ivrzt1.jpg"},
    {"id": 41,  "title": "Casablanca",                            "year": 1942, "genres": ["Drama","Romance","War"],                    "rating": 8.5, "votes": 580000,  "runtime": 102, "poster_path": "/lGCEKlJo2CnWydQj7aamY7s1S7Q.jpg"},
    {"id": 42,  "title": "Citizen Kane",                          "year": 1941, "genres": ["Drama","Mystery"],                         "rating": 7.9, "votes": 440000,  "runtime": 119, "poster_path": "/sav0jxhqiH0bPr2vZFU0Kjt2nZL.jpg"},
    {"id": 43,  "title": "Sunset Boulevard",                      "year": 1950, "genres": ["Drama","Film-Noir","Thriller"],             "rating": 8.4, "votes": 300000,  "runtime": 110, "poster_path": "/zt8aQ6ksqK6p1AopC5zVTDS9pKT.jpg"},
    {"id": 44,  "title": "Rear Window",                           "year": 1954, "genres": ["Mystery","Thriller"],                       "rating": 8.5, "votes": 480000,  "runtime": 112, "poster_path": "/ILVF0eJxHMddjxeQhswFtpMtqx.jpg"},
    {"id": 45,  "title": "Vertigo",                               "year": 1958, "genres": ["Mystery","Romance","Thriller"],             "rating": 8.3, "votes": 360000,  "runtime": 128, "poster_path": "/15uOEfqBNTVtDUT7hGBVCka0rZz.jpg"},
    {"id": 46,  "title": "Psycho",                                "year": 1960, "genres": ["Horror","Mystery","Thriller"],              "rating": 8.5, "votes": 680000,  "runtime": 109, "poster_path": "/yz4QVqPx3h1hD1DfqqQkCq3rmxW.jpg"},
    {"id": 47,  "title": "North by Northwest",                    "year": 1959, "genres": ["Action","Adventure","Mystery","Thriller"],  "rating": 8.3, "votes": 310000,  "runtime": 136, "poster_path": "/kNOFPQrel9YFCVzI0DF8FnCEpCw.jpg"},
    {"id": 48,  "title": "Some Like It Hot",                      "year": 1959, "genres": ["Comedy","Romance"],                         "rating": 8.2, "votes": 300000,  "runtime": 121, "poster_path": "/hVIKyTK13AvOGv7ICmJjK44DTzp.jpg"},
    {"id": 49,  "title": "12 Angry Men",                          "year": 1957, "genres": ["Crime","Drama"],                           "rating": 9.0, "votes": 830000,  "runtime": 96, "poster_path": "/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg"},
    {"id": 50,  "title": "To Kill a Mockingbird",                 "year": 1962, "genres": ["Crime","Drama"],                           "rating": 8.3, "votes": 370000,  "runtime": 129, "poster_path": "/gZycFUMLx2110dzK3nBNai7gfpM.jpg"},
    {"id": 51,  "title": "Lawrence of Arabia",                    "year": 1962, "genres": ["Adventure","Biography","Drama","History"],  "rating": 8.3, "votes": 280000,  "runtime": 228, "poster_path": "/AiAm0EtDvyGqNpVoieRw4u65vD1.jpg"},
    {"id": 52,  "title": "Once Upon a Time in the West",          "year": 1968, "genres": ["Drama","Western"],                          "rating": 8.5, "votes": 280000,  "runtime": 165, "poster_path": "/qbYgqOczabWNn2XKwgMtVrntD6P.jpg"},
    {"id": 53,  "title": "The Good, the Bad and the Ugly",        "year": 1966, "genres": ["Adventure","Western"],                      "rating": 8.8, "votes": 790000,  "runtime": 178, "poster_path": "/bX2xnavhMYjWDoZp1VM6VnU1xwe.jpg"},
    {"id": 54,  "title": "Chinatown",                             "year": 1974, "genres": ["Drama","Mystery","Thriller"],               "rating": 8.2, "votes": 380000,  "runtime": 130, "poster_path": "/kZRSP3FmOcq0xnBulqpUQngJUXY.jpg"},
    {"id": 55,  "title": "Taxi Driver",                           "year": 1976, "genres": ["Crime","Drama","Thriller"],                 "rating": 8.3, "votes": 820000,  "runtime": 114, "poster_path": "/ekstpH614fwDX8DUln1a2Opz0N8.jpg"},
    {"id": 56,  "title": "Raging Bull",                           "year": 1980, "genres": ["Biography","Drama","Sport"],               "rating": 8.2, "votes": 430000,  "runtime": 129, "poster_path": "/1WV7WlTS8LI1L5NkCgjWT9GSW3O.jpg"},
    {"id": 57,  "title": "Annie Hall",                            "year": 1977, "genres": ["Comedy","Drama","Romance"],                 "rating": 8.0, "votes": 330000,  "runtime": 93, "poster_path": "/dEtjPywhDbAXYjoFfhBC4U9unU7.jpg"},
    {"id": 58,  "title": "Monty Python and the Holy Grail",       "year": 1975, "genres": ["Adventure","Comedy","Fantasy"],             "rating": 8.2, "votes": 590000,  "runtime": 91, "poster_path": "/7nTkHjETdGMYK1phHwDbPsrzbYl.jpg"},
    {"id": 59,  "title": "The Princess Bride",                    "year": 1987, "genres": ["Adventure","Comedy","Family","Fantasy","Romance"], "rating": 8.1, "votes": 440000, "runtime": 98, "poster_path": "/2FC9L9MrjBoGHYjYZjdWQdopVYb.jpg"},
    {"id": 60,  "title": "Toy Story",                             "year": 1995, "genres": ["Animation","Adventure","Comedy","Family"],  "rating": 8.3, "votes": 1000000, "runtime": 81, "poster_path": "/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"},
    {"id": 61,  "title": "The Lion King",                         "year": 1994, "genres": ["Animation","Adventure","Drama","Family"],   "rating": 8.5, "votes": 1000000, "runtime": 88, "poster_path": "/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg"},
    {"id": 62,  "title": "Beauty and the Beast",                  "year": 1991, "genres": ["Animation","Family","Fantasy","Romance"],   "rating": 8.0, "votes": 490000,  "runtime": 84, "poster_path": "/hUJ0UvQ5tgE2Z9WpfuduVSdiCiU.jpg"},
    {"id": 63,  "title": "Aladdin",                               "year": 1992, "genres": ["Animation","Adventure","Comedy","Family","Fantasy"], "rating": 8.0, "votes": 530000, "runtime": 90, "poster_path": "/eLFfl7vS8dkeG1hKp5mwbm37V83.jpg"},
    {"id": 64,  "title": "Up",                                    "year": 2009, "genres": ["Animation","Adventure","Comedy","Family"],  "rating": 8.3, "votes": 980000,  "runtime": 96, "poster_path": "/mFvoEwSfLqbcWwFsDjQebn9bzFe.jpg"},
    {"id": 65,  "title": "WALL·E",                                "year": 2008, "genres": ["Animation","Adventure","Family","Sci-Fi"],  "rating": 8.4, "votes": 1100000, "runtime": 98, "poster_path": "/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg"},
    {"id": 66,  "title": "Finding Nemo",                          "year": 2003, "genres": ["Animation","Adventure","Comedy","Family"],  "rating": 8.2, "votes": 1000000, "runtime": 100, "poster_path": "/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg"},
    {"id": 67,  "title": "The Incredibles",                       "year": 2004, "genres": ["Animation","Action","Adventure","Family"],  "rating": 8.0, "votes": 1000000, "runtime": 115, "poster_path": "/2LqaLgk4Z226KkgPJuiOQ58wvrm.jpg"},
    {"id": 68,  "title": "Coco",                                  "year": 2017, "genres": ["Animation","Adventure","Comedy","Family","Fantasy"], "rating": 8.4, "votes": 500000, "runtime": 105, "poster_path": "/6Ryitt95xrO8KXuqRGm1fUuNwqF.jpg"},
    {"id": 69,  "title": "Soul",                                  "year": 2020, "genres": ["Animation","Comedy","Drama","Family"],      "rating": 8.1, "votes": 370000,  "runtime": 100, "poster_path": "/6jmppcaubzLF8wkXM36ganVISCo.jpg"},
    {"id": 70,  "title": "Inside Out",                            "year": 2015, "genres": ["Animation","Adventure","Comedy","Drama","Family"], "rating": 8.2, "votes": 680000, "runtime": 95, "poster_path": "/2H1TmgdfNtsKlU9jKdeNyYL5y8T.jpg"},
    {"id": 71,  "title": "Ratatouille",                           "year": 2007, "genres": ["Animation","Comedy","Family"],              "rating": 8.1, "votes": 680000,  "runtime": 111, "poster_path": "/t3vaWRPSf6WjDSamIkKDs1iQWna.jpg"},
    {"id": 72,  "title": "Spirited Away",                         "year": 2001, "genres": ["Animation","Adventure","Family","Fantasy"], "rating": 8.6, "votes": 750000,  "runtime": 125, "poster_path": "/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"},
    {"id": 73,  "title": "Princess Mononoke",                     "year": 1997, "genres": ["Animation","Action","Adventure","Fantasy"], "rating": 8.4, "votes": 400000,  "runtime": 134, "poster_path": "/cMYCDADoLKLbB83g4WnJegaZimC.jpg"},
    {"id": 74,  "title": "My Neighbor Totoro",                    "year": 1988, "genres": ["Animation","Family","Fantasy"],             "rating": 8.2, "votes": 320000,  "runtime": 86, "poster_path": "/rtGDOeG9LzoerkDGZF9dnVeLppL.jpg"},
    {"id": 75,  "title": "Grave of the Fireflies",                "year": 1988, "genres": ["Animation","Drama","War"],                  "rating": 8.5, "votes": 310000,  "runtime": 89, "poster_path": "/k9tv1rXZbOhH7eiCk378x61kNQ1.jpg"},
    {"id": 76,  "title": "Akira",                                 "year": 1988, "genres": ["Animation","Action","Sci-Fi","Thriller"],   "rating": 8.0, "votes": 280000,  "runtime": 124, "poster_path": "/neZ0ykEsPqxamsX6o5QNUFILQrz.jpg"},
    {"id": 77,  "title": "Ghost in the Shell",                    "year": 1995, "genres": ["Animation","Action","Crime","Sci-Fi"],      "rating": 8.0, "votes": 270000,  "runtime": 83, "poster_path": "/9gC88zYUBARRSThcG93MvW14sqx.jpg"},
    {"id": 78,  "title": "Howl's Moving Castle",                  "year": 2004, "genres": ["Animation","Adventure","Drama","Fantasy","Romance"], "rating": 8.2, "votes": 460000, "runtime": 119, "poster_path": "/13kOl2v0nD2OLbVSHnHk8GUFEhO.jpg"},
    {"id": 79,  "title": "Spider-Man: Into the Spider-Verse",     "year": 2018, "genres": ["Animation","Action","Adventure","Family","Sci-Fi"], "rating": 8.4, "votes": 580000, "runtime": 117, "poster_path": "/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"},
    {"id": 80,  "title": "The Social Network",                    "year": 2010, "genres": ["Biography","Drama","History"],              "rating": 7.8, "votes": 720000,  "runtime": 120, "poster_path": "/n0ybibhJtQ5icDqTp8eRytcIHJx.jpg"},
    {"id": 81,  "title": "The Big Short",                         "year": 2015, "genres": ["Biography","Comedy","Drama","History"],     "rating": 7.8, "votes": 480000,  "runtime": 130, "poster_path": "/scVEaJEwP8zUix8vgmMoJJ9Nq0w.jpg"},
    {"id": 82,  "title": "Spotlight",                             "year": 2015, "genres": ["Biography","Crime","Drama","History"],      "rating": 8.1, "votes": 470000,  "runtime": 129, "poster_path": "/8DPGG400FgaFWaqcv11n8mRd2NG.jpg"},
    {"id": 83,  "title": "Gone Girl",                             "year": 2014, "genres": ["Drama","Mystery","Thriller"],               "rating": 8.1, "votes": 850000,  "runtime": 149, "poster_path": "/ts996lKsxvjkO2yiYG0ht4qAicO.jpg"},
    {"id": 84,  "title": "Prisoners",                             "year": 2013, "genres": ["Crime","Drama","Mystery","Thriller"],       "rating": 8.1, "votes": 700000,  "runtime": 153, "poster_path": "/jsS3a3ep2KyBVmmiwaz3LvK49b1.jpg"},
    {"id": 85,  "title": "Sicario",                               "year": 2015, "genres": ["Action","Crime","Drama","Thriller"],        "rating": 7.6, "votes": 470000,  "runtime": 121, "poster_path": "/lz8vNyXeidqqOdJW9ZjnDAMb5Vr.jpg"},
    {"id": 86,  "title": "Nightcrawler",                          "year": 2014, "genres": ["Crime","Drama","Thriller"],                 "rating": 7.9, "votes": 560000,  "runtime": 117, "poster_path": "/j9HrX8f7GbZQm1BrBiR40uFQZSb.jpg"},
    {"id": 87,  "title": "Drive",                                 "year": 2011, "genres": ["Crime","Drama","Thriller"],                 "rating": 7.8, "votes": 660000,  "runtime": 100, "poster_path": "/602vevIURmpDfzbnv5Ubi6wIkQm.jpg"},
    {"id": 88,  "title": "Zodiac",                                "year": 2007, "genres": ["Crime","Drama","History","Mystery","Thriller"],"rating": 7.7, "votes": 470000, "runtime": 157, "poster_path": "/6YmeO4pB7XTh8P8F960O1uA14JO.jpg"},
    {"id": 89,  "title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "genres": ["Drama","Romance","Sci-Fi"],                 "rating": 8.3, "votes": 940000,  "runtime": 108, "poster_path": "/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg"},
    {"id": 90,  "title": "Her",                                   "year": 2013, "genres": ["Drama","Romance","Sci-Fi"],                 "rating": 8.0, "votes": 620000,  "runtime": 126, "poster_path": "/eCOtqtfvn7mxGl6nfmq4b1exJRc.jpg"},
    {"id": 91,  "title": "Ex Machina",                            "year": 2014, "genres": ["Drama","Sci-Fi","Thriller"],                "rating": 7.7, "votes": 550000,  "runtime": 108, "poster_path": "/dmJW8IAKHKxFNiUnoDR7JfsK7Rp.jpg"},
    {"id": 92,  "title": "Annihilation",                          "year": 2018, "genres": ["Adventure","Drama","Horror","Sci-Fi"],      "rating": 7.5, "votes": 330000,  "runtime": 115, "poster_path": "/4YRplSk6BhH6PRuE9gfyw9byUJ6.jpg"},
    {"id": 93,  "title": "Arrival",                               "year": 2016, "genres": ["Drama","Mystery","Sci-Fi"],                 "rating": 7.9, "votes": 620000,  "runtime": 116, "poster_path": "/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg"},
    {"id": 94,  "title": "Moon",                                  "year": 2009, "genres": ["Drama","Mystery","Sci-Fi"],                 "rating": 7.9, "votes": 320000,  "runtime": 97, "poster_path": "/35IU0Mq0zFsN1mYwDGts5mKc77n.jpg"},
    {"id": 95,  "title": "The Martian",                           "year": 2015, "genres": ["Adventure","Drama","Sci-Fi"],               "rating": 8.0, "votes": 840000,  "runtime": 144, "poster_path": "/3ndAx3weG6KDkJIRMCi5vXX6Dyb.jpg"},
    {"id": 96,  "title": "Gravity",                               "year": 2013, "genres": ["Drama","Sci-Fi","Thriller"],                "rating": 7.7, "votes": 800000,  "runtime": 91, "poster_path": "/kZ2nZw8D681aphje8NJi8EfbL1U.jpg"},
    {"id": 97,  "title": "Dune",                                  "year": 2021, "genres": ["Action","Adventure","Drama","Sci-Fi"],      "rating": 8.0, "votes": 690000,  "runtime": 155, "poster_path": "/d5NXSklXo0qyIYkgV94XAgMIckC.jpg"},
    {"id": 98,  "title": "Oppenheimer",                           "year": 2023, "genres": ["Biography","Drama","History","Thriller"],   "rating": 8.9, "votes": 570000,  "runtime": 180, "poster_path": "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"},
    {"id": 99,  "title": "Everything Everywhere All at Once",     "year": 2022, "genres": ["Action","Adventure","Comedy","Drama","Fantasy","Sci-Fi"], "rating": 8.0, "votes": 580000, "runtime": 139, "poster_path": "/u68AjlvlutfEIcpmbYpKcdi09ut.jpg"},
    {"id": 100, "title": "Joker",                                 "year": 2019, "genres": ["Crime","Drama","Thriller"],                 "rating": 8.4, "votes": 1200000, "runtime": 122, "poster_path": "/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"},
    {"id": 101, "title": "Avengers: Endgame",                     "year": 2019, "genres": ["Action","Adventure","Drama","Sci-Fi"],      "rating": 8.4, "votes": 1200000, "runtime": 181, "poster_path": "/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg"},
    {"id": 102, "title": "Knives Out",                            "year": 2019, "genres": ["Comedy","Crime","Drama","Mystery","Thriller"], "rating": 7.9, "votes": 590000, "runtime": 130, "poster_path": "/pThyQovXQrw2m0s9x82twj48Jq4.jpg"},
    {"id": 103, "title": "Glass Onion",                           "year": 2022, "genres": ["Comedy","Crime","Mystery","Thriller"],      "rating": 7.1, "votes": 280000,  "runtime": 139, "poster_path": "/vDGr1YdrlfbU9wxTOdpf3zChmv9.jpg"},
    {"id": 104, "title": "Get Out",                               "year": 2017, "genres": ["Horror","Mystery","Thriller"],              "rating": 7.7, "votes": 520000,  "runtime": 104, "poster_path": "/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"},
    {"id": 105, "title": "Hereditary",                            "year": 2018, "genres": ["Drama","Horror","Mystery","Thriller"],      "rating": 7.3, "votes": 280000,  "runtime": 127, "poster_path": "/hjlZSXM86wJrfCv5VKfR5DI2VeU.jpg"},
    {"id": 106, "title": "Midsommar",                             "year": 2019, "genres": ["Drama","Horror","Mystery","Thriller"],      "rating": 7.1, "votes": 250000,  "runtime": 148, "poster_path": "/7LEI8ulZzO5gy9Ww2NVCrKmHeDZ.jpg"},
    {"id": 107, "title": "A Quiet Place",                         "year": 2018, "genres": ["Drama","Horror","Mystery","Sci-Fi"],        "rating": 7.5, "votes": 460000,  "runtime": 90, "poster_path": "/nAU74GmpUk7t5iklEp3bufwDq4n.jpg"},
    {"id": 108, "title": "The Witch",                             "year": 2015, "genres": ["Horror","Mystery","Thriller"],              "rating": 6.9, "votes": 190000,  "runtime": 92, "poster_path": "/zap5hpFCWSvdWSuPGAQyjUv2wAC.jpg"},
    {"id": 109, "title": "The Lighthouse",                        "year": 2019, "genres": ["Drama","Fantasy","Horror","Mystery"],       "rating": 7.5, "votes": 230000,  "runtime": 109, "poster_path": "/f1tIYarTbkBdIT1aW0gzelDwknv.jpg"},
    {"id": 110, "title": "Pan's Labyrinth",                       "year": 2006, "genres": ["Drama","Fantasy","War"],                    "rating": 8.2, "votes": 630000,  "runtime": 118, "poster_path": "/z7xXihu5wHuSMWymq5VAulPVuvg.jpg"},
    {"id": 111, "title": "The Shape of Water",                    "year": 2017, "genres": ["Adventure","Drama","Fantasy","Romance"],    "rating": 7.3, "votes": 350000,  "runtime": 123, "poster_path": "/9zfwPffUXpBrEP26yp0q1ckXDcj.jpg"},
    {"id": 112, "title": "Amélie",                                "year": 2001, "genres": ["Comedy","Romance"],                         "rating": 8.3, "votes": 730000,  "runtime": 122, "poster_path": "/nSxDa3M9aMvGVLoItzWTepQ5h5d.jpg"},
    {"id": 113, "title": "Cinema Paradiso",                       "year": 1988, "genres": ["Drama","Romance"],                          "rating": 8.5, "votes": 250000,  "runtime": 155, "poster_path": "/gCI2AeMV4IHSewhJkzsur5MEp6R.jpg"},
    {"id": 114, "title": "Life is Beautiful",                     "year": 1997, "genres": ["Comedy","Drama","Romance","War"],           "rating": 8.6, "votes": 720000,  "runtime": 116, "poster_path": "/jtPq0g829wJb5d2S7i3h4e1c0d.jpg"},
    {"id": 115, "title": "Oldboy",                                "year": 2003, "genres": ["Action","Drama","Mystery","Thriller"],      "rating": 8.4, "votes": 560000,  "runtime": 120, "poster_path": "/pWDtjs568ZfOTMbURQBYuT4Qxka.jpg"},
    {"id": 116, "title": "Memories of Murder",                    "year": 2003, "genres": ["Crime","Drama","Mystery","Thriller"],       "rating": 8.1, "votes": 200000,  "runtime": 132, "poster_path": "/dsEoTJKM1s5OVDkS2P2JdoTxo4K.jpg"},
    {"id": 117, "title": "The Handmaiden",                        "year": 2016, "genres": ["Drama","Mystery","Romance","Thriller"],     "rating": 8.1, "votes": 200000,  "runtime": 145, "poster_path": "/dLlH4aNHdnmf62umnInL8xPlPzw.jpg"},
    {"id": 118, "title": "In the Mood for Love",                  "year": 2000, "genres": ["Drama","Romance"],                          "rating": 8.1, "votes": 180000,  "runtime": 98, "poster_path": "/iYypPT4bhqXfq1b6EnmxvRt6b2Y.jpg"},
    {"id": 119, "title": "City of God",                           "year": 2002, "genres": ["Crime","Drama"],                           "rating": 8.6, "votes": 750000,  "runtime": 130, "poster_path": "/k7eYdWvhYQyRQoU2TB2A2Xu2TfD.jpg"},
    {"id": 120, "title": "The Lives of Others",                   "year": 2006, "genres": ["Drama","Thriller"],                         "rating": 8.4, "votes": 330000,  "runtime": 137, "poster_path": "/cVUDMnskSc01rdbyH0tLATTJUdP.jpg"},
    {"id": 121, "title": "Das Boot",                              "year": 1981, "genres": ["Action","Adventure","Drama","History","War"], "rating": 8.4, "votes": 250000, "runtime": 149, "poster_path": "/u8FhQPncOAkwcei2OI9orPWhV6K.jpg"},
    {"id": 122, "title": "Seven Samurai",                         "year": 1954, "genres": ["Action","Adventure","Drama"],               "rating": 8.6, "votes": 350000,  "runtime": 207, "poster_path": "/lOMGc8bnSwQhS4XyE1S99uH8NXf.jpg"},
    {"id": 123, "title": "Rashomon",                              "year": 1950, "genres": ["Crime","Drama","Mystery"],                  "rating": 8.2, "votes": 210000,  "runtime": 88, "poster_path": "/vL7Xw04nFMHwnvXRFCmYYAzMUvY.jpg"},
    {"id": 124, "title": "Yojimbo",                               "year": 1961, "genres": ["Action","Adventure","Drama","Thriller"],    "rating": 8.2, "votes": 130000,  "runtime": 110, "poster_path": "/tN7kYPjRhDolpui9sc9Eq9n5b2O.jpg"},
    {"id": 125, "title": "Tokyo Story",                           "year": 1953, "genres": ["Drama"],                                    "rating": 8.2, "votes": 130000,  "runtime": 136, "poster_path": "/g2YbTYKpY7N2yDSk7BfXZ18I5QV.jpg"},
    {"id": 126, "title": "Stalker",                               "year": 1979, "genres": ["Drama","Mystery","Sci-Fi"],                 "rating": 8.2, "votes": 150000,  "runtime": 162, "poster_path": "/1qhOyf5C4s9ZdvY8d5JDx9DFMeT.jpg"},
    {"id": 127, "title": "The Pianist",                           "year": 2002, "genres": ["Biography","Drama","Music","War"],          "rating": 8.5, "votes": 840000,  "runtime": 150, "poster_path": "/2hFvxCCWrTmCYwfy7yum0GKRi3Y.jpg"},
    {"id": 128, "title": "Braveheart",                            "year": 1995, "genres": ["Action","Biography","Drama","History","War"], "rating": 8.3, "votes": 1000000, "runtime": 177, "poster_path": "/or1gBugydmjToAEq7OZY0owwFk.jpg"},
    {"id": 129, "title": "Gladiator",                             "year": 2000, "genres": ["Action","Adventure","Drama"],               "rating": 8.5, "votes": 1500000, "runtime": 155, "poster_path": "/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"},
    {"id": 130, "title": "The Last Samurai",                      "year": 2003, "genres": ["Action","Drama","History","War"],           "rating": 7.8, "votes": 490000,  "runtime": 154, "poster_path": "/a8jmJPs5eZBARmnuEEvZwbjwyz4.jpg"},
    {"id": 131, "title": "Minority Report",                       "year": 2002, "genres": ["Action","Crime","Mystery","Sci-Fi","Thriller"], "rating": 7.7, "votes": 580000, "runtime": 145, "poster_path": "/ccqpHq5tk5W4ymbSbuoy4uYOxFI.jpg"},
    {"id": 132, "title": "The Sixth Sense",                       "year": 1999, "genres": ["Drama","Mystery","Thriller"],               "rating": 8.2, "votes": 1000000, "runtime": 107, "poster_path": "/vOyfUXNFSnaTk7Vk5AjpsKTUWsu.jpg"},
    {"id": 133, "title": "The Truman Show",                       "year": 1998, "genres": ["Comedy","Drama","Sci-Fi"],                  "rating": 8.2, "votes": 1000000, "runtime": 103, "poster_path": "/vuza0WqY239yBXOadKlGwJsZJFE.jpg"},
    {"id": 134, "title": "American History X",                    "year": 1998, "genres": ["Crime","Drama"],                           "rating": 8.5, "votes": 1100000, "runtime": 119, "poster_path": "/x2drgoXYZ8484lqyDj7L1CEVR4T.jpg"},
    {"id": 135, "title": "The Green Mile",                        "year": 1999, "genres": ["Crime","Drama","Fantasy","Mystery"],        "rating": 8.6, "votes": 1300000, "runtime": 189, "poster_path": "/8VG8fDNiy50H4FedGwdSVUPoaJe.jpg"},
    {"id": 136, "title": "American Beauty",                       "year": 1999, "genres": ["Drama","Romance","Thriller"],               "rating": 8.3, "votes": 1100000, "runtime": 122, "poster_path": "/wby9315QzVKdW9BonAefg8jGTTb.jpg"},
    {"id": 137, "title": "A Beautiful Mind",                      "year": 2001, "genres": ["Biography","Drama","Mystery","Thriller"],   "rating": 8.2, "votes": 940000,  "runtime": 135, "poster_path": "/zwzWCmH72OSC9NA0ipoqw5Zjya8.jpg"},
    {"id": 138, "title": "Catch Me If You Can",                   "year": 2002, "genres": ["Biography","Crime","Drama","Thriller"],     "rating": 8.1, "votes": 1000000, "runtime": 141, "poster_path": "/ctjEj2xM32OvBXCq8zAdK3ZrsAj.jpg"},
    {"id": 139, "title": "Good Will Hunting",                     "year": 1997, "genres": ["Drama","Romance"],                          "rating": 8.3, "votes": 960000,  "runtime": 126, "poster_path": "/z2FnLKpFi1HPO7BEJxdkv6hpJSU.jpg"},
    {"id": 140, "title": "Dead Poets Society",                    "year": 1989, "genres": ["Drama"],                                    "rating": 8.1, "votes": 620000,  "runtime": 128, "poster_path": "/l5NbiHKUmahlAT3Q1ig8Tyl9xrc.jpg"},
    {"id": 141, "title": "Groundhog Day",                         "year": 1993, "genres": ["Comedy","Fantasy","Romance"],               "rating": 8.0, "votes": 680000,  "runtime": 101, "poster_path": "/gCgt1WARPZaXnq523ySQEUKinCs.jpg"},
    {"id": 142, "title": "Home Alone",                            "year": 1990, "genres": ["Comedy","Family"],                          "rating": 7.7, "votes": 580000,  "runtime": 103, "poster_path": "/i5We88HdO9Nsrv8xLyo4toNsLUM.jpg"},
    {"id": 143, "title": "Back to the Future",                    "year": 1985, "genres": ["Adventure","Comedy","Sci-Fi"],              "rating": 8.5, "votes": 1200000, "runtime": 116, "poster_path": "/vN5B5WgYscRGcQpVhHl6p9DDTP0.jpg"},
    {"id": 144, "title": "The Breakfast Club",                    "year": 1985, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.9, "votes": 340000,  "runtime": 97, "poster_path": "/gp4zlj7wgbiofLMNsTPndMuO3PN.jpg"},
    {"id": 145, "title": "Ferris Bueller's Day Off",              "year": 1986, "genres": ["Comedy"],                                   "rating": 7.8, "votes": 380000,  "runtime": 103, "poster_path": "/9LTQNCvoLsKXP0LtaKAaYVtRaQL.jpg"},
    {"id": 146, "title": "Stand by Me",                           "year": 1986, "genres": ["Adventure","Drama"],                        "rating": 8.1, "votes": 460000,  "runtime": 89, "poster_path": "/vz0w9BSehcqjDcJOjRaCk7fgJe7.jpg"},
    {"id": 147, "title": "Midnight in Paris",                     "year": 2011, "genres": ["Comedy","Fantasy","Romance"],               "rating": 7.7, "votes": 430000,  "runtime": 94, "poster_path": "/4wBG5kbfagTQclETblPRRGihk0I.jpg"},
    {"id": 148, "title": "Lost in Translation",                   "year": 2003, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.8, "votes": 500000,  "runtime": 102, "poster_path": "/3jCLmYDIIiSMPujbwygNpqdpM8N.jpg"},
    {"id": 149, "title": "Before Sunrise",                        "year": 1995, "genres": ["Drama","Romance"],                          "rating": 8.1, "votes": 350000,  "runtime": 101, "poster_path": "/kf1Jb1c2JAOqjuzA3H4oDM263uB.jpg"},
    {"id": 150, "title": "Before Sunset",                         "year": 2004, "genres": ["Drama","Romance"],                          "rating": 8.1, "votes": 300000,  "runtime": 80, "poster_path": "/4sW5XH9ZfYXpvFzev00S1IGAEbg.jpg"},
    {"id": 151, "title": "Before Midnight",                       "year": 2013, "genres": ["Drama","Romance"],                          "rating": 7.9, "votes": 190000,  "runtime": 109, "poster_path": "/qbGKJmNUroDz75kh5Oafoall89e.jpg"},
    {"id": 152, "title": "Pride & Prejudice",                     "year": 2005, "genres": ["Drama","Romance"],                          "rating": 7.8, "votes": 430000,  "runtime": 129, "poster_path": "/o8UhmEbWPHmTUxP0lMuCoqNkbB3.jpg"},
    {"id": 153, "title": "Sense and Sensibility",                 "year": 1995, "genres": ["Drama","Romance"],                          "rating": 7.7, "votes": 200000,  "runtime": 136, "poster_path": "/cBK2yL3HqhFvIVd7lLtazWlRZPR.jpg"},
    {"id": 154, "title": "Atonement",                             "year": 2007, "genres": ["Drama","Romance","War"],                    "rating": 7.8, "votes": 300000,  "runtime": 123, "poster_path": "/hMRIyBjPzxaSXWM06se3OcNjIQa.jpg"},
    {"id": 155, "title": "Titanic",                               "year": 1997, "genres": ["Drama","Romance"],                          "rating": 7.9, "votes": 1100000, "runtime": 194, "poster_path": "/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg"},
    {"id": 156, "title": "The Notebook",                          "year": 2004, "genres": ["Drama","Romance"],                          "rating": 7.9, "votes": 580000,  "runtime": 123, "poster_path": "/rNzQyW4f8B8cQeg7Dgj3n6eT5k9.jpg"},
    {"id": 157, "title": "Crouching Tiger, Hidden Dragon",        "year": 2000, "genres": ["Action","Adventure","Drama","Romance"],     "rating": 7.9, "votes": 290000,  "runtime": 120, "poster_path": "/iNDVBFNz4XyYzM9Lwip6atSTFqf.jpg"},
    {"id": 158, "title": "Hero",                                  "year": 2002, "genres": ["Action","Adventure","Drama","History"],     "rating": 7.9, "votes": 240000,  "runtime": 99, "poster_path": "/vxgZto2Cz7ILHAlmRXt50I2brB2.jpg"},
    {"id": 159, "title": "The Witch",                             "year": 2015, "genres": ["Horror","Mystery","Thriller"],              "rating": 6.9, "votes": 190000,  "runtime": 92, "poster_path": "/zap5hpFCWSvdWSuPGAQyjUv2wAC.jpg"},
    {"id": 160, "title": "The Babadook",                          "year": 2014, "genres": ["Drama","Horror","Thriller"],                "rating": 6.8, "votes": 160000,  "runtime": 93, "poster_path": "/qt3fqapeo94TfvMyld8P7gkpXLz.jpg"},
    {"id": 161, "title": "Wind River",                            "year": 2017, "genres": ["Crime","Drama","Mystery","Thriller","Western"], "rating": 7.7, "votes": 250000, "runtime": 107, "poster_path": "/pySivdR845Hom4u4T2WNkJxe6Ad.jpg"},
    {"id": 162, "title": "Hell or High Water",                    "year": 2016, "genres": ["Crime","Drama","Western"],                  "rating": 7.7, "votes": 250000,  "runtime": 102, "poster_path": "/ljRRxqy2aXIkIBXLmOVifcOR021.jpg"},
    {"id": 163, "title": "Mulholland Drive",                      "year": 2001, "genres": ["Drama","Mystery","Romance","Thriller"],     "rating": 7.9, "votes": 300000,  "runtime": 147, "poster_path": "/x7A59t6ySylr1L7aubOQEA480vM.jpg"},
    {"id": 164, "title": "Blue Velvet",                           "year": 1986, "genres": ["Crime","Drama","Mystery","Thriller"],       "rating": 7.7, "votes": 200000,  "runtime": 120, "poster_path": "/tzXuURjPzCqtA6eL0Cswq9wzFx0.jpg"},
    {"id": 165, "title": "The Batman",                            "year": 2022, "genres": ["Action","Crime","Drama","Mystery"],         "rating": 7.8, "votes": 640000,  "runtime": 176, "poster_path": "/74xTEgt7R36Fpooo50r9T25onhq.jpg"},
    {"id": 166, "title": "Tenet",                                 "year": 2020, "genres": ["Action","Sci-Fi","Thriller"],               "rating": 7.4, "votes": 540000,  "runtime": 150, "poster_path": "/aCIFMriQh8rvhxpN1IWGgvH0Tlg.jpg"},
    {"id": 167, "title": "Past Lives",                            "year": 2023, "genres": ["Drama","Romance"],                          "rating": 7.8, "votes": 130000,  "runtime": 106, "poster_path": "/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg"},
    {"id": 168, "title": "All Quiet on the Western Front",        "year": 2022, "genres": ["Drama","War"],                             "rating": 7.8, "votes": 280000,  "runtime": 148, "poster_path": "/2IRjbi9cADuDMKmHdLK7LaqQDKA.jpg"},
    {"id": 169, "title": "Barbie",                                "year": 2023, "genres": ["Adventure","Comedy","Fantasy"],             "rating": 6.9, "votes": 450000,  "runtime": 114, "poster_path": "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"},
    {"id": 170, "title": "The Wolf of Wall Street",               "year": 2013, "genres": ["Biography","Comedy","Crime","Drama"],       "rating": 8.2, "votes": 1400000, "runtime": 180, "poster_path": "/kW9LmvYHAaS9iA0tHmZVq8hQYoq.jpg"},
    {"id": 171, "title": "Gangs of New York",                     "year": 2002, "genres": ["Crime","Drama","History"],                  "rating": 7.5, "votes": 470000,  "runtime": 167, "poster_path": "/lemqKtcCuAano5aqrzxYiKC8kkn.jpg"},
    {"id": 172, "title": "Troy",                                  "year": 2004, "genres": ["Action","Adventure","Drama","History","War"], "rating": 7.3, "votes": 440000, "runtime": 163, "poster_path": "/51auXjXepW1zblzhaN7CAhwvf5i.jpg"},
    {"id": 173, "title": "Gladiator",                             "year": 2000, "genres": ["Action","Adventure","Drama"],               "rating": 8.5, "votes": 1500000, "runtime": 155, "poster_path": "/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"},
    {"id": 174, "title": "Road to Perdition",                     "year": 2002, "genres": ["Crime","Drama","Thriller"],                 "rating": 7.7, "votes": 340000,  "runtime": 117, "poster_path": "/loSpBeirRfTPJ3cMIqpQArstGhh.jpg"},
    {"id": 175, "title": "Munich",                                "year": 2005, "genres": ["Action","Drama","History","Thriller"],      "rating": 7.6, "votes": 300000,  "runtime": 164, "poster_path": "/iUekaw96QLInZpsNwRTlRKrZgwm.jpg"},
    {"id": 176, "title": "Bridge of Spies",                       "year": 2015, "genres": ["Biography","Drama","History","Thriller"],   "rating": 7.6, "votes": 320000,  "runtime": 142, "poster_path": "/fmOOjHAQzxr0c1sfcY4qkiSRBH6.jpg"},
    {"id": 177, "title": "Lincoln",                               "year": 2012, "genres": ["Biography","Drama","History","War"],        "rating": 7.4, "votes": 300000,  "runtime": 150, "poster_path": "/5KeUqW6DpVtf8G9VMuI2l0XIPCo.jpg"},
    {"id": 178, "title": "Saving Private Ryan",                   "year": 1998, "genres": ["Drama","War"],                             "rating": 8.6, "votes": 1400000, "runtime": 169, "poster_path": "/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg"},
    {"id": 179, "title": "Cast Away",                             "year": 2000, "genres": ["Adventure","Drama","Romance"],              "rating": 7.8, "votes": 530000,  "runtime": 143, "poster_path": "/7lLJgKnAicAcR5UEuo8xhSMj18w.jpg"},
    {"id": 180, "title": "The Terminal",                          "year": 2004, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.4, "votes": 370000,  "runtime": 128, "poster_path": "/cPB3ZMM4UdsSAhNdS4c7ps5nypY.jpg"},
    {"id": 181, "title": "Schindler's List",                      "year": 1993, "genres": ["Biography","Drama","History","War"],        "rating": 9.0, "votes": 1400000, "runtime": 195, "poster_path": "/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"},
    {"id": 182, "title": "Downfall",                              "year": 2004, "genres": ["Biography","Drama","History","War"],        "rating": 8.2, "votes": 290000,  "runtime": 156, "poster_path": "/cP1ElGjBhbZAAqmueXjHDKlSwiP.jpg"},
    {"id": 183, "title": "The Imitation Game",                    "year": 2014, "genres": ["Biography","Drama","History","Thriller","War"], "rating": 8.0, "votes": 750000, "runtime": 114, "poster_path": "/zSqJ1qFq8NXFfi7JeIYMlzyR0dx.jpg"},
    {"id": 184, "title": "The Theory of Everything",              "year": 2014, "genres": ["Biography","Drama","Romance"],              "rating": 7.7, "votes": 390000,  "runtime": 123, "poster_path": "/kJuL37NTE51zVP3eG5aGMyKAIlh.jpg"},
    {"id": 185, "title": "Philadelphia",                          "year": 1993, "genres": ["Drama"],                                   "rating": 7.7, "votes": 200000,  "runtime": 125, "poster_path": "/tFe5Yoo5zT495okA49bq1vPPkiV.jpg"},
    {"id": 186, "title": "Rain Man",                              "year": 1988, "genres": ["Drama"],                                   "rating": 8.0, "votes": 480000,  "runtime": 133, "poster_path": "/iTNHwO896WKkaoPtpMMS74d8VNi.jpg"},
    {"id": 187, "title": "Big Fish",                              "year": 2003, "genres": ["Adventure","Drama","Fantasy","Romance"],    "rating": 8.0, "votes": 560000,  "runtime": 125, "poster_path": "/tjK063yCgaBAluVU72rZ6PKPH2l.jpg"},
    {"id": 188, "title": "Edward Scissorhands",                   "year": 1990, "genres": ["Drama","Fantasy","Romance"],               "rating": 7.9, "votes": 490000,  "runtime": 105, "poster_path": "/e0FqKFvGPdQNWG8tF9cZBtev9Em.jpg"},
    {"id": 189, "title": "Beetlejuice",                           "year": 1988, "genres": ["Comedy","Fantasy","Horror"],               "rating": 7.5, "votes": 390000,  "runtime": 92, "poster_path": "/nnl6OWkyPpuMm595hmAxNW3rZFn.jpg"},
    {"id": 190, "title": "The Nightmare Before Christmas",        "year": 1993, "genres": ["Animation","Family","Fantasy","Musical"],   "rating": 7.9, "votes": 440000,  "runtime": 76, "poster_path": "/oQffRNjK8e19rF7xVYEN8ew0j7b.jpg"},
    {"id": 191, "title": "Coraline",                              "year": 2009, "genres": ["Animation","Drama","Family","Fantasy","Horror"], "rating": 7.7, "votes": 360000, "runtime": 100, "poster_path": "/4jeFXQYytChdZYE9JYO7Un87IlW.jpg"},
    {"id": 192, "title": "Kubo and the Two Strings",              "year": 2016, "genres": ["Animation","Action","Adventure","Drama","Family","Fantasy"], "rating": 7.7, "votes": 120000, "runtime": 101, "poster_path": "/ewcOCkuuKAKULGUnbBVaO1htt0D.jpg"},
    {"id": 193, "title": "Isle of Dogs",                          "year": 2018, "genres": ["Animation","Adventure","Comedy","Drama","Fantasy"], "rating": 7.9, "votes": 170000, "runtime": 101, "poster_path": "/c0nUX6Q1ZB0P2t1Jo6EeFSVnOGQ.jpg"},
    {"id": 194, "title": "Fantastic Mr. Fox",                     "year": 2009, "genres": ["Animation","Adventure","Comedy","Family"],  "rating": 7.9, "votes": 280000,  "runtime": 87, "poster_path": "/euZyZb6iGreujYKrGyZHRddhUYh.jpg"},
    {"id": 195, "title": "The Royal Tenenbaums",                  "year": 2001, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.6, "votes": 290000,  "runtime": 110, "poster_path": "/nG7hZJn7wQTSDCQT39Gy3s3tbrp.jpg"},
    {"id": 196, "title": "Rushmore",                              "year": 1998, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.5, "votes": 170000,  "runtime": 93, "poster_path": "/hSJ6swahAuZ8wM96lHDTwQPXUvZ.jpg"},
    {"id": 197, "title": "The French Dispatch",                   "year": 2021, "genres": ["Comedy","Drama","Romance"],                 "rating": 7.2, "votes": 180000,  "runtime": 108, "poster_path": "/6JXR3KJH5roiBCjWFt09xfgxHZc.jpg"},
    {"id": 198, "title": "Asteroid City",                         "year": 2023, "genres": ["Comedy","Drama","Romance","Sci-Fi"],        "rating": 6.6, "votes": 90000,   "runtime": 105, "poster_path": "/hfo7pvL9Fys7rocfL4VOzw9qDEQ.jpg"},
    {"id": 199, "title": "The Prestige",                          "year": 2006, "genres": ["Drama","Mystery","Sci-Fi","Thriller"],      "rating": 8.5, "votes": 1400000, "runtime": 130, "poster_path": "/Ag2B2KHKQPukjH7WutmgnnSNurZ.jpg"},
    {"id": 200, "title": "Memento",                               "year": 2000, "genres": ["Mystery","Thriller"],                       "rating": 8.4, "votes": 1200000, "runtime": 113, "poster_path": "/fKTPH2WvH8nHTXeBYBVhawtRqtR.jpg"},
    {"id": 201, "title": "Batman Begins",                         "year": 2005, "genres": ["Action","Adventure","Drama"],               "rating": 8.2, "votes": 1300000, "runtime": 140, "poster_path": "/sPX89Td70IDDjVr85jdSBb4rWGr.jpg"},
    {"id": 202, "title": "The Dark Knight Rises",                 "year": 2012, "genres": ["Action","Adventure","Drama","Thriller"],    "rating": 8.4, "votes": 1600000, "runtime": 164, "poster_path": "/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg"},
    {"id": 203, "title": "Interstellar",                          "year": 2014, "genres": ["Adventure","Drama","Sci-Fi"],               "rating": 8.7, "votes": 1900000, "runtime": 169, "poster_path": "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"},
    {"id": 204, "title": "Contact",                               "year": 1997, "genres": ["Drama","Mystery","Sci-Fi"],                 "rating": 7.5, "votes": 340000,  "runtime": 150, "poster_path": "/bCpMIywuNZeWt3i5UMLEIc0VSwM.jpg"},
    {"id": 205, "title": "Close Encounters of the Third Kind",    "year": 1977, "genres": ["Drama","Sci-Fi"],                           "rating": 7.6, "votes": 230000,  "runtime": 138, "poster_path": "/gCWPB8cF82tqzrS9tvzcO6q6nyz.jpg"},
    {"id": 206, "title": "The English Patient",                   "year": 1996, "genres": ["Drama","Romance","War"],                    "rating": 7.4, "votes": 160000,  "runtime": 162, "poster_path": "/8eHHqMg8qEYtVw8LQLygsHXSR2q.jpg"},
    {"id": 207, "title": "Unbreakable",                           "year": 2000, "genres": ["Drama","Mystery","Sci-Fi","Thriller"],      "rating": 7.3, "votes": 340000,  "runtime": 106, "poster_path": "/mLuehrGLiK5zFCyRmDDOH6gbfPf.jpg"},
    {"id": 208, "title": "Signs",                                 "year": 2002, "genres": ["Drama","Mystery","Sci-Fi","Thriller"],      "rating": 7.2, "votes": 380000,  "runtime": 106, "poster_path": "/YtrIdrTxpRhvCnlw43dwOjfLqx.jpg"},
    {"id": 209, "title": "Children of Men",                       "year": 2006, "genres": ["Action","Drama","Sci-Fi","Thriller"],       "rating": 7.9, "votes": 490000,  "runtime": 109, "poster_path": "/lQcXgb0fFzffnLV5WY0Q0X2WW7E.jpg"},
    {"id": 210, "title": "District 9",                            "year": 2009, "genres": ["Action","Drama","Sci-Fi","Thriller"],       "rating": 7.9, "votes": 700000,  "runtime": 112, "poster_path": "/tuGlQkqLxnodDSk6mp5c2wvxUEd.jpg"},
    {"id": 211, "title": "Elysium",                               "year": 2013, "genres": ["Action","Drama","Sci-Fi","Thriller"],       "rating": 6.6, "votes": 370000,  "runtime": 109, "poster_path": "/uiiXHBd9oUrtUa4YqZiAoy05cRz.jpg"},
    {"id": 212, "title": "Edge of Tomorrow",                      "year": 2014, "genres": ["Action","Adventure","Sci-Fi"],              "rating": 7.9, "votes": 670000,  "runtime": 113, "poster_path": "/nBM9MMa2WCwvMG4IJ3eiGUdbPe6.jpg"},
    {"id": 213, "title": "The Revenant",                          "year": 2015, "genres": ["Adventure","Drama","Western"],              "rating": 8.0, "votes": 800000,  "runtime": 156, "poster_path": "/ji3ecJphATlVgWNY0B0RVXZizdf.jpg"},
    {"id": 214, "title": "Birdman",                               "year": 2014, "genres": ["Comedy","Drama"],                           "rating": 7.7, "votes": 530000,  "runtime": 119, "poster_path": "/rFERAyRuI6nuWKaLTpcjowOoQPC.jpg"},
    {"id": 215, "title": "12 Years a Slave",                      "year": 2013, "genres": ["Biography","Drama","History"],              "rating": 8.1, "votes": 640000,  "runtime": 134, "poster_path": "/xdANQijuNrJaw1HA61rDccME4Tm.jpg"},
    {"id": 216, "title": "Moonlight",                             "year": 2016, "genres": ["Drama","Romance"],                          "rating": 7.4, "votes": 310000,  "runtime": 111, "poster_path": "/qLnfEmPrDjJfPyyddLJPkXmshkp.jpg"},
    {"id": 217, "title": "La La Land",                            "year": 2016, "genres": ["Comedy","Drama","Music","Musical","Romance"], "rating": 8.0, "votes": 700000, "runtime": 128, "poster_path": "/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg"},
    {"id": 218, "title": "Once",                                  "year": 2007, "genres": ["Drama","Music","Romance"],                  "rating": 7.8, "votes": 190000,  "runtime": 86, "poster_path": "/7nW363kSYRCkr4VGOMvuSGwtzKs.jpg"},
    {"id": 219, "title": "Bohemian Rhapsody",                     "year": 2018, "genres": ["Biography","Drama","Music"],                "rating": 7.9, "votes": 600000,  "runtime": 134, "poster_path": "/lHu1wtNaczFPGFDTrjCSzeLPTKN.jpg"},
    {"id": 220, "title": "Elvis",                                 "year": 2022, "genres": ["Biography","Drama","Music"],                "rating": 7.4, "votes": 200000,  "runtime": 159, "poster_path": "/rva3UhKaMeiB0Vej5A2pm1leX7K.jpg"},
]

# =====================================================================
# SECTION 2 — DERIVED FEATURES
# =====================================================================

def quality_band(rating: float) -> str:
    if rating >= 8.5: return "excellent"
    if rating >= 7.5: return "good"
    if rating >= 6.0: return "average"
    return "low"

def runtime_category(runtime: int) -> str:
    if runtime < 90:  return "short"
    if runtime <= 120: return "medium"
    return "long"

def popularity_band(votes: int) -> str:
    """Assign popularity based on vote count quartiles across the dataset."""
    all_votes = sorted(m["votes"] for m in MOVIES)
    n = len(all_votes)
    q1 = all_votes[n // 4]
    q3 = all_votes[(3 * n) // 4]
    if votes >= q3: return "popular"
    if votes <= q1: return "obscure"
    return "average"

# Pre-compute derived fields
for m in MOVIES:
    m["quality"]    = str(quality_band(float(m["rating"])))
    m["runtime_cat"] = str(runtime_category(int(m["runtime"])))
    m["pop_band"]   = str(popularity_band(int(m["votes"])))

ALL_GENRES: List[str] = sorted({str(g) for m in MOVIES for g in m["genres"]})

# =====================================================================
# SECTION 3 — RULE DEFINITIONS
# =====================================================================

class Rule:
    id: str
    description: str
    score: float
    condition: Any
    explanation: Any

    def __init__(self, rid: str, description: str, score: float,
                 condition: Any, explanation: Any):
        self.id          = str(rid)
        self.description = str(description)
        self.score       = float(score)
        self.condition   = condition   # callable(movie, prefs) -> bool
        self.explanation = explanation # callable(movie, prefs) -> str


def build_rules(prefs: Dict[str, Any]) -> List[Rule]:
    rules: List[Rule] = []

    # ── Genre: individual preferred genre matches ──────────────────
    for g in ALL_GENRES:
        rules.append(Rule(
            rid=f"GENRE_{g}",
            description=f"Contains genre '{g}'",
            score=1.5,
            condition=lambda m, p, _g=g: _g in m["genres"],
            explanation=lambda m, p, _g=g: f"Includes genre '{_g}'",
        ))

    # ── Genre: multiple preferred genres matched ───────────────────
    if len(prefs["inc_genres"]) >= 2:
        rules.append(Rule(
            rid="GENRE_MULTI_MATCH",
            description="Matches 2+ preferred genres",
            score=2.5,
            condition=lambda m, p: sum(g in m["genres"] for g in p["inc_genres"]) >= 2,
            explanation=lambda m, p: (
                "Matches multiple preferred genres: " +
                ", ".join(g for g in p["inc_genres"] if g in m["genres"])
            ),
        ))

    # ── Quality tiers ──────────────────────────────────────────────
    rules.append(Rule(
        rid="QUALITY_EXCELLENT", description="Excellent quality (≥8.5)",
        score=3.5,
        condition=lambda m, p: m["quality"] == "excellent",
        explanation=lambda m, p: f"Excellent rating: {m['rating']}/10",
    ))
    rules.append(Rule(
        rid="QUALITY_GOOD", description="Good quality (7.5–8.4)",
        score=2.0,
        condition=lambda m, p: m["quality"] == "good",
        explanation=lambda m, p: f"Good rating: {m['rating']}/10",
    ))
    rules.append(Rule(
        rid="QUALITY_AVERAGE", description="Average quality (6.0–7.4)",
        score=0.5,
        condition=lambda m, p: m["quality"] == "average",
        explanation=lambda m, p: f"Average rating: {m['rating']}/10",
    ))

    # ── Popularity tier ────────────────────────────────────────────
    rules.append(Rule(
        rid="POP_POPULAR", description="Widely popular title",
        score=1.2,
        condition=lambda m, p: m["pop_band"] == "popular",
        explanation=lambda m, p: f"Popular title ({m['votes']:,} votes)",
    ))
    rules.append(Rule(
        rid="POP_OBSCURE", description="Hidden gem / niche pick",
        score=0.8,
        condition=lambda m, p: m["pop_band"] == "obscure",
        explanation=lambda m, p: f"Hidden gem ({m['votes']:,} votes)",
    ))
    if prefs["pop_pref"] in ("popular", "obscure"):
        rules.append(Rule(
            rid="POP_PREF_MATCH", description="Popularity preference match",
            score=2.0,
            condition=lambda m, p: m["pop_band"] == p["pop_pref"],
            explanation=lambda m, p: f"Matches '{p['pop_pref']}' popularity preference",
        ))

    # ── Era / Year ─────────────────────────────────────────────────
    rules.append(Rule(
        rid="ERA_IN_RANGE", description="Within preferred year range",
        score=1.5,
        condition=lambda m, p: p["year_from"] <= m["year"] <= p["year_to"],
        explanation=lambda m, p: f"Released in {m['year']} (within {p['year_from']}–{p['year_to']})",
    ))
    if prefs["year_to"] <= 1985:
        rules.append(Rule(
            rid="CLASSIC_CINEMA", description="Classic cinema era bonus",
            score=1.0,
            condition=lambda m, p: m["year"] <= 1985,
            explanation=lambda m, p: f"Classic cinema era ({m['year']})",
        ))
    if prefs["year_from"] >= 2010:
        rules.append(Rule(
            rid="MODERN_CINEMA", description="Modern cinema era bonus",
            score=1.0,
            condition=lambda m, p: m["year"] >= 2010,
            explanation=lambda m, p: f"Contemporary film ({m['year']})",
        ))

    # ── Runtime ────────────────────────────────────────────────────
    if prefs["runtime_pref"] != "any":
        rules.append(Rule(
            rid="RUNTIME_PREF_MATCH", description="Runtime preference match",
            score=1.8,
            condition=lambda m, p: m["runtime_cat"] == p["runtime_pref"],
            explanation=lambda m, p: f"Runtime matches '{p['runtime_pref']}' ({m['runtime']} min)",
        ))
    rules.append(Rule(
        rid="RUNTIME_SHORT", description="Short film bonus",
        score=0.6,
        condition=lambda m, p: m["runtime_cat"] == "short",
        explanation=lambda m, p: f"Short runtime ({m['runtime']} min)",
    ))
    rules.append(Rule(
        rid="RUNTIME_MEDIUM", description="Medium runtime bonus",
        score=0.8,
        condition=lambda m, p: m["runtime_cat"] == "medium",
        explanation=lambda m, p: f"Medium runtime ({m['runtime']} min)",
    ))
    rules.append(Rule(
        rid="RUNTIME_LONG", description="Long runtime bonus",
        score=0.5,
        condition=lambda m, p: m["runtime_cat"] == "long",
        explanation=lambda m, p: f"Epic runtime ({m['runtime']} min)",
    ))

    # ── Genre combos (quality-gated) ───────────────────────────────
    COMBOS: List[Tuple[str, str]] = [
        ("Action",    "Sci-Fi"),
        ("Drama",     "Romance"),
        ("Animation", "Family"),
        ("Comedy",    "Romance"),
        ("Adventure", "Fantasy"),
        ("Crime",     "Thriller"),
        ("Drama",     "History"),
        ("Action",    "Adventure"),
        ("Mystery",   "Thriller"),
        ("Biography", "Drama"),
    ]
    for a, b in COMBOS:
        rules.append(Rule(
            rid=f"COMBO_{a}_{b}",
            description=f"Quality {a}+{b} combo",
            score=2.5,
            condition=lambda m, p, _a=a, _b=b: (
                _a in m["genres"] and _b in m["genres"]
                and m["quality"] in ("excellent", "good")
            ),
            explanation=lambda m, p, _a=a, _b=b: (
                f"Strong genre combo: {_a} + {_b} with {m['quality']} quality"
            ),
        ))

    # ── Highly voted (engagement signal) ──────────────────────────
    rules.append(Rule(
        rid="HIGHLY_VOTED",
        description="Over 1M votes",
        score=1.0,
        condition=lambda m, p: m["votes"] >= 1_000_000,
        explanation=lambda m, p: f"Highly engaged audience ({m['votes']:,} votes)",
    ))

    # ── Decade-specific genre affinity (example heuristics) ───────
    rules.append(Rule(
        rid="NOIR_CLASSIC",
        description="Film-Noir classic era bonus",
        score=1.5,
        condition=lambda m, p: "Film-Noir" in m["genres"] and m["year"] <= 1965,
        explanation=lambda m, p: "Classic Film-Noir era",
    ))
    rules.append(Rule(
        rid="ANIME_BONUS",
        description="Japanese animation quality bonus",
        score=1.0,
        condition=lambda m, p: (
            "Animation" in m["genres"]
            and m["quality"] in ("excellent", "good")
            and m["year"] >= 1984
        ),
        explanation=lambda m, p: "High-quality animation title",
    ))

    return rules

# =====================================================================
# SECTION 4 — HARD CONSTRAINTS FILTER
# =====================================================================

def apply_hard_constraints(prefs: Dict[str, Any]) -> List[Dict]:
    results = []
    for m in MOVIES:
        if m["year"] < prefs["year_from"] or m["year"] > prefs["year_to"]:
            continue
        if m["rating"] < prefs["min_rating"]:
            continue
        if prefs["inc_genres"] and not any(g in m["genres"] for g in prefs["inc_genres"]):
            continue
        if any(g in m["genres"] for g in prefs["exc_genres"]):
            continue
        if prefs["runtime_pref"] != "any" and m["runtime_cat"] != prefs["runtime_pref"]:
            continue
        results.append(m)
    return results

# =====================================================================
# SECTION 5 — FORWARD-CHAINING INFERENCE ENGINE
# =====================================================================

def infer(candidates: List[Dict[str, Any]], prefs: Dict[str, Any],
          rules: List[Rule]) -> List[Dict[str, Any]]:
    scored: List[Dict[str, Any]] = []
    for movie in candidates:
        all_scores: List[float] = []
        fired_list: List[Dict[str, Any]] = []
        for rule in rules:
            try:
                if rule.condition(movie, prefs):
                    s_val: float = float(rule.score)
                    all_scores.append(s_val)
                    fired_list.append({
                        "rule_id":     str(rule.id),
                        "description": str(rule.description),
                        "delta":       s_val,
                        "explanation": str(rule.explanation(movie, prefs)),
                    })
            except Exception:
                continue
        
        total_score: float = sum(all_scores)
        scored.append({
            "movie":  movie,
            "score":  total_score,
            "fired":  fired_list,
        })
    scored.sort(
        key=lambda x: (float(x["score"]), float(x["movie"]["rating"]), int(x["movie"]["votes"])),
        reverse=True,
    )
    return scored

# =====================================================================
# SECTION 6 — USER PREFERENCE INPUT
# =====================================================================

def prompt_choice(prompt: str, options: List[str], default: str) -> str:
    print(f"  {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"    [{i}] {opt}")
    raw = input(f"  Enter number (default: {default}): ").strip()
    if not raw:
        return default
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass
    return default


def prompt_genres(label: str) -> List[str]:
    print(f"\n  {label}")
    print("  " + "  ".join(f"[{i+1:>2}] {g}" for i, g in enumerate(ALL_GENRES)))
    raw = input("  Enter numbers separated by spaces (or Enter to skip): ").strip()
    if not raw:
        return []
    selected = []
    for token in raw.split():
        try:
            idx = int(token) - 1
            if 0 <= idx < len(ALL_GENRES):
                selected.append(ALL_GENRES[idx])
        except ValueError:
            pass
    return selected


def prompt_int(prompt: str, default: int, lo: int, hi: int) -> int:
    raw = input(f"  {prompt} [{lo}–{hi}] (default {default}): ").strip()
    if not raw:
        return default
    try:
        val = int(raw)
        return max(lo, min(hi, val))
    except ValueError:
        return default


def prompt_float(prompt: str, default: float, lo: float, hi: float) -> float:
    raw = input(f"  {prompt} [{lo}–{hi}] (default {default}): ").strip()
    if not raw:
        return default
    try:
        val = float(raw)
        return max(lo, min(hi, val))
    except ValueError:
        return default


def gather_preferences() -> Dict[str, Any]:
    year_min = min(m["year"] for m in MOVIES)
    year_max = max(m["year"] for m in MOVIES)

    print("\n" + "═" * 60)
    print("  GENRE SELECTION")
    print("═" * 60)
    inc_genres = prompt_genres("Include genres (only show films with these):")
    exc_genres = prompt_genres("Exclude genres (never show films with these):")
    # Remove overlap
    exc_genres = [g for g in exc_genres if g not in inc_genres]

    print("\n" + "═" * 60)
    print("  ERA & QUALITY")
    print("═" * 60)
    year_from  = prompt_int("Release year — from", 1970, year_min, year_max)
    year_to    = prompt_int("Release year — to",   year_max, year_min, year_max)
    if year_from > year_to:
        year_from, year_to = year_to, year_from
    min_rating = prompt_float("Minimum rating (0–10)", 0.0, 0.0, 10.0)

    print("\n" + "═" * 60)
    print("  POPULARITY & RUNTIME")
    print("═" * 60)
    pop_pref     = prompt_choice("Popularity preference:",
                                 ["any", "popular", "obscure"], "any")
    runtime_pref = prompt_choice("Runtime preference:",
                                 ["any", "short", "medium", "long"], "any")

    print("\n" + "═" * 60)
    print("  OUTPUT")
    print("═" * 60)
    top_k = prompt_int("Number of recommendations (top K)", 10, 1, 50)

    return {
        "inc_genres":   inc_genres,
        "exc_genres":   exc_genres,
        "year_from":    year_from,
        "year_to":      year_to,
        "min_rating":   min_rating,
        "pop_pref":     pop_pref,
        "runtime_pref": runtime_pref,
        "top_k":        top_k,
    }

# =====================================================================
# SECTION 7 — OUTPUT RENDERING
# =====================================================================

def bar(value: float, max_value: float, width: int = 20) -> str:
    filled = int(round((value / max_value) * width)) if max_value > 0 else 0
    return "█" * filled + "░" * (width - filled)


def print_recommendations(top_results: List[Dict[str, Any]],
                           candidate_count: int,
                           rule_count: int,
                           prefs: Dict[str, Any]) -> None:
    W = 70
    print("\n" + "═" * W)
    print("  ★  TOP RECOMMENDATIONS  ★")
    print("═" * W)

    if not top_results:
        print("\n  No films matched your criteria.")
        print("  Try: wider year range · lower min rating · fewer genre filters")
        print("═" * W)
        return

    # Defensive way to get max score without indexing
    max_score: float = 1.0
    for res_item in top_results:
        max_score = float(res_item["score"])
        break

    for rank, rec in enumerate(top_results, 1):
        m     = rec["movie"]
        score = rec["score"]
        fired = rec["fired"]

        genres_str  = ", ".join(m["genres"])
        quality_lbl = {"excellent": "★★★★", "good": "★★★ ", "average": "★★  ", "low": "★   "}.get(m["quality"], "?")
        pop_lbl     = {"popular": "◆ POPULAR", "obscure": "◇ OBSCURE", "average": "● MID-TIER"}.get(m["pop_band"], "")
        rt_lbl      = f"{m['runtime']} min ({m['runtime_cat']})"

        print(f"\n  {'─'*66}")
        print(f"  #{rank:<3}  {m['title']}  ({m['year']})")
        print(f"       Rating : {m['rating']:.1f}/10  {quality_lbl}  |  {pop_lbl}")
        print(f"       Runtime: {rt_lbl}  |  Votes: {m['votes']:,}")
        print(f"       Genres : {genres_str}")
        print(f"       Score  : {score:.2f}  {bar(score, max_score)}")
        print(f"       Rules  : {len(fired)} fired")

        fired_reasons: List[Dict[str, Any]] = rec.get("fired", [])
        top_reasons: List[Dict[str, Any]] = []
        for i, r_item in enumerate(sorted(fired_reasons, key=lambda x: x["delta"], reverse=True)):
            if i >= 5: break
            top_reasons.append(r_item)
        for r in top_reasons:
            print(f"         + {r['explanation']}  (+{r['delta']:.1f})")

    print("\n" + "═" * W)
    print("  SYSTEM SUMMARY")
    print(f"  Total films   : {len(MOVIES)}")
    print(f"  Rules active  : {rule_count}")
    print(f"  Candidates    : {candidate_count}  (after hard constraints)")
    print(f"  Shown         : {len(top_results)}")
    print("═" * W)

# =====================================================================
# SECTION 8 — AUTOMATED TESTS
# =====================================================================

def run_tests() -> None:
    print("\n" + "─" * 50)
    print("  Running self-tests...")

    profiles = [
        {
            "name": "Action/Sci-Fi fan",
            "prefs": {
                "inc_genres": ["Action", "Sci-Fi"],
                "exc_genres": [],
                "year_from": 1980, "year_to": 2023,
                "min_rating": 7.0,
                "pop_pref": "any",
                "runtime_pref": "any",
                "top_k": 5,
            },
        },
        {
            "name": "Classic Drama lover",
            "prefs": {
                "inc_genres": ["Drama"],
                "exc_genres": ["Horror"],
                "year_from": 1940, "year_to": 1980,
                "min_rating": 7.5,
                "pop_pref": "any",
                "runtime_pref": "any",
                "top_k": 5,
            },
        },
        {
            "name": "Family Animation night",
            "prefs": {
                "inc_genres": ["Animation", "Family"],
                "exc_genres": [],
                "year_from": 1985, "year_to": 2023,
                "min_rating": 7.5,
                "pop_pref": "popular",
                "runtime_pref": "any",
                "top_k": 5,
            },
        },
        {
            "name": "Short hidden gems",
            "prefs": {
                "inc_genres": [],
                "exc_genres": [],
                "year_from": 1980, "year_to": 2023,
                "min_rating": 7.0,
                "pop_pref": "obscure",
                "runtime_pref": "short",
                "top_k": 5,
            },
        },
    ]

    all_passed = True
    for prof in profiles:
        # Explicit cast to satisfy strict linter
        p_obj = cast(Dict[str, Any], prof)
        name: str = str(p_obj["name"])
        prefs: Dict[str, Any] = cast(Dict[str, Any], p_obj["prefs"])
        
        rules = build_rules(prefs)
        cands = apply_hard_constraints(prefs)
        results: List[Dict[str, Any]] = infer(cands, prefs, rules)

        errors: List[str] = []
        # Check first 10 recommendations
        recs_to_check: List[Dict[str, Any]] = []
        for idx, rec_item in enumerate(results):
            if idx >= 10: break
            recs_to_check.append(rec_item)
        
        for rec in recs_to_check:
            m: Dict[str, Any] = rec["movie"]
            if not (float(prefs["year_from"]) <= float(m["year"]) <= float(prefs["year_to"])):
                errors.append(f"Year {m['year']} outside [{prefs['year_from']}, {prefs['year_to']}]")
            if float(m["rating"]) < float(prefs["min_rating"]):
                errors.append(f"Rating {m['rating']} < {prefs['min_rating']}")
            if prefs["inc_genres"] and not any(g in m["genres"] for g in prefs["inc_genres"]):
                errors.append(f"Missing included genres in {m['genres']}")
            if any(g in m["genres"] for g in prefs["exc_genres"]):
                errors.append(f"Has excluded genre in {m['genres']}")
            if str(prefs["runtime_pref"]) != "any" and str(m["runtime_cat"]) != str(prefs["runtime_pref"]):
                errors.append(f"Runtime '{m['runtime_cat']}' != '{prefs['runtime_pref']}'")

        top_5: List[Dict[str, Any]] = []
        for idx, rec_item in enumerate(results):
            if idx >= 5: break
            top_5.append(rec_item)
            
        if not any(len(r["fired"]) > 0 for r in top_5):
            errors.append("No rules fired in top-5")

        if errors:
            all_passed = False
            print(f"  [FAIL] {name}: {errors[0]}")
        else:
            print(f"  [PASS] {name}: {len(results)} recommendations, rules fired ✓")

    print(f"  {'All tests passed ✓' if all_passed else 'Some tests FAILED ✗'}")
    print("─" * 50)

# =====================================================================
# SECTION 9 — MAIN
# =====================================================================

def main() -> None:
    print("═" * 60)
    print("  CineLogic — Rule-Based Movie Recommendation System")
    print("  Pure Python · No ML · No External Files")
    print(f"  {len(MOVIES)} films · {len(ALL_GENRES)} genres · Forward-chaining engine")
    print("═" * 60)

    # Run self-tests first
    run_tests()

    # Gather user preferences
    print("\n  Configure your preferences below.")
    print("  (Press Enter at any prompt to use the default value)\n")
    prefs = gather_preferences()

    # Build rules, filter, infer
    rules      = build_rules(prefs)
    candidates = apply_hard_constraints(prefs)
    results    = infer(candidates, prefs, rules)
    
    top_k: int = int(prefs.get("top_k", 5))
    top: List[Dict[str, Any]] = []
    for i, res in enumerate(results):
        if i >= top_k: break
        top.append(res)

    # Display results
    print_recommendations(top, len(candidates), len(rules), prefs)


if __name__ == "__main__":
    main()
