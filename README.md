# Recommendation Favorite Genre

#### Video Demo: [Watch Here](https://www.youtube.com/watch?v=5g18FqyOIo4)

#### Description:
The **Recommendation Favorite Genre** project is a movie recommender system that uses a reinforcement learning approach, specifically **Q-learning**, to suggest movies tailored to user preferences. Users interact with the system by providing feedback on recommended movies, which dynamically updates their preferences and improves subsequent recommendations.

### Features:
- **User Input**: Users input their preferences for genres in a structured format (e.g., `username-rate of Action-rate of Comedy-rate of Drama`).
- **Validation**: Input is validated using a regex pattern to ensure correctness.
- **Dynamic Learning**: User feedback is used to refine future recommendations.
- **Q-Learning**: The system balances exploration of new movies and exploitation of learned user preferences.
- **PDF Reporting**: Generates a detailed evaluation report after running episodes.

### Key Components:
1. **Movie Class**:
   - Represents individual movies with attributes like `movie_id`, `name`, and `genre`.

2. **User Class**:
   - Stores user preferences and tracks liked movies.
   - Updates genre preferences based on user feedback.

3. **Recommender System Class**:
   - Manages the recommendation process, Q-learning updates, and logging.
   - Generates a PDF summary of performance metrics.

4. **Input Functions**:
   - `get_user_input`: Collects user profiles.
   - `validate_input_format`: Validates input format with a regular expression.
   - `create_users_from_input`: Converts input into `User` objects.

### How It Works:
1. Users provide their profiles, specifying their preferences for genres.
2. The system recommends movies based on exploration (random selection) or exploitation (best Q-value).
3. Users give feedback (like or dislike) for each recommended movie.
4. The system updates:
   - Q-values for user-movie interactions.
   - User profiles if they like a movie.
5. After multiple episodes, the system generates a PDF evaluation report.

### Files Included:
- `project.py`: The main code for the recommendation system.
- `test_project.py`: Unit tests for the supporting functions.
- `request.txt`: List of Python libraries required to run the project.
- `README.md`: Documentation for the project.

### Requirements:
- Python 3.x
- Libraries: `FPDF`, `re`, `random`, `sys`

To install the necessary libraries, run:
```bash
pip install -r request.txt
```

### Usage:
1. Run the `project.py` file.
2. Enter user profiles when prompted.
3. Interact with the system by providing feedback on recommended movies.
4. Check the generated `evaluation_report.pdf` for performance metrics.

### Test Instructions:
Run `test_project.py` to validate the supporting functions:
```bash
pytest test_project.py
```

#### Additional Notes:
- This project demonstrates how reinforcement learning principles can be applied in real-world applications.
- The generated PDF provides insight into user interactions and system performance.

