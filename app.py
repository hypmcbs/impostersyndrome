

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import sys
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class ImposterGame:
    def __init__(self):
        self.name = ""
        self.score = 0
        self.current_step = "intro"
        self.choices = {}
    
    def process_input(self, user_input, step=None):
        if step:
            self.current_step = step
            
        if self.current_step == "intro":
            self.name = user_input
            self.current_step = "score"
            print("I'm very sorry your feeling this way.")
            return f" {self.name}! How would you rate your accomplishments as of right now? (0-10)"
        
        elif self.current_step == "score":
            try:
                self.score = int(user_input)
                self.current_step = "listA"
                return ("You have a huge leadership job at a massive tech company. You have earned millions of dollars and have led your company to earn billions of dollars.\n\n"
                       "But you can't seem to notice any of your hundreds of achievements. You feel like your achievements are invalid and don't matter.\n\n"
                       "To fix this feeling do you make a list of achievements and relize your potetnial or do nothing and try to shake the feeling")
            except ValueError:
                return "Please enter a number between 0 and 10."
        
        elif self.current_step == "listA":
            self.choices["listA"] = user_input.lower()
            if "do nothing" in user_input.lower():
                self.current_step = "redo_listA"
                return "This will not be helpful in the long term. Understand your achmlishpmets are so valid and you are worthy of what you have earned."
            elif "list" in user_input.lower() or "make" in user_input.lower():
                self.current_step = "help"
                return ("Exactly! This is an amazing way to cope with feeling as if you have no accomplishments, even though you have tons!\n\n"
                       "But as you look through this list, you realize you had a team for each of these projects. You begin to believe you are a fraud because you needed help.\n\n"
                       "Do you quit your job so you can be independent or do you realize that teamwork is essential?")
            else:
                return "I didn't understand that. Please choose to either make a list or sulk."
        
        elif self.current_step == "redo_listA":
            self.choices["listA"] = user_input.lower()
            if "list" in user_input.lower() or "make" in user_input.lower():
                self.current_step = "make a list"
                return ("Exactly! This is an amazing way to cope with feeling as if you have no accomplishments, even though you have tons!\n\n"
                       "But as you look through this list, you realize you had a team for each of these projects. You begin to believe you are a fraud because you needed help.\n\n"
                       "Do you quit your job so you can be independent or do you realize that teamwork is essential?")
            else:
                return "I didn't understand that. Please choose to make a list or do nothing."
        
        elif self.current_step == "help":
            self.choices["help"] = user_input.lower()
            if "quit" in user_input.lower():
                self.current_step = "animal"
                return ("That's one approach, but working alone isn't always better. Many great achievements come from collaboration.\n\n"
                       "Let's shift gears. Please name an animal that you like:")
            elif "real" in user_input.lower() or "team" in user_input.lower() or "essential" in user_input.lower():
                self.current_step = "animal"
                return ("That's right! Teamwork doesn't diminish your contributions. Great leaders know how to leverage diverse talents.\n\n"
                       "Let's shift gears. Please name an animal that you like:")
            else:
                return "Please choose to either quit your job or realize the importance of teamwork."
        
        elif self.current_step == "animal":
            self.choices["animal"] = user_input
            self.current_step = "habitat"
            return f"Where does a {user_input} typically live? (Name a habitat)"
        
        elif self.current_step == "habitat":
            self.choices["habitat"] = user_input
            self.current_step = "adjective"
            return "Give me an adjective that describes how you're feeling right now:"
        
        elif self.current_step == "adjective":
            self.choices["adjective"] = user_input
            self.current_step = "subject"
            return "Name a subject or topic you enjoy learning about:"
        
        elif self.current_step == "subject":
            self.choices["subject"] = user_input
            self.current_step = "final"
            
            # Create personalized story based on user choices
            story = (f"Dear {self.name},\n\n"
                    f"Just like the {self.choices['adjective']} {self.choices['animal']} thrives in the {self.choices['habitat']}, "
                    f"you too are perfectly suited for your leadership role. Your passion for {self.choices['subject']} shows how you "
                    f"bring unique perspectives to your team.\n\n"
                    f"Remember, feeling like an impostor is common among high achievers. In fact, your initial score of {self.score}/10 "
                    f"shows how you tend to undervalue your contributions. The fact that you chose to ")
            
            if "list" in self.choices.get("listA", ""):
                story += "make a list of achievements reveals your proactive nature. "
            else:
                story += "reconsider your approach shows your adaptability. "
                
            if "real" in self.choices.get("help", "") or "team" in self.choices.get("help", "") or "essential" in self.choices.get("help", ""):
                story += ("And your understanding that teamwork enhances rather than diminishes your contributions "
                         "demonstrates your emotional intelligence and leadership wisdom.\n\n")
            else:
                story += ("Even though you considered quitting, deep down you know that collaboration "
                         "is where true innovation happens.\n\n")
                
            story += ("You're not an impostor. You're a leader who has earned their position "
                     "through hard work, skill, and the ability to bring out the best in others. "
                     "Trust yourself as much as others trust you.")
            
            return story
        
        else:
            return "Thank you for playing the Imposter Syndrome game! Refresh to play again."

game = ImposterGame()

@app.route('/game', methods=['POST'])
def process_input():
    data = request.json
    user_input = data.get('text', '')
    step = data.get('step', None)
    
    response = game.process_input(user_input, step)
    
    return jsonify({
        'response': response,
        'current_step': game.current_step,
        'choices': game.choices
    })

@app.route('/reset-game', methods=['POST'])
def reset_game():
    global game
    game = ImposterGame()
    return jsonify({'status': 'Game reset successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)