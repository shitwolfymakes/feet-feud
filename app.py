from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'


# Database initialization
def init_db():
    conn = sqlite3.connect('family_feud.db')
    cursor = conn.cursor()

    # Create questions table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS questions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       question
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')

    # Create answers table
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS answers
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       question_id
                       INTEGER,
                       answer
                       TEXT
                       NOT
                       NULL,
                       points
                       INTEGER
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       question_id
                   ) REFERENCES questions
                   (
                       id
                   )
                       )
                   ''')

    # Create games table to track game sessions
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS games
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       team1_name
                       TEXT
                       NOT
                       NULL,
                       team2_name
                       TEXT
                       NOT
                       NULL,
                       team1_score
                       INTEGER
                       DEFAULT
                       0,
                       team2_score
                       INTEGER
                       DEFAULT
                       0,
                       current_question_id
                       INTEGER,
                       current_team
                       INTEGER
                       DEFAULT
                       1,
                       strikes
                       INTEGER
                       DEFAULT
                       0,
                       round_points
                       INTEGER
                       DEFAULT
                       0,
                       game_status
                       TEXT
                       DEFAULT
                       'active',
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP,
                       FOREIGN
                       KEY
                   (
                       current_question_id
                   ) REFERENCES questions
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('family_feud.db')
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
        team1_name = request.form['team1_name']
        team2_name = request.form['team2_name']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get a random question
        cursor.execute('SELECT id FROM questions ORDER BY RANDOM() LIMIT 1')
        question_id = cursor.fetchone()[0]

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

    return render_template('new_game.html')


@app.route('/game')
def game():
    if 'game_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    game = conn.execute('''
                        SELECT g.*, q.question
                        FROM games g
                                 JOIN questions q ON g.current_question_id = q.id
                        WHERE g.id = ?
                        ''', (session['game_id'],)).fetchone()

    if not game:
        return redirect(url_for('index'))

    # Get answers for current question
    answers = conn.execute('''
                           SELECT *
                           FROM answers
                           WHERE question_id = ?
                           ORDER BY points DESC
                           ''', (game['current_question_id'],)).fetchall()

    conn.close()

    return render_template('game.html', game=game, answers=answers)


@app.route('/guess', methods=['POST'])
def guess():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400

    guess_text = request.json['guess'].strip().lower()

    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()

    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Check if guess matches any answer
    answers = conn.execute('''
                           SELECT *
                           FROM answers
                           WHERE question_id = ?
                           ORDER BY points DESC
                           ''', (game['current_question_id'],)).fetchall()

    matched_answer = None
    for answer in answers:
        if guess_text in answer['answer'].lower() or answer['answer'].lower() in guess_text:
            matched_answer = answer
            break

    if matched_answer:
        # Correct guess - add points to round total
        new_round_points = game['round_points'] + matched_answer['points']
        conn.execute('''
                     UPDATE games
                     SET round_points = ?,
                         strikes      = 0
                     WHERE id = ?
                     ''', (new_round_points, session['game_id']))

        result = {
            'correct': True,
            'answer': matched_answer['answer'],
            'points': matched_answer['points'],
            'round_points': new_round_points
        }
    else:
        # Wrong guess - add strike
        new_strikes = game['strikes'] + 1
        conn.execute('UPDATE games SET strikes = ? WHERE id = ?',
                     (new_strikes, session['game_id']))

        result = {
            'correct': False,
            'strikes': new_strikes
        }

        # If 3 strikes, other team can steal
        if new_strikes >= 3:
            result['steal_opportunity'] = True

    conn.commit()
    conn.close()

    return jsonify(result)


@app.route('/steal', methods=['POST'])
def steal():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400

    steal_guess = request.json['guess'].strip().lower()

    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (session['game_id'],)).fetchone()

    # Check if steal guess is correct
    answers = conn.execute('''
                           SELECT *
                           FROM answers
                           WHERE question_id = ?
                           ORDER BY points DESC
                           ''', (game['current_question_id'],)).fetchall()

    matched_answer = None
    for answer in answers:
        if steal_guess in answer['answer'].lower() or answer['answer'].lower() in steal_guess:
            matched_answer = answer
            break

    if matched_answer:
        # Successful steal - other team gets all round points
        other_team = 2 if game['current_team'] == 1 else 1
        if other_team == 1:
            new_team1_score = game['team1_score'] + game['round_points']
            conn.execute('UPDATE games SET team1_score = ? WHERE id = ?',
                         (new_team1_score, session['game_id']))
        else:
            new_team2_score = game['team2_score'] + game['round_points']
            conn.execute('UPDATE games SET team2_score = ? WHERE id = ?',
                         (new_team2_score, session['game_id']))

        result = {'successful': True, 'points_stolen': game['round_points']}
    else:
        # Failed steal - current team keeps their points
        if game['current_team'] == 1:
            new_team1_score = game['team1_score'] + game['round_points']
            conn.execute('UPDATE games SET team1_score = ? WHERE id = ?',
                         (new_team1_score, session['game_id']))
        else:
            new_team2_score = game['team2_score'] + game['round_points']
            conn.execute('UPDATE games SET team2_score = ? WHERE id = ?',
                         (new_team2_score, session['game_id']))

        result = {'successful': False}

    conn.commit()
    conn.close()

    return jsonify(result)


@app.route('/next_round', methods=['POST'])
def next_round():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400

    conn = get_db_connection()

    # Get a new random question
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM questions ORDER BY RANDOM() LIMIT 1')
    new_question_id = cursor.fetchone()[0]

    # Reset for next round
    conn.execute('''
                 UPDATE games
                 SET current_question_id = ?,
                     current_team        = ?,
                     strikes             = 0,
                     round_points        = 0
                 WHERE id = ?
                 ''', (new_question_id, 1, session['game_id']))

    conn.commit()
    conn.close()

    return jsonify({'success': True})


@app.route('/game_data')
def game_data():
    if 'game_id' not in session:
        return jsonify({'error': 'No active game'}), 400

    conn = get_db_connection()
    game = conn.execute('''
                        SELECT g.*, q.question
                        FROM games g
                                 JOIN questions q ON g.current_question_id = q.id
                        WHERE g.id = ?
                        ''', (session['game_id'],)).fetchone()

    answers = conn.execute('''
                           SELECT *
                           FROM answers
                           WHERE question_id = ?
                           ORDER BY points DESC
                           ''', (game['current_question_id'],)).fetchall()

    conn.close()

    return jsonify({
        'game': dict(game),
        'answers': [dict(answer) for answer in answers]
    })


if __name__ == '__main__':
    init_db()
    seed_sample_data()
    app.run(debug=True)