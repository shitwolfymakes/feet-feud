from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Ensure static folder structure exists
os.makedirs('static/assets', exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('feet_feud.db')
    cursor = conn.cursor()
    
    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create answers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            answer TEXT NOT NULL,
            points INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')
    
    # Create games table to track game sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1_name TEXT NOT NULL,
            team2_name TEXT NOT NULL,
            team1_score INTEGER DEFAULT 0,
            team2_score INTEGER DEFAULT 0,
            current_question_id INTEGER,
            current_team INTEGER DEFAULT 1,
            strikes INTEGER DEFAULT 0,
            round_points INTEGER DEFAULT 0,
            round_frozen INTEGER DEFAULT 0,
            game_status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (current_question_id) REFERENCES questions (id)
        )
    ''')
    
    # Create revealed_answers table to track which answers have been revealed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revealed_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            answer_id INTEGER,
            revealed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id),
            FOREIGN KEY (answer_id) REFERENCES answers (id),
            UNIQUE(game_id, answer_id)
        )
    ''')
    
    # Add round_frozen column to existing games if it doesn't exist
    cursor.execute('''
        PRAGMA table_info(games)
    ''')
    columns = [column[1] for column in cursor.fetchall()]
    if 'round_frozen' not in columns:
        cursor.execute('''
            ALTER TABLE games ADD COLUMN round_frozen INTEGER DEFAULT 0
        ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('feet_feud.db')
    conn.row_factory = sqlite3.Row
    return conn

def seed_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if we already have sample data
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Sample questions and answers
    sample_data = [
        {
            'question': 'Name something you find in a kitchen',
            'answers': [
                ('Refrigerator', 25),
                ('Stove/Oven', 20),
                ('Sink', 15),
                ('Microwave', 12),
                ('Dishwasher', 10),
                ('Cabinets', 8),
                ('Table', 6),
                ('Toaster', 4)
            ]
        },
        {
            'question': 'Name a popular pet',
            'answers': [
                ('Dog', 45),
                ('Cat', 35),
                ('Fish', 8),
                ('Bird', 5),
                ('Hamster', 3),
                ('Rabbit', 2),
                ('Turtle', 1),
                ('Snake', 1)
            ]
        },
        {
            'question': 'Name something people do at the beach',
            'answers': [
                ('Swimming', 30),
                ('Sunbathing', 25),
                ('Building sandcastles', 15),
                ('Playing volleyball', 10),
                ('Surfing', 8),
                ('Reading', 6),
                ('Walking', 4),
                ('Collecting shells', 2)
            ]
        },
        {
            'question': 'Name a common pizza topping',
            'answers': [
                ('Pepperoni', 35),
                ('Cheese', 25),
                ('Sausage', 15),
                ('Mushrooms', 10),
                ('Peppers', 6),
                ('Onions', 5),
                ('Olives', 3),
                ('Pineapple', 1)
            ]
        },
        {
            'question': 'Name something you do before going to bed',
            'answers': [
                ('Brush teeth', 40),
                ('Change into pajamas', 20),
                ('Watch TV', 12),
                ('Read', 10),
                ('Set alarm', 8),
                ('Shower', 5),
                ('Pray', 3),
                ('Check phone', 2)
            ]
        },
        {
            'question': 'Name a popular breakfast food',
            'answers': [
                ('Eggs', 30),
                ('Cereal', 25),
                ('Toast', 15),
                ('Bacon', 12),
                ('Pancakes', 8),
                ('Coffee', 5),
                ('Oatmeal', 3),
                ('Fruit', 2)
            ]
        },
        {
            'question': 'Name something you might find in a garage',
            'answers': [
                ('Car', 35),
                ('Tools', 25),
                ('Lawn mower', 15),
                ('Bicycle', 10),
                ('Storage boxes', 7),
                ('Workbench', 5),
                ('Paint', 2),
                ('Ladder', 1)
            ]
        },
        {
            'question': 'Name a reason people call in sick to work',
            'answers': [
                ('Flu/Cold', 35),
                ('Stomach bug', 20),
                ('Headache', 15),
                ('Doctor appointment', 10),
                ('Fever', 8),
                ('Back pain', 7),
                ('Family emergency', 3),
                ('Food poisoning', 2)
            ]
        }
    ]
    
    for data in sample_data:
        cursor.execute('INSERT INTO questions (question) VALUES (?)', (data['question'],))
        question_id = cursor.lastrowid
        
        for answer, points in data['answers']:
            cursor.execute('INSERT INTO answers (question_id, answer, points) VALUES (?, ?, ?)',
                         (question_id, answer, points))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        try:
            # Hardcoded team names
            team1_name = 'Left Foot'
            team2_name = 'Right Foot'
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get the first question (ordered by ID)
            cursor.execute('SELECT id FROM questions ORDER BY id ASC LIMIT 1')
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return render_template('new_game.html', error='No questions available'), 500
            
            question_id = result[0]
            
            # Create new game
            cursor.execute('''
                INSERT INTO games (team1_name, team2_name, current_question_id)
                VALUES (?, ?, ?)
            ''', (team1_name, team2_name, question_id))
            
            game_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            session['game_id'] = game_id
            return redirect(url_for('game'))
            
        except Exception as e:
            print(f"Error creating new game: {e}")
            return render_template('new_game.html', error='Error creating game'), 500
    
    return render_template('new_game.html')

@app.route('/game')
def game():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    try:
        conn = get_db_connection()
        game_row = conn.execute('''
            SELECT g.*, q.question 
            FROM games g 
            JOIN questions q ON g.current_question_id = q.id 
            WHERE g.id = ?
        ''', (session['game_id'],)).fetchone()
        
        if not game_row:
            conn.close()
            return redirect(url_for('index'))
        
        # Convert Row to dict for JSON serialization
        game = dict(game_row)
        
        # Get answers for current question
        answers_rows = conn.execute('''
            SELECT * FROM answers 
            WHERE question_id = ? 
            ORDER BY points DESC
        ''', (game['current_question_id'],)).fetchall()
        
        # Convert Row objects to dicts
        answers = [dict(row) for row in answers_rows]
        
        conn.close()
        
        return render_template('game.html', game=game, answers=answers)
        
    except Exception as e:
        print(f"Error loading game: {e}")
        return redirect(url_for('index'))

@app.route('/game_data_json')
def game_data_json():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        conn = get_db_connection()
        game_row = conn.execute('''
            SELECT g.*, q.question 
            FROM games g 
            JOIN questions q ON g.current_question_id = q.id 
            WHERE g.id = ?
        ''', (session['game_id'],)).fetchone()
        
        if not game_row:
            conn.close()
            return jsonify({'error': 'Game not found'}), 404
        
        answers_rows = conn.execute('''
            SELECT * FROM answers 
            WHERE question_id = ? 
            ORDER BY points DESC
        ''', (game_row['current_question_id'],)).fetchall()
        
        # Get revealed answers for this game and question
        revealed_rows = conn.execute('''
            SELECT ra.answer_id 
            FROM revealed_answers ra
            JOIN answers a ON ra.answer_id = a.id
            WHERE ra.game_id = ? AND a.question_id = ?
        ''', (session['game_id'], game_row['current_question_id'])).fetchall()
        
        revealed_answer_ids = [row['answer_id'] for row in revealed_rows]
        
        # Get question position
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM questions WHERE id <= ?
        ''', (game_row['current_question_id'],))
        current_question_number = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM questions')
        total_questions = cursor.fetchone()[0]
        
        conn.close()
        
        # Convert game row to dict and ensure round_frozen is included
        game_dict = dict(game_row)
        if 'round_frozen' not in game_dict:
            game_dict['round_frozen'] = 0
        
        # Check if question has been revealed
        question_revealed = session.get(f'question_revealed_{session["game_id"]}', False)
        
        return jsonify({
            'game': game_dict,
            'answers': [dict(row) for row in answers_rows],
            'revealed_answer_ids': revealed_answer_ids,
            'question_number': current_question_number,
            'total_questions': total_questions,
            'question_revealed': question_revealed
        })
        
    except Exception as e:
        print(f"Error getting game data: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/add_strike', methods=['POST'])
def add_strike():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        conn = get_db_connection()
        game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()
        
        if not game:
            conn.close()
            return jsonify({'error': 'Game not found'}), 404
        
        new_strikes = game['strikes'] + 1
        conn.execute('UPDATE games SET strikes = ? WHERE id = ?', 
                    (new_strikes, session['game_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'strikes': new_strikes, 'success': True})
        
    except Exception as e:
        print(f"Error adding strike: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/switch_team', methods=['POST'])
def switch_team():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        conn = get_db_connection()
        game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()
        
        if not game:
            conn.close()
            return jsonify({'error': 'Game not found'}), 404
        
        # Award current round points to current team
        if game['round_points'] > 0:
            if game['current_team'] == 1:
                new_team1_score = game['team1_score'] + game['round_points']
                conn.execute('UPDATE games SET team1_score = ? WHERE id = ?', 
                            (new_team1_score, session['game_id']))
            else:
                new_team2_score = game['team2_score'] + game['round_points']
                conn.execute('UPDATE games SET team2_score = ? WHERE id = ?', 
                            (new_team2_score, session['game_id']))
        
        # Switch teams and reset round
        new_team = 2 if game['current_team'] == 1 else 1
        conn.execute('''
            UPDATE games SET 
            current_team = ?, 
            strikes = 0, 
            round_points = 0 
            WHERE id = ?
        ''', (new_team, session['game_id']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'new_team': new_team})
        
    except Exception as e:
        print(f"Error switching team: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/award_steal', methods=['POST'])
def award_steal():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        stealing_team = data.get('stealing_team')
        points = data.get('points', 0)
        
        if stealing_team not in [1, 2]:
            return jsonify({'error': 'Invalid team'}), 400
        
        conn = get_db_connection()
        
        if stealing_team == 1:
            conn.execute('''
                UPDATE games SET 
                team1_score = team1_score + ?, 
                strikes = 0, 
                round_points = 0 
                WHERE id = ?
            ''', (points, session['game_id']))
        else:
            conn.execute('''
                UPDATE games SET 
                team2_score = team2_score + ?, 
                strikes = 0, 
                round_points = 0 
                WHERE id = ?
            ''', (points, session['game_id']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error awarding steal: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/award_points', methods=['POST'])
def award_points():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        team = data.get('team')
        points = data.get('points', 0)
        
        if team not in [1, 2]:
            return jsonify({'error': 'Invalid team'}), 400
        
        conn = get_db_connection()
        
        if team == 1:
            conn.execute('UPDATE games SET team1_score = team1_score + ? WHERE id = ?', 
                        (points, session['game_id']))
        else:
            conn.execute('UPDATE games SET team2_score = team2_score + ? WHERE id = ?', 
                        (points, session['game_id']))
        
        # Set round points to 0 and freeze the round after awarding
        conn.execute('UPDATE games SET round_points = 0, round_frozen = 1 WHERE id = ?', 
                    (session['game_id'],))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error awarding points: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/update_round_points', methods=['POST'])
def update_round_points():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        points = data.get('points', 0)
        
        conn = get_db_connection()
        conn.execute('UPDATE games SET round_points = ? WHERE id = ?', 
                    (points, session['game_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error updating round points: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reset_round', methods=['POST'])
def reset_round():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        conn = get_db_connection()
        
        # Get current question
        game = conn.execute('SELECT current_question_id FROM games WHERE id = ?', 
                           (session['game_id'],)).fetchone()
        
        if game:
            # Clear revealed answers for this question
            conn.execute('''
                DELETE FROM revealed_answers 
                WHERE game_id = ? AND answer_id IN (
                    SELECT id FROM answers WHERE question_id = ?
                )
            ''', (session['game_id'], game['current_question_id']))
        
        # Reset game state
        conn.execute('''
            UPDATE games SET 
            strikes = 0, 
            round_points = 0,
            round_frozen = 0
            WHERE id = ?
        ''', (session['game_id'],))
        
        # Clear question reveal state
        session.pop(f'question_revealed_{session["game_id"]}', None)
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error resetting round: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_answer/<int:answer_id>')
def get_answer(answer_id):
    try:
        conn = get_db_connection()
        answer = conn.execute('SELECT * FROM answers WHERE id = ?', (answer_id,)).fetchone()
        conn.close()
        
        if answer:
            return jsonify({
                'success': True,
                'answer': answer['answer'],
                'points': answer['points']
            })
        else:
            return jsonify({'success': False, 'error': 'Answer not found'}), 404
            
    except Exception as e:
        print(f"Error getting answer: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/next_round', methods=['POST'])
def next_round():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        conn = get_db_connection()
        
        # Get current game state
        game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()
        if not game:
            conn.close()
            return jsonify({'error': 'Game not found'}), 404
        
        # Don't award any points - just move to next round
        
        # Get the next question in sequence (ordered by ID)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM questions 
            WHERE id > ? 
            ORDER BY id ASC 
            LIMIT 1
        ''', (game['current_question_id'],))
        
        result = cursor.fetchone()
        if not result:
            # No more questions - could loop back to first or end game
            cursor.execute('SELECT id FROM questions ORDER BY id ASC LIMIT 1')
            result = cursor.fetchone()
            if not result:
                conn.close()
                return jsonify({'error': 'No more questions available'}), 404
            
        new_question_id = result[0]
        
        # Reset for next round
        conn.execute('''
            UPDATE games SET 
            current_question_id = ?, 
            current_team = 1, 
            strikes = 0, 
            round_points = 0,
            round_frozen = 0
            WHERE id = ?
        ''', (new_question_id, session['game_id']))
        
        # Clear question reveal state for new round
        session.pop(f'question_revealed_{session["game_id"]}', None)
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error starting next round: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reveal_question_state', methods=['POST'])
def reveal_question_state():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        # Store in session that question has been revealed for this round
        session[f'question_revealed_{session["game_id"]}'] = True
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error setting question reveal state: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reveal_answer', methods=['POST'])
def reveal_answer():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        answer_id = data.get('answer_id')
        
        if not answer_id:
            return jsonify({'error': 'No answer_id provided'}), 400
        
        conn = get_db_connection()
        
        # Record that this answer has been revealed
        try:
            conn.execute('''
                INSERT INTO revealed_answers (game_id, answer_id)
                VALUES (?, ?)
            ''', (session['game_id'], answer_id))
            conn.commit()
        except sqlite3.IntegrityError:
            # Answer already revealed, that's okay
            pass
        
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error recording revealed answer: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/questions')
def view_questions():
    conn = get_db_connection()
    questions = conn.execute('''
        SELECT q.id, q.question, COUNT(a.id) as answer_count
        FROM questions q
        LEFT JOIN answers a ON q.id = a.question_id
        GROUP BY q.id
        ORDER BY q.id ASC
    ''').fetchall()
    conn.close()
    
    return render_template('questions.html', questions=questions)

@app.route('/final_scores')
def final_scores():
    if 'game_id' not in session:
        return redirect(url_for('index'))
    
    try:
        conn = get_db_connection()
        game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()
        
        if not game:
            conn.close()
            return redirect(url_for('index'))
        
        # Determine winner
        winner = None
        if game['team1_score'] > game['team2_score']:
            winner = game['team1_name']
            winner_score = game['team1_score']
            loser = game['team2_name']
            loser_score = game['team2_score']
        elif game['team2_score'] > game['team1_score']:
            winner = game['team2_name']
            winner_score = game['team2_score']
            loser = game['team1_name']
            loser_score = game['team1_score']
        else:
            # It's a tie
            winner = 'TIE'
            winner_score = game['team1_score']
            loser_score = game['team2_score']
        
        # Mark game as completed
        conn.execute('UPDATE games SET game_status = ? WHERE id = ?', 
                    ('completed', session['game_id']))
        conn.commit()
        conn.close()
        
        return render_template('final_scores.html', 
                             team1_name=game['team1_name'],
                             team2_name=game['team2_name'],
                             team1_score=game['team1_score'],
                             team2_score=game['team2_score'],
                             winner=winner,
                             winner_score=winner_score,
                             loser=loser if winner != 'TIE' else None,
                             loser_score=loser_score)
        
    except Exception as e:
        print(f"Error showing final scores: {e}")
        return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/') or request.path in ['/game_data_json', '/add_strike', '/switch_team', '/award_steal', '/award_points', '/reset_round', '/next_round']:
        return jsonify({'error': 'Not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/') or request.path in ['/game_data_json', '/add_strike', '/switch_team', '/award_steal', '/award_points', '/reset_round', '/next_round']:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    seed_sample_data()
    app.run(debug=True)