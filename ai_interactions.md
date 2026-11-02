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

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
