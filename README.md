# Family Feud Web Game

A web-based implementation of the classic Family Feud game show using Flask and SQLite.

## Features

- **Two-team gameplay** with customizable team names
- **Real-time scoring** system
- **Strike mechanics** - 3 strikes and the other team can steal
- **Random question selection** from database
- **Steal opportunities** following classic Family Feud rules
- **Responsive design** that works on desktop and mobile
- **Sample questions** included to get started immediately

## Game Rules

1. Two teams take turns guessing answers to survey questions
2. Each correct answer earns points based on how many people gave that response
3. Teams can keep guessing until they get 3 wrong answers (strikes)
4. After 3 strikes, the opposing team gets one chance to "steal" all accumulated points
5. The team with the most points wins!

## Installation

1. **Clone or download** the project files
2. **Install Python 3.7+** if not already installed
3. **Install Flask**:
   ```bash
   pip install Flask==3.1.1
   ```
4. **Create the project structure**:
   ```
   family-feud/
   ├── app.py
   ├── requirements.txt
   ├── README.md
   └── templates/
       ├── base.html
       ├── index.html
       ├── new_game.html
       └── game.html
   ```

## Running the Game

1. **Navigate to the project directory**:
   ```bash
   cd family-feud
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

3. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

4. **Start playing!** Click "Start New Game" and enter your team names.

## File Structure

- `app.py` - Main Flask application with all game logic
- `templates/base.html` - Base HTML template with styling
- `templates/index.html` - Home page
- `templates/new_game.html` - Team setup page
- `templates/game.html` - Main game interface
- `family_feud.db` - SQLite database (created automatically)

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
conn = sqlite3.connect('family_feud.db')
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

**Database errors**: Delete `family_feud.db` file and restart the app to recreate the database.

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