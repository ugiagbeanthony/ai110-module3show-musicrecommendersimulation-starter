# AI Interactions Log

## Recommendation Research

**Prompt:**

> Research how major music streaming platforms predict the song a user is likely to love next. Explain the difference between collaborative filtering, which uses patterns from other users' behavior, and content-based filtering, which uses attributes of the songs themselves. Also identify key interaction data (likes, dislikes, skips, saves, playlists, listening history, and recency) and song-content data (genre, mood, tempo, energy, valence, danceability, and acousticness). Describe a simple example of each approach and where a hybrid recommender would be useful.

**Summary of the AI-assisted analysis:**

- Collaborative filtering can recommend a track liked by users with behavior similar to the current user without knowing what the audio features mean.
- Content-based filtering compares song attributes, and is especially useful when little user-history data exists or when avoiding dependence on popularity.
- Likes and saves are usually positive signals; skips and short listens are negative signals, but their meaning depends on context. Playlists provide stronger relationships between songs than a single interaction.
- The simulator uses content-based reasoning with weighted genre and mood matches plus proximity scores for numerical features.

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Implement and verify this phase of the music recommender, including multiple scoring strategies and diversity-aware ranking.

**Prompts used:**

Prompts asked for genre-first, mood-first, and energy-focused modes, a Strategy design pattern, artist and genre diversity penalties, focused tests, and documentation in the interaction log.

**What did the agent generate or change?**

The agent added strategy classes and a strategy registry, CLI mode selection, candidate penalties in `recommend_songs()`, Strategy documentation, and focused strategy/diversity tests in `src/recommender.py`, `src/main.py`, `ai_interactions.md`, and `tests/test_recommender.py`.

**What did you verify or fix manually?**

I verified the generated CLI output, ran the complete pytest suite, reviewed the strategy weight changes and diversity ordering, and corrected any documentation or integration issues found during validation.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The Strategy design pattern.

**How did AI help you brainstorm or implement it?**

AI suggested separating each ranking profile into an object with a common `apply(user_prefs)` interface. This keeps weight selection modular and lets the CLI switch between `genre-first`, `mood-first`, and `energy-focused` without changing the shared scoring or ranking loop.

**How does the pattern appear in your final code?**

`ScoringStrategy`, `GenreFirstStrategy`, `MoodFirstStrategy`, and `EnergyFocusedStrategy` are in `src/recommender.py`. `recommend_songs()` selects the requested strategy from `SCORING_STRATEGIES`, applies its weights, and performs diversity-aware ranking.
