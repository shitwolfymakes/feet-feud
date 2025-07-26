# Feet Feud Web Game

A web-based implementation of the classic Family Feud game show using Flask and SQLite. Perfect for hosting live game show events with a presentation-style interface.

## Features

- **Presentation-style gameplay** - Host controls with click-to-reveal answers
- **Two-team scoring** with customizable team names
- **Real-time host controls** - Add strikes, switch teams, award steals
- **Classic Family Feud mechanics** - 3 strikes and steal opportunities
- **Random question selection** from database
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
└── templates/
    ├── base.html
    ├── index.html
    ├── new_game.html
    └── game.html
```

### 4. Run the Application

```bash
# Make sure you're in the project directory with virtual environment activated
python app.py
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

## Hosting a Game

### Pre-Game Setup
1. **Connect to projector/TV** for audience viewing
2. **Start the application** and navigate to the game URL
3. **Create new game** with team names
4. **Explain rules** to participants

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

## Database Schema

The game uses three main tables:

- **questions** - Stores survey questions
- **answers** - Stores possible answers with point values
- **games** - Tracks active game sessions with scores and state

## Adding Custom Questions

You can add your own questions by inserting data into the database:

```python
# Connect to database
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
The game comes with sample questions, but you can add as many as you want using the database structure above.

## Technical Details

- **Backend**: Flask 3.3 (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Session Management**: Flask sessions for game state
- **AJAX**: For real-time game updates without page refreshes
- **Host-Controlled**: Presentation-style interface for live game hosting

## Troubleshooting

**Game won't start**: Make sure your virtual environment is activated and Flask is installed.

**Database errors**: Delete `feet_feud.db` file and restart the app to recreate the database.

**Port conflicts**: If port 5000 is in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=8000)  # Use different port
```

**Virtual environment issues**: Make sure you see `(venv)` in your terminal prompt before running commands.

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

## License

This project is open source and available under the MIT License.

## File Structure

- `app.py` - Main Flask application with all game logic
- `templates/base.html` - Base HTML template with styling
- `templates/index.html` - Home page
- `templates/new_game.html` - Team setup page
- `templates/game.html` - Main game interface
- `feet_feud.db` - SQLite database (created automatically)

## Database Schema

The game uses three main tables:

- **questions** - Stores survey questions
- **answers** - Stores possible answers with point values
- **games** - Tracks active game sessions with scores and state

## Adding Custom Questions

You can add your own questions by inserting data into the database:

```python
# Connect to database
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

## Customization

### Styling
Modify the CSS in `templates/base.html` to change colors, fonts, and layout.

### Game Rules
Adjust strike limits, scoring, or add new features in `app.py`.

### Questions
The game comes with sample questions, but you can add as many as you want using the database structure above.

## Technical Details

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Session Management**: Flask sessions for game state
- **AJAX**: For real-time game updates without page refreshes

## Troubleshooting

**Game won't start**: Make sure Flask is installed and you're running `python app.py` from the correct directory.

**Database errors**: Delete `feet_feud.db` file and restart the app to recreate the database.

**Port conflicts**: If port 5000 is in use, modify the last line in `app.py`:
```python
app.run(debug=True, port=8000)  # Use different port
```

## Future Enhancements

Some ideas for extending the game:

- Add sound effects and animations
- Implement multiple rounds with different point multipliers
- Add a tournament mode
- Create an admin panel for managing questions
- Add player statistics and leaderboards
- Support for more than 2 teams

## License

This project is open source and available under the MIT License.