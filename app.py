from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
from openai import OpenAI
import os
import random


class Question(BaseModel):
    question: str
    options: list[str]
    answer: str


class Quiz(BaseModel):
    questions: list[Question]


# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


app = Flask(__name__)
app.secret_key = os.urandom(24)
# Home route


@app.route('/')
def hello_world():
    return render_template('index.html')

# Current affairs route


@app.route('/current', methods=['GET'])
def current_affairs():
    url = f"https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Extract articles from the JSON data
    articles = data.get('articles', [])

    # Create HTML content for the articles
    if articles:
        html_content = "<ul>"
        for article in articles:
            html_content += f"""
                <li>
                    <h3>{article['title']}</h3>
                    <p>{article['description']}</p>
                    <p>{article['content']}</p>
                    <p><strong>Published At:</strong> {article['publishedAt']}</p>
                    <a href="{article['url']}" target="_blank">Read more</a>
                    <br><img src="{article['image']}" alt="{article['title']}" style="max-width: 300px;">
                </li>
            """
        html_content += "</ul>"
    else:
        html_content = "<p>No current affairs data found.</p>"

    return html_content

# Quiz generation route


@app.route('/quiz', methods=['GET'])
def quiz():
    try:
        url = f"https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={NEWS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        client = OpenAI()
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": f"Generate a quiz with 5 questions based on the following news article data: {data}. Return the quiz as a JSON object with a 'questions' key containing an array of question objects. Each question object should have 'question', 'options', and 'answer' fields."},
                {"role": "user", "content": "Generate a quiz with 5 questions based on the news article data."},
            ],
            response_format=Quiz,
        )

        quiz_data = completion.choices[0].message.parsed
        session['quiz'] = quiz_data.dict()
        session['current_question'] = 0
        session['score'] = 0

        return render_next_question()

    except Exception as e:
        print("Error:", str(e))
        return f"<p>Error: {str(e)}</p>"


def render_next_question():
    quiz = session.get('quiz')
    current_question = session.get('current_question', 0)

    if current_question >= len(quiz['questions']):
        return render_quiz_end()

    question = quiz['questions'][current_question]
    options_html = ''.join(
        [f'<input type="radio" name="answer" value="{option}">{option}<br>' for option in question['options']])

    return f"""
    <form hx-post="/check-answer" hx-target="#quiz">
        <h2>Question {current_question + 1}</h2>
        <p>{question['question']}</p>
        {options_html}
        <input type="submit" value="Submit">
    </form>
    """


def render_quiz_end():
    score = session.get('score', 0)
    total_questions = len(session.get('quiz', {}).get('questions', []))
    return f"""
    <h2>Quiz Completed!</h2>
    <p>Your final score: {score} out of {total_questions}</p>
    <button hx-get="/quiz" hx-target="#quiz">Take Another Quiz</button>
    """


@app.route('/check-answer', methods=['POST'])
def check_answer():
    user_answer = request.form.get('answer')
    quiz = session.get('quiz')
    current_question = session.get('current_question', 0)

    correct_answer = quiz['questions'][current_question]['answer']

    if user_answer == correct_answer:
        session['score'] = session.get('score', 0) + 1
        result = "<h3>Correct! Well done!</h3>"
    else:
        result = f"<h3>Sorry, that's incorrect. The correct answer is: {correct_answer}</h3>"

    session['current_question'] = current_question + 1

    return f"""
    {result}
    <hr>
    {render_next_question()}
    """


# Main function
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
