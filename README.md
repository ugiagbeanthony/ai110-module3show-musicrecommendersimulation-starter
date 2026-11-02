# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

VibeFinder 1.0 is a CLI-first content-based music recommender that scores an 18-song catalog against explicit user preferences. It prioritizes genre and mood, uses proximity scores for energy, tempo, and valence, and applies artist and genre diversity penalties before returning the top recommendations with explanations.

---

## How The System Works

Major streaming platforms usually combine signals from many listeners with song content. Collaborative filtering compares user behavior, such as likes, skips, saves, listening history, and playlist membership, to find users or tracks with similar patterns. Content-based filtering instead compares the attributes of tracks the user already likes, such as genre, mood, tempo, energy, valence, danceability, and acousticness, with other songs. Real systems usually blend both approaches with context, popularity, freshness, and recency-aware models.

This simulator is a small content-based recommender. It will prioritize genre and mood matches because those are strong categorical descriptions of a listening preference, then use numerical closeness for energy, tempo, valence, danceability, and acousticness. For example, a numerical score can reward proximity instead of always favoring larger values:

```text
numerical similarity = 1 - |song_value - user_target| / value_range
```

The final `Song` score can also use weighted categorical and numerical matches. Each recommendation can be calculated with:

```text
score = genre_weight + mood_weight + numerical_feature_similarities
```

### Finalized Algorithm Recipe

The simulator uses this example user profile:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "target_tempo_bpm": 120,
    "target_valence": 0.75,
}
```

This profile is high-energy and positive rather than generic. A pop track at roughly 0.8 energy can be distinguished from chill lofi even if both moods are not exact matches: genre and mood should contribute strongly, and lofi's lower energy and acoustic character should reduce the numerical match. However, the exact targets should not prevent discovery of songs with a slightly lower energy.

Weighting:

- Genre match: **+2.0 points**
- Mood match: **+1.0 point**
- Energy similarity: **up to +1.0 point**, calculated as `1 - abs(song_energy - target_energy)`
- Tempo similarity: **up to +0.5 point**, calculated proportionally within a 40 BPM tolerance
- Valence similarity: **up to +0.5 point**, calculated as `1 - abs(song_valence - target_valence)`
- Acousticness: optional category preference contributing no more than **0.25 points**

Genre is weighted higher than mood because genre represents a broader listening identity, while mood is a more temporary context. The full data flow is:

```text
User Preferences
      |
      v
Catalog CSV -> Load songs -> Judge each song with scoring rule
                                      |
                                      v
                         Calculate every song's total score
                                      |
                                      v
                         Sort descending -> Return top K
```

The scoring rule evaluates one song and explains its points. The ranking rule compares every song's score and selects the top `k`, making the scoring and ranking stages separate.

### Expected Biases and Limitations

The fixed weights may over-prioritize genre and ignore a song with an excellent mood or energy match from another genre. Mood labels are subjective, the tiny catalog lacks enough examples from some genres, and artificial distance thresholds can make small feature differences look more important than they are. No collaborative signals such as skips, saves, playlists, or listening history are modeled yet, so the system cannot learn broad listener trends or preferences from behavior.

A scoring rule gives one song a score and reasons. A ranking rule scores every candidate, sorts them from highest to lowest score, breaks ties predictably, and returns the top `k`. Both rules are necessary: scoring evaluates a single match, while ranking turns the full catalog into an ordered recommendation list.

### Features Used

The simulator's `Song` objects use:

- `id`, `title`, and `artist`
- `genre` and `mood`
- `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`

The `UserProfile` stores a favorite genre, favorite mood, target energy, and preference for acoustic music. The main content-based preference uses genre, mood, and energy; tempo, valence, danceability, and acousticness provide additional profile detail or secondary weights.

### Feature Choice

Genre and mood are the most useful categorical features for this small catalog because they clearly distinguish the examples. Energy and valence are especially useful numerically: energy captures intensity, while valence captures musical positivity. Tempo adds useful rhythm information but should not dominate mood. Danceability and acousticness further describe how a track feels and sounds. This aligns with everyday ideas of vibe, though genre is not a perfect proxy for taste and mood labels can be subjective.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate                 # macOS/Linux/Git Bash
   .\.venv\Scripts\Activate.ps1              # Windows PowerShell
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

The CLI output for the default pop/happy profile is:

```text
Loaded songs: 18

Top recommendations:

Sunrise City - Score: 4.91
Reasons: genre match (+2.0); mood match (+1.0); energy similarity (+0.98); tempo similarity (+0.47); valence similarity (+0.46)

Gym Hero - Score: 3.71
Reasons: genre match (+2.0); energy similarity (+0.87); tempo similarity (+0.35); valence similarity (+0.49)

Rooftop Lights - Score: 2.88
Reasons: mood match (+1.0); energy similarity (+0.96); tempo similarity (+0.45); valence similarity (+0.47)

Neon Circuit - Score: 1.70
Reasons: energy similarity (+0.87); tempo similarity (+0.40); valence similarity (+0.43)

Night Drive Loop - Score: 1.69
Reasons: energy similarity (+0.95); tempo similarity (+0.38); valence similarity (+0.37)
```

**Screenshot or video** *(optional)*: No screenshot included; the text output above records the CLI result.

---

## Experiments You Tried

I tested High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting high-energy sad profile. The pop and lofi lists were clearly different, while the rock list favored Storm Runner. In an experiment, I doubled the energy weight and halved the genre weight for the pop profile; Sunrise City remained first, Rooftop Lights moved ahead of Gym Hero, and an unrelated high-energy track entered the list. This showed that energy creates variety but can reduce genre specificity.

---

## Limitations and Risks

The recommender uses a tiny catalog, fixed weights, and no listening-history signals. It does not understand lyrics, language, artist similarity, audio quality, or broader cultural context. It can over-prioritize genre, favor a numerically similar song from the wrong style, and repeat the strongest artist or genre unless diversity penalties reduce that effect.

---

## Reflection

This project showed that even simple weighted rules can create results that feel personalized when genre, mood, and numerical similarity are combined. It also showed where bias can enter: a small catalog, subjective mood labels, fixed thresholds, and heavy categorical weights shape the list before any learning occurs. The complete limitations and evaluation are documented in the [Model Card](model_card.md).
