from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    recommend_songs,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_scoring_modes_return_different_modular_rankings():
    songs = [
        {"title": "Genre Song", "artist": "A", "genre": "pop", "mood": "sad", "energy": 0.5,
         "tempo_bpm": 100, "valence": 0.5, "danceability": 0.5, "acousticness": 0.2},
        {"title": "Mood Song", "artist": "B", "genre": "rock", "mood": "happy", "energy": 0.5,
         "tempo_bpm": 100, "valence": 0.5, "danceability": 0.5, "acousticness": 0.2},
    ]
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.5,
    }

    genre_first = recommend_songs(prefs, songs, k=1, mode="genre-first")
    mood_first = recommend_songs(prefs, songs, k=1, mode="mood-first")

    assert genre_first[0][0]["title"] == "Genre Song"
    assert mood_first[0][0]["title"] == "Mood Song"


def test_artist_and_genre_diversity_penalties():
    songs = [
        {"title": "First", "artist": "Same Artist", "genre": "pop", "mood": "happy", "energy": 0.8,
         "tempo_bpm": 120, "valence": 0.75, "danceability": 0.8, "acousticness": 0.2},
        {"title": "Second", "artist": "Same Artist", "genre": "pop", "mood": "happy", "energy": 0.79,
         "tempo_bpm": 119, "valence": 0.74, "danceability": 0.8, "acousticness": 0.2},
        {"title": "Third", "artist": "Other Artist", "genre": "rock", "mood": "happy", "energy": 0.5,
         "tempo_bpm": 100, "valence": 0.6, "danceability": 0.5, "acousticness": 0.2},
    ]

    results = recommend_songs(
        {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8},
        songs,
        k=3,
    )

    assert len({song["artist"] for song, _, _ in results}) >= 2
