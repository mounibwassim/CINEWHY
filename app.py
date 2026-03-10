from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import movie_recommender as mr

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    year_min = min(m["year"] for m in mr.MOVIES)
    year_max = max(m["year"] for m in mr.MOVIES)
    return render_template(
        "index.html",
        genres=mr.ALL_GENRES,
        year_min=year_min,
        year_max=year_max,
    )


@app.route("/api/init", methods=["GET"])
def api_init():
    year_min = min(m["year"] for m in mr.MOVIES)
    year_max = max(m["year"] for m in mr.MOVIES)
    return jsonify({
        "movies": mr.MOVIES,
        "genres": mr.ALL_GENRES,
        "year_min": year_min,
        "year_max": year_max,
        "pop_options": ["any", "popular", "obscure"],
        "runtime_options": ["any", "short", "medium", "long"]
    })


def build_prefs_from_form(form):
    if hasattr(form, "getlist"):
        inc_genres = form.getlist("inc_genres")
        exc_genres = form.getlist("exc_genres")
    else:
        inc_genres = form.get("inc_genres", [])
        exc_genres = form.get("exc_genres", [])

    try:
        year_from = int(form.get("year_from") or min(m["year"] for m in mr.MOVIES))
    except (ValueError, TypeError):
        year_from = min(m["year"] for m in mr.MOVIES)
    try:
        year_to = int(form.get("year_to") or max(m["year"] for m in mr.MOVIES))
    except (ValueError, TypeError):
        year_to = max(m["year"] for m in mr.MOVIES)
    try:
        min_rating = float(form.get("min_rating") or 0.0)
    except (ValueError, TypeError):
        min_rating = 0.0

    pop_pref = form.get("pop_pref") or "any"
    runtime_pref = form.get("runtime_pref") or "any"
    try:
        top_k = int(form.get("top_k") or 10)
    except (ValueError, TypeError):
        top_k = 10

    # Ensure excluded genres don't overlap
    exc_genres = [g for g in exc_genres if g not in inc_genres]

    return {
        "inc_genres": inc_genres,
        "exc_genres": exc_genres,
        "year_from": year_from,
        "year_to": year_to,
        "min_rating": min_rating,
        "pop_pref": pop_pref,
        "runtime_pref": runtime_pref,
        "top_k": top_k,
    }


@app.route("/recommend", methods=["POST"])
def recommend():
    prefs = build_prefs_from_form(request.form)
    rules = mr.build_rules(prefs)
    candidates = mr.apply_hard_constraints(prefs)
    results = mr.infer(candidates, prefs, rules)
    top = results[: int(prefs.get("top_k", 10))]
    return render_template(
        "results.html",
        top=top,
        candidate_count=len(candidates),
        rule_count=len(rules),
        prefs=prefs,
    )


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.json or {}
    # Accept the same keys as the form; fallback to defaults
    form = request.form if request.form else data
    prefs = build_prefs_from_form(form)
    rules = mr.build_rules(prefs)
    candidates = mr.apply_hard_constraints(prefs)
    results = mr.infer(candidates, prefs, rules)
    top = results[: int(prefs.get("top_k", 10))]
    out = []
    for r in top:
        out.append({
            "movie": r["movie"],
            "score": r["score"],
            "fired": r["fired"],
        })
    return jsonify({"results": out, "candidate_count": len(candidates), "rule_count": len(rules)})


if __name__ == "__main__":
    # CineWhy Backend Initialization
    app.run(host="0.0.0.0", port=5000, debug=True)
