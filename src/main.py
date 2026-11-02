"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "target_tempo_bpm": 120,
            "target_valence": 0.75,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "target_tempo_bpm": 78,
            "target_valence": 0.58,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "target_tempo_bpm": 150,
            "target_valence": 0.45,
        },
        "Conflicting High-Energy Sad": {
            "favorite_genre": "rock",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "target_tempo_bpm": 140,
            "target_valence": 0.25,
        },
    }

    energy_experiment = {
        **profiles["High-Energy Pop"],
        "genre_weight": 1.0,
        "energy_weight": 2.0,
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\nProfile: {profile_name}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("Top recommendations:")
        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Reasons: {explanation}")
        print()

    print("Experiment: High-Energy Pop with energy doubled and genre halved")
    for song, score, explanation in recommend_songs(energy_experiment, songs, k=5):
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Reasons: {explanation}")


if __name__ == "__main__":
    main()
