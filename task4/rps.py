import random
import time
import json
import os
from datetime import datetime

class RockPaperScissors:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.scores = {'user': 0, 'computer': 0, 'ties': 0}
        self.history = []
        self.scoreboard_file = 'rps_scoreboard.json'
        self.load_scoreboard()

    def load_scoreboard(self):
        if os.path.exists(self.scoreboard_file):
            try:
                with open(self.scoreboard_file, 'r') as f:
                    self.high_scores = json.load(f)
            except:
                self.high_scores = {'best_streak': 0, 'total_games': 0, 'total_wins': 0}
        else:
            self.high_scores = {'best_streak': 0, 'total_games': 0, 'total_wins': 0}

    def save_scoreboard(self):
        with open(self.scoreboard_file, 'w') as f:
            json.dump(self.high_scores, f)

    def get_user_choice(self):
        while True:
            print("\nChoose your move:")
            print("1. Rock 🪨")
            print("2. Paper 📄")
            print("3. Scissors ✂️")
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice in ['1', '2', '3']:
                return self.choices[int(choice) - 1]
            print("Invalid choice! Please enter 1, 2, or 3.")

    def get_computer_choice(self):
        return random.choice(self.choices)

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'tie'
        
        winning_combinations = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        
        if winning_combinations[user_choice] == computer_choice:
            return 'user'
        return 'computer'

    def display_choices(self, user_choice, computer_choice):
        emoji_map = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️'
        }
        
        print(f"\nYour choice: {user_choice.upper()} {emoji_map[user_choice]}")
        print("Computer is choosing", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print(f"\nComputer's choice: {computer_choice.upper()} {emoji_map[computer_choice]}")

    def display_result(self, result):
        if result == 'tie':
            print("\n🎯 It's a tie!")
        elif result == 'user':
            print("\n🎉 Congratulations! You win!")
        else:
            print("\n😔 Computer wins!")

    def update_scores(self, result):
        self.scores[result if result != 'tie' else 'ties'] += 1
        self.history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'result': result
        })

    def display_scores(self):
        print("\n=== Current Scores ===")
        print(f"You: {self.scores['user']} 👤")
        print(f"Computer: {self.scores['computer']} 🤖")
        print(f"Ties: {self.scores['ties']} 🎯")

    def display_statistics(self):
        total_games = sum(self.scores.values())
        if total_games == 0:
            return
        
        win_rate = (self.scores['user'] / total_games) * 100
        current_streak = 0
        best_streak = 0
        
        for game in reversed(self.history):
            if game['result'] == 'user':
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                break

        print("\n=== Game Statistics ===")
        print(f"Total Games: {total_games}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Current Streak: {current_streak}")
        print(f"Best Streak: {max(best_streak, self.high_scores['best_streak'])}")

    def play_game(self):
        while True:
            print("\n=== Rock Paper Scissors ===")
            user_choice = self.get_user_choice()
            computer_choice = self.get_computer_choice()
            
            self.display_choices(user_choice, computer_choice)
            result = self.determine_winner(user_choice, computer_choice)
            
            self.display_result(result)
            self.update_scores(result)
            self.display_scores()
            
            # Update high scores
            self.high_scores['total_games'] += 1
            if result == 'user':
                self.high_scores['total_wins'] += 1
                current_streak = sum(1 for game in reversed(self.history) 
                                  if game['result'] == 'user')
                self.high_scores['best_streak'] = max(
                    self.high_scores['best_streak'], 
                    current_streak
                )
            
            self.save_scoreboard()
            self.display_statistics()
            
            if not self.play_again():
                break

    def play_again(self):
        while True:
            choice = input("\nWould you like to play again? (y/n): ").lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("Please enter 'y' for yes or 'n' for no.")

    def show_rules(self):
        print("\n=== Game Rules ===")
        print("🪨 Rock beats ✂️ Scissors")
        print("📄 Paper beats 🪨 Rock")
        print("✂️ Scissors beats 📄 Paper")
        input("\nPress Enter to continue...")

def main():
    game = RockPaperScissors()
    
    print("Welcome to Rock Paper Scissors!")
    print("\n1. Start Game")
    print("2. Show Rules")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            game.play_game()
            break
        elif choice == '2':
            game.show_rules()
        elif choice == '3':
            print("\nThanks for playing!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()