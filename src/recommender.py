import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


class ScoringStrategy:
    """Strategy interface for selecting score weights."""

    def apply(self, user_prefs: Dict) -> Dict:
        return dict(user_prefs)


class GenreFirstStrategy(ScoringStrategy):
    def apply(self, user_prefs: Dict) -> Dict:
        prefs = dict(user_prefs)
        prefs.update(genre_weight=2.0, mood_weight=1.0, energy_weight=1.0)
        return prefs


class MoodFirstStrategy(ScoringStrategy):
    def apply(self, user_prefs: Dict) -> Dict:
        prefs = dict(user_prefs)
        prefs.update(genre_weight=1.0, mood_weight=2.0, energy_weight=1.0)
        return prefs


class EnergyFocusedStrategy(ScoringStrategy):
    def apply(self, user_prefs: Dict) -> Dict:
        prefs = dict(user_prefs)
        prefs.update(genre_weight=1.0, mood_weight=1.0, energy_weight=2.0)
        return prefs


SCORING_STRATEGIES = {
    "genre-first": GenreFirstStrategy(),
    "mood-first": MoodFirstStrategy(),
    "energy-focused": EnergyFocusedStrategy(),
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the highest-scoring songs for an OOP user profile."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre.lower() == user.favorite_genre.lower():
                score += 2.0
            if song.mood.lower() == user.favorite_mood.lower():
                score += 1.0
            score += max(0.0, 1.0 - abs(song.energy - user.target_energy))
            if user.likes_acoustic and song.acousticness >= 0.5:
                score += 0.25
            scored.append((score, song))
        return [song for _, song in sorted(scored, key=lambda item: item[0], reverse=True)[:max(0, k)]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain the score for one song using the same OOP recipe."""
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre match (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood match (+1.0)")
        reasons.append(
            f"energy similarity (+{max(0.0, 1.0 - abs(song.energy - user.target_energy)):.2f})"
        )
        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("acoustic preference (+0.25)")
        return "; ".join(reasons) if reasons else "closest overall content match"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV and convert numeric fields to numbers."""
    numeric_fields = (
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    )
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = []
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song and return its points and human-readable reasons."""
    score = 0.0
    reasons = []
    genre = str(user_prefs.get("favorite_genre", user_prefs.get("genre", ""))).lower()
    mood = str(user_prefs.get("favorite_mood", user_prefs.get("mood", ""))).lower()

    genre_weight = float(user_prefs.get("genre_weight", 2.0))
    mood_weight = float(user_prefs.get("mood_weight", 1.0))
    energy_weight = float(user_prefs.get("energy_weight", 1.0))

    if genre and str(song["genre"]).lower() == genre:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.2f})")

    if mood and str(song["mood"]).lower() == mood:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.2f})")

    if "target_energy" in user_prefs:
        energy_similarity = max(0.0, 1.0 - abs(float(song["energy"]) - float(user_prefs["target_energy"])))
        energy_points = energy_weight * energy_similarity
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if "target_tempo_bpm" in user_prefs:
        tempo_similarity = max(
            0.0,
            1.0 - abs(float(song["tempo_bpm"]) - float(user_prefs["target_tempo_bpm"])) / 40.0,
        )
        tempo_points = 0.5 * tempo_similarity
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    if "target_valence" in user_prefs:
        valence_similarity = max(0.0, 1.0 - abs(float(song["valence"]) - float(user_prefs["target_valence"])))
        valence_points = 0.5 * valence_similarity
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    if user_prefs.get("likes_acoustic") and float(song["acousticness"]) >= 0.5:
        score += 0.25
        reasons.append("acoustic preference (+0.25)")

    return score, reasons or ["content-based fit (no exact preference match)"]

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "genre-first",
    artist_penalty: float = 0.25,
    genre_penalty: float = 0.15,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return a diverse top-k ranking."""
    strategy = SCORING_STRATEGIES.get(mode.lower())
    if strategy is None:
        choices = ", ".join(SCORING_STRATEGIES)
        raise ValueError(f"Unknown scoring mode '{mode}'. Choose one of: {choices}")

    prefs = strategy.apply(user_prefs)
    ranked = []
    for song in songs:
        score, reasons = score_song(prefs, song)
        ranked.append((song, score, "; ".join(reasons)))

    selected = []
    remaining = sorted(ranked, key=lambda recommendation: (-recommendation[1], recommendation[0]["title"]))
    while remaining and len(selected) < max(0, k):
        selected_artists = {item[0]["artist"].lower() for item in selected}
        selected_genres = {item[0]["genre"].lower() for item in selected}
        diverse_ranked = []
        for song, score, explanation in remaining:
            adjusted_score = score
            if song["artist"].lower() in selected_artists:
                adjusted_score -= artist_penalty
            if song["genre"].lower() in selected_genres:
                adjusted_score -= genre_penalty
            diverse_ranked.append((adjusted_score, song, explanation))

        _, song, explanation = min(
            diverse_ranked,
            key=lambda item: (-item[0], item[1]["title"]),
        )
        adjusted_score = next(
            item[0] for item in diverse_ranked if item[1] is song
        )
        selected.append((song, adjusted_score, explanation))
        remaining.remove(next(item for item in remaining if item[0] is song))

    return selected
