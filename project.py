import random
import re
import sys
from fpdf import FPDF

# Define the Movie class
class Movie:
    def __init__(self, movie_id, name, genre):
        self.movie_id = movie_id
        self.name = name
        self.genre = genre

# Define the User class
class User:
    def __init__(self, name, profile):
        self.name = name
        self.profile = profile  # User's genre preferences
        self.liked_movies = []

    def give_feedback(self, movie):
        print(f"User: {self.name}, Movie: {movie.name}, Genre: {movie.genre}")
        feedback = int(input("Do you like this movie? (1 for like, 0 for dislike): "))
        if feedback == 1:
            self.liked_movies.append(movie.movie_id)
            self.profile[movie.genre] = min(1.0, self.profile[movie.genre] + 0.1)
            print("You liked the movie. Updating your profile...")
        else:
            print("You disliked the movie. No updates.")
        return feedback

# Define the RecommenderSystem class
class RecommenderSystem:
    def __init__(self, users, movies, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.users = {user.name: user for user in users}
        self.movies = {movie.movie_id: movie for movie in movies}
        self.q_table = {user.name: {movie.movie_id: 0 for movie in movies} for user in users}
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

    def choose_action(self, user_name):
        if random.random() < self.epsilon:  # Exploration
            return random.choice(list(self.movies.values()))
        else:  # Exploitation
            user_q_values = self.q_table[user_name]
            best_movie_id = max(user_q_values, key=user_q_values.get)
            return self.movies[best_movie_id]

    def update_q_table(self, user_name, movie, reward):
        current_q = self.q_table[user_name][movie.movie_id]
        best_future_q = max(self.q_table[user_name].values())
        new_q = current_q + self.alpha * (reward + self.gamma * best_future_q - current_q)
        self.q_table[user_name][movie.movie_id] = new_q

    def log_to_pdf(self, content):
        """Add a line of text to the PDF file."""
        self.pdf.multi_cell(0, 10, content)

    def save_pdf(self, filename):
        """Save the PDF file."""
        self.pdf.output(filename)

    def run_episode(self, episodes=5):
        total_rewards = {user: 0 for user in self.users}
        num_interactions = {user: 0 for user in self.users}
        total_system_rewards = 0

        for episode in range(episodes):
            for user_name, user in self.users.items():
                recommended_movie = self.choose_action(user_name)
                print(f"Recommended Movie: {recommended_movie.name}, {recommended_movie.genre}")
                feedback = user.give_feedback(recommended_movie)
                reward = 1 if feedback == 1 else -1
                self.update_q_table(user_name, recommended_movie, reward)
                total_rewards[user_name] += reward
                num_interactions[user_name] += 1
                total_system_rewards += reward

            # System evaluation at the end of each episode
            evaluation_report = f"\n--- Evaluation at Episode {episode} ---\n"
            self.log_to_pdf(evaluation_report)  # Save to PDF

            for user_name in self.users:
                avg_reward = total_rewards[user_name] / num_interactions[user_name]
                user_report = (
                    f"User: {user_name}\n"
                    f"Average Reward: {avg_reward:.2f}\n"
                    f"Q-table: {self.q_table[user_name]}\n"
                )
                self.log_to_pdf(user_report)  # Save to PDF

            system_report = (
                f"Total System Reward (All Users): {total_system_rewards}\n"
                f"Average System Reward per Interaction: "
                f"{total_system_rewards / sum(num_interactions.values()):.2f}\n"
            )
            self.log_to_pdf(system_report)  # Save to PDF

        # Save the PDF after running all episodes
        self.save_pdf("evaluation_report.pdf")
        print("PDF report saved as 'evaluation_report.pdf'.")

# First function: Get user input for user profiles
def get_user_input():
    users_input = []
    print("Enter user profiles (username-rate of Action-rate of Comedy-rate of Drama):")
    print("Example: User1-0.7-0.3-0.4")
    while True:
        user_data = input("Enter a user profile or 'done' to finish: ")
        if user_data.lower() == 'done':
            break
        users_input.append(user_data)
    return users_input

# Second function: Validate the input format using Regex
def validate_input_format(user_input):
    pattern = r"^[a-zA-Z 0-9]+-(0(\.[0-9]{1,2})?|1(\.0{1,2})?)-(0(\.[0-9]{1,2})?|1(\.0{1,2})?)-(0(\.[0-9]{1,2})?|1(\.0{1,2})?)$"
    if re.match(pattern, user_input):
        return user_input.split("-")
    else:
        print("Invalid format. Exiting...")
        sys.exit(1)

# Third function: Convert the input data into user dictionaries
def create_users_from_input(users_input):
    users = []
    for user_data in users_input:
        
        username, action_rate, comedy_rate, drama_rate = validate_input_format(user_data)
        profile = create_dic(action_rate, comedy_rate, drama_rate)
        
        users.append(User(username, profile))
    
    return users

# creation dictionary
def create_dic(action_rate, comedy_rate, drama_rate):
    profile = {
            "Action": float(action_rate),
            "Comedy": float(comedy_rate),
            "Drama": float(drama_rate)
        }
    return profile

# Main method that runs the program
def main():
    # Get user input
    users_input = get_user_input()
    
    # Create users from input
    users = create_users_from_input(users_input)
    
    # Define movies
    movies = [
        Movie(0, "Movie A", "Action"),
        Movie(1, "Movie B", "Comedy"),
        Movie(2, "Movie C", "Action"),
        Movie(3, "Movie D", "Drama"),
        Movie(4, "Movie E", "Comedy"),
    ]
    
    # Run the recommender system
    recommender = RecommenderSystem(users, movies, epsilon=0.1)
    recommender.run_episode(episodes=2)

# Run the main method
if __name__ == "__main__":
    main()
