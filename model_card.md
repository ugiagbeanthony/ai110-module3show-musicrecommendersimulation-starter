# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model compares each song with one sample taste profile. A matching genre earns 2 points, a matching mood earns 1 point, and closer energy, tempo, and valence values earn similarity points. The recommender calculates a score for every song, sorts the scores from highest to lowest, and displays the top results with a short explanation. This is a content-based approach rather than collaborative filtering: it uses attributes of the songs instead of learning from other listeners.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 18 songs with 15 genres and several moods. Each track includes tempo, energy, valence, danceability, and acousticness. The expanded catalog is broad enough for simple demonstrations, but it is too small to represent real music preferences and does not include listening history, skips, saves, or collaborative behavior.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The 18-song catalog is sparse, so matching genre is very influential even though only a few tracks represent many genres. Fixed numeric targets can also produce unexpected results for conflicting preferences: a high-energy profile can rank an intense song above a happy pop song because energy similarity outweighs catalog-context differences. The model has no collaborative listening signals, short-list diversity control, freshness, or penalties for repeatedly recommending popular tracks. A profile with a mood absent from the catalog receives no mood-match points and may appear poorly represented.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
