from flask import Flask, render_template, request, jsonify, session
import os
from game import generate_question, grade_morality

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    # Reset session when starting new game
    session.clear()
    session['current_level'] = 1
    session['previous_answers'] = {}
    return render_template('index.html')

@app.route('/get_question')
def get_question():
    current_level = session.get('current_level', 1)
    previous_answers = session.get('previous_answers', {})
    
    question, choices = generate_question(previous_answers, current_level)
    return jsonify({
        'question': question,
        'choices': choices,
        'level': current_level
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer = data.get('answer')
    question = data.get('question')
    
    score, explanation = grade_morality(question, answer)
    
    # Store the answer
    previous_answers = session.get('previous_answers', {})
    previous_answers[f"question{session['current_level']}"] = answer
    session['previous_answers'] = previous_answers
    
    if score <= 5:
        session.clear()
        return jsonify({
            'success': False,
            'score': score,
            'explanation': explanation,
            'message': "Game Over! You didn't meet the moral threshold to advance."
        })
    else:
        session['current_level'] += 1
        if session['current_level'] > 5:
            session.clear()
            return jsonify({
                'success': True,
                'score': score,
                'explanation': explanation,
                'message': "🌟 Congratulations! You've completed all levels and demonstrated exceptional wisdom in DeepZen!"
            })
        return jsonify({
            'success': True,
            'score': score,
            'explanation': explanation,
            'message': f"🎉 Congratulations! You've advanced to Level {session['current_level']}!"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 