# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

Goal / task: suggest the five songs from the small catalog that best match a user's preferred genre, mood, energy, tempo, and valence.

---

## 2. Intended Use  

VibeFinder generates simple ranked recommendations for classroom exploration. It assumes that a user expresses taste through a few explicit preferences and that closeness in song attributes represents preference similarity. It is not intended for commercial music delivery or decisions with real personal or business consequences.

It should not be used to infer sensitive traits, judge people, or make recommendations from only one profile feature. Real users need more data, privacy controls, and ways to correct recommendations.

---

## 3. How the Model Works  

The model compares each song with one sample taste profile. A matching genre earns 2 points, a matching mood earns 1 point, and closer energy, tempo, and valence values earn similarity points. The recommender calculates a score for every song, sorts the scores from highest to lowest, and displays the top results with a short explanation. This is a content-based approach rather than collaborative filtering: it uses attributes of the songs instead of learning from other listeners.

---

## 4. Data  

The catalog contains 18 songs with 15 genres and several moods. Each track includes tempo, energy, valence, danceability, and acousticness. The expanded catalog is broad enough for simple demonstrations, but it is too small to represent real music preferences and does not include listening history, skips, saves, or collaborative behavior.

---

## 5. Strengths  

The recommender works best when genre, mood, and target energy strongly agree. Chill Lofi and Deep Intense Rock produced focused lists that matched their profiles. The score explanations also make the result easy to inspect, because each total shows exactly how genre, mood, and numerical similarity contributed.

---

## 6. Limitations and Bias 

The 18-song catalog is sparse, so matching genre is very influential even though only a few tracks represent many genres. Fixed numeric targets can also produce unexpected results for conflicting preferences: a high-energy profile can rank an intense song above a happy pop song because energy similarity outweighs catalog-context differences. The model has no collaborative listening signals, short-list diversity control, freshness, or penalties for repeatedly recommending popular tracks. A profile with a mood absent from the catalog receives no mood-match points and may appear poorly represented.

---

## 7. Evaluation  

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting High-Energy Sad profile. Sunrise City ranked first for the high-energy pop profile, while Midnight Coding and Library Rain topped the chill profile. The pop and lofi outputs were clearly different because genre, mood, energy, and acoustic preference all reinforce one style.

The rock profile placed Storm Runner first, followed by Afterburn and Gym Hero. Comparing that output with the pop profile shows that genre and mood changed the ranking rather than only energy: Gym Hero could rank highly for multiple profiles because its 0.93 energy is numerically close to both targets. This is reasonable, but it demonstrates that numerical similarity alone cannot identify genre or context.

The conflicting profile requested rock, an unavailable sad mood, and 0.9 energy. Storm Runner ranked first because it matched both rock and high energy, even though the sad mood could not be matched. This exposed a limitation: mismatched moods simply lose points, and no penalty or conflict resolution tells the user that the requested combination is unusual.

As a sensitivity experiment, I doubled energy and halved genre weight for the High-Energy Pop profile. Sunrise City remained first, while Rooftop Lights moved above Gym Hero. General high-energy tracks such as City Rhythm also entered the top five. The experiment made energy more important, but it could also recommend songs from unrelated genres, so increased numerical sensitivity made the system more exploratory but less genre-specific.

```text
High-Energy Pop:
1. Sunrise City - 4.91
2. Gym Hero - 3.71
3. Rooftop Lights - 2.88
4. Neon Circuit - 1.70
5. Night Drive Loop - 1.69

Chill Lofi:
1. Midnight Coding - 5.22
2. Library Rain - 5.12
3. Focus Flow - 4.22
4. Spacewalk Thoughts - 2.87
5. Coffee Shop Stories - 2.00

Deep Intense Rock:
1. Storm Runner - 4.92
2. Afterburn - 2.71
3. Gym Hero - 2.59
4. Neon Circuit - 1.37
5. Rooftop Lights - 1.31

Energy-weighted experiment:
1. Sunrise City - 4.89
2. Rooftop Lights - 3.84
3. Gym Hero - 3.58
4. City Rhythm - 2.67
5. Night Drive Loop - 2.65
```

---

## 8. Future Work  

- Add more songs from each genre so matching does not depend on a tiny catalog.
- Add exclusion rules, taste diversity, and a clearer conflict warning for unavailable or incompatible preferences.
- Let users provide likes, skips, and saved songs so the system can learn instead of relying only on manual targets.

---

## 9. Personal Reflection  

My biggest learning moment was seeing that a few understandable rules can produce convincing recommendations, while small changes to weights can strongly change the list. I used AI tools to brainstorm features, prompts, experimental weights, and documentation. I needed to double-check CSV data, formulas, generated output, and tests because AI suggestions were hypotheses, not proof.

I was surprised that simple energy similarity could make Gym Hero appear relevant to several listeners, even when their genre and mood were different. I would next add listening-history signals, diversity filtering, better profile editing, and tests comparing alternate weights across more profiles.
