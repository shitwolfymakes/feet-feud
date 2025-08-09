# Feet Feud Web Game

A web-based implementation of the classic Family Feud game show using Flask and SQLite. Perfect for hosting live game show events with a presentation-style interface. Now supports custom questions via JSON import!

## Features

- **Presentation-style gameplay** - Host controls with click-to-reveal answers
- **Two-team scoring** with customizable team names
- **Real-time host controls** - Add strikes, switch teams, award steals
- **Classic Family Feud mechanics** - 3 strikes and steal opportunities
- **JSON question import** - Load custom questions from JSON files
- **Responsive design** that works on desktop and mobile
- **Sample questions** included to get started immediately
- **Round management** - Reset rounds, next question, score tracking

## Game Rules

1. **Teams take turns** calling out answers to survey questions
2. **Host clicks answers** to reveal correct responses and add points
3. **Wrong answers get strikes** - host clicks "Add Strike" button
4. **After 3 strikes**, the opposing team gets one chance to "steal" all accumulated points
5. **Host controls everything** - reveals, scoring, team switching, and round management
6. **The team with the most points wins!**

## Installation

### 1. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Make sure you're in the activated virtual environment
# (you should see (venv) in your terminal prompt)

pip install Flask==3.3
```

### 3. Setup Project Structure

Create the following folder structure:
```
feet-feud/
├── app.py
├── requirements.txt
├── README.md
├── questions.json (optional - for custom questions)
└── templates/
    ├── base.html
    ├── index.html
    ├── new_game.html
    └── game.html
```

### 4. Run the Application

```bash
# With default sample questions
python app.py

# With custom questions from JSON file
python app.py questions.json
```

### 5. Access the Game

Open your web browser and go to:
```
http://localhost:5000
```

### 6. Deactivating Virtual Environment

When you're done, deactivate the virtual environment:
```bash
deactivate
```

## Loading Custom Questions from JSON

### JSON File Format

Create a JSON file with the following structure:

```json
{
  "questions": [
    {
      "question": "Name something you find in a bathroom",
      "answers": [
        {"answer": "Toilet", "points": 35},
        {"answer": "Sink", "points": 25},
        {"answer": "Mirror", "points": 15},
        {"answer": "Towel", "points": 10},
        {"answer": "Bathtub/Shower", "points": 8},
        {"answer": "Toothbrush", "points": 4},
        {"answer": "Soap", "points": 2},
        {"answer": "Medicine Cabinet", "points": 1}
      ]
    },
    {
      "question": "Name a popular social media platform",
      "answers": [
        {"answer": "Facebook", "points": 30},
        {"answer": "Instagram", "points": 25},
        {"answer": "TikTok", "points": 20},
        {"answer": "Twitter/X", "points": 10},
        {"answer": "LinkedIn", "points": 7},
        {"answer": "Snapchat", "points": 5},
        {"answer": "YouTube", "points": 2},
        {"answer": "Pinterest", "points": 1}
      ]
    }
  ]
}
```

### Loading Questions

There are three ways to load questions:

1. **Default Sample Questions** - Just run without arguments:
   ```bash
   python app.py
   ```

2. **Custom JSON File** - Provide path to your JSON file:
   ```bash
   python app.py my_questions.json
   ```

3. **Multiple JSON Files** - Create different files for different themes:
   ```bash
   # Sports-themed questions
   python app.py sports_questions.json
   
   # Holiday-themed questions
   python app.py holiday_questions.json
   
   # Office-themed questions
   python app.py office_questions.json
   ```

### Important Notes about JSON Import

- **Replaces all existing questions** - Loading from JSON clears the database first
- **Points are automatically sorted** - Answers will be ordered by points (highest first)
- **Validation included** - Invalid JSON format will fall back to default questions
- **UTF-8 encoding supported** - Can include special characters and emojis
- **No limit on questions** - Add as many questions and answers as needed

### Example Custom Questions File

Create `custom_questions.json`:

```json
{
  "questions": [
    {
      "question": "Name something you do on vacation",
      "answers": [
        {"answer": "Relax/Sleep", "points": 25},
        {"answer": "Sightseeing", "points": 20},
        {"answer": "Swimming", "points": 18},
        {"answer": "Eating out", "points": 15},
        {"answer": "Shopping", "points": 10},
        {"answer": "Take photos", "points": 7},
        {"answer": "Reading", "points": 3},
        {"answer": "Hiking", "points": 2}
      ]
    },
    {
      "question": "Name a type of weather",
      "answers": [
        {"answer": "Sunny", "points": 30},
        {"answer": "Rainy", "points": 25},
        {"answer": "Cloudy", "points": 15},
        {"answer": "Snowy", "points": 12},
        {"answer": "Windy", "points": 8},
        {"answer": "Foggy", "points": 5},
        {"answer": "Stormy", "points": 3},
        {"answer": "Hail", "points": 2}
      ]
    },
    {
      "question": "Name something found in a wallet",
      "answers": [
        {"answer": "Money/Cash", "points": 35},
        {"answer": "Credit Cards", "points": 25},
        {"answer": "Driver's License", "points": 20},
        {"answer": "Photos", "points": 8},
        {"answer": "Business Cards", "points": 5},
        {"answer": "Receipts", "points": 4},
        {"answer": "Insurance Card", "points": 2},
        {"answer": "Gift Cards", "points": 1}
      ]
    }
  ]
}
```

Then run:
```bash
python app.py custom_questions.json
```

## Hosting a Game

### Pre-Game Setup
1. **Connect to projector/TV** for audience viewing
2. **Prepare questions** - Use default or load custom JSON file
3. **Start the application** and navigate to the game URL
4. **Create new game** with team names
5. **Explain rules** to participants

### During Gameplay
1. **Teams call out answers** - you don't type anything
2. **Click answer slots** to reveal correct responses
3. **Click "Add Strike"** when teams guess incorrectly
4. **Watch the strike counter** - after 3 strikes, steal opportunity appears
5. **Click "Award Steal"** then click a correct answer if the stealing team succeeds
6. **Use "Switch Team"** to award points and change control
7. **Use "Reset Round"** if you need to start the current question over
8. **Click "Next Round"** for a new question

### Host Controls Reference
- **🎯 Click Answer Slots** - Reveal correct answers and add points
- **❌ Add Strike** - Add strike for wrong answers
- **🔄 Switch Team** - Award current points to team and switch control
- **🎯 Award Steal** - Enable steal mode for opposing team
- **🎲 Next Round** - Load new question (awards current points first)
- **🔄 Reset Round** - Hide all answers and reset strikes/points
- **🏁 End Game** - Return to home screen

## File Structure

- `app.py` - Main Flask application with all game logic
- `templates/base.html` - Base HTML template with styling
- `templates/index.html` - Home page
- `templates/new_game.html` - Team setup page
- `templates/game.html` - Main game interface with host controls
- `feet_feud.db` - SQLite database (created automatically)
- `requirements.txt` - Python dependencies
- `questions.json` - Optional JSON file for custom questions

## Database Schema

The game uses three main tables:

- **questions** - Stores survey questions
- **answers** - Stores possible answers with point values
- **games** - Tracks active game sessions with scores and state
- **revealed_answers** - Tracks which answers have been revealed in each game

## Adding Questions Programmatically

Besides JSON import, you can also add questions directly to the database:

```python
import sqlite3
conn = sqlite3.connect('feet_feud.db')
cursor = conn.cursor()

# Add a question
cursor.execute('INSERT INTO questions (question) VALUES (?)', 
               ('Name something you find in a bathroom',))
question_id = cursor.lastrowid

# Add answers (answer, points)
answers = [
    ('Toilet', 35),
    ('Sink', 25),
    ('Mirror', 15),
    ('Towel', 10),
    ('Bathtub/Shower', 8),
    ('Toothbrush', 4),
    ('Soap', 2),
    ('Medicine Cabinet', 1)
]

for answer, points in answers:
    cursor.execute('INSERT INTO answers (question_id, answer, points) VALUES (?, ?, ?)',
                   (question_id, answer, points))

conn.commit()
conn.close()
```

## Creating Theme-Based Question Sets

You can create different JSON files for different occasions:

### Holiday Questions (`holiday_questions.json`)
```json
{
  "questions": [
    {
      "question": "Name a Christmas tradition",
      "answers": [
        {"answer": "Decorating tree", "points": 35},
        {"answer": "Opening presents", "points": 25},
        {"answer": "Christmas dinner", "points": 15},
        {"answer": "Singing carols", "points": 10},
        {"answer": "Santa Claus", "points": 8},
        {"answer": "Stockings", "points": 4},
        {"answer": "Cookies for Santa", "points": 2},
        {"answer": "Christmas lights", "points": 1}
      ]
    }
  ]
}
```

### Office/Corporate Questions (`office_questions.json`)
```json
{
  "questions": [
    {
      "question": "Name something annoying about meetings",
      "answers": [
        {"answer": "Too long", "points": 30},
        {"answer": "Could've been an email", "points": 25},
        {"answer": "People arriving late", "points": 15},
        {"answer": "No clear agenda", "points": 10},
        {"answer": "Technical difficulties", "points": 8},
        {"answer": "Side conversations", "points": 7},
        {"answer": "No decisions made", "points": 3},
        {"answer": "Bad coffee", "points": 2}
      ]
    }
  ]
}
```

## Virtual Environment Benefits

Using a virtual environment is recommended because it:
- **Isolates dependencies** - Keeps this project's packages separate from your system Python
- **Prevents conflicts** - Avoids version conflicts with other Python projects
- **Makes deployment easier** - Ensures consistent package versions
- **Keeps your system clean** - Doesn't install packages globally

## Customization

### Styling
Modify the CSS in `templates/base.html` to change colors, fonts, and layout.

### Game Rules
Adjust strike limits, scoring, or add new features in `app.py`.

### Questions
Use JSON import for easy question management or add directly to the database.

## Technical Details

- **Backend**: Flask 3.3 (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Session Management**: Flask sessions for game state
- **AJAX**: For real-time game updates without page refreshes
- **JSON Import**: Command-line argument support for custom questions
- **Host-Controlled**: Presentation-style interface for live game hosting

## Troubleshooting

**Game won't start**: Make sure your virtual environment is activated and Flask is installed.

**Database errors**: Delete `feet_feud.db` file and restart the app to recreate the database.

**JSON import fails**: Check that your JSON file is valid (use a JSON validator) and follows the correct format.

**Port conflicts**: If port 5000 is in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=8000)  # Use different port
```

**Virtual environment issues**: Make sure you see `(venv)` in your terminal prompt before running commands.

**Questions not loading**: Ensure JSON file path is correct and file is readable.

## Future Enhancements

Some ideas for extending the game:

- Add sound effects and animations for reveals
- Implement multiple rounds with different point multipliers
- Add a tournament mode for multiple games
- Create an admin panel for managing questions during gameplay
- Add player statistics and leaderboards
- Support for more than 2 teams
- Timer functionality for time-limited rounds
- Export game results and statistics
- Web-based question editor interface
- Support for image-based questions
- Integration with external APIs for dynamic questions

## License

This project is open source and available under the MIT License.