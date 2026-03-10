export const deduplicateMovies = (movies: any[]) => {
  const seen = new Set();
  return movies.filter(item => {
    // Some items might be recommendations with { movie, score, fired }
    const movie = item.movie || item;
    const key = `${movie.title.toLowerCase().trim()}-${movie.year}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};

export const formatRuntime = (minutes: number) => {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h}h ${m}m`;
};
