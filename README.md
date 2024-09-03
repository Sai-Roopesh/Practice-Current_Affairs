# Current Affairs Quiz

This project is a web application that provides users with current affairs information and generates quizzes based on recent news articles. It uses Flask for the backend, HTMX for dynamic frontend interactions, and integrates with external APIs for news data and quiz generation.

## Features

- Fetch and display current affairs articles
- Generate quizzes based on recent news
- Interactive quiz-taking experience
- Score tracking and result display

## Technologies Used

- Python 3.x
- Flask
- HTMX
- OpenAI API
- GNews API

## Project Structure

```
.
├── app.py
├── templates
│   └── index.html
├── .env
├── requirements.txt
└── README.md
```

- `app.py`: Main Flask application file containing all routes and logic
- `templates/index.html`: HTML template for the main page
- `.env`: Environment variables file (not included in repository)
- `requirements.txt`: List of Python dependencies
- `README.md`: This file

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd current-affairs-quiz
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   NEWS_API_KEY=your_gnews_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://localhost:8080` to use the application.

## Usage

1. **View Current Affairs**: Click the "View Current Affairs" button to fetch and display recent news articles.

2. **Take Quiz**: Click the "Take Quiz" button to generate a quiz based on recent news. Answer the questions and submit to see your results.

## API Integration

- **GNews API**: Used to fetch recent news articles. You'll need to sign up for an API key at [https://gnews.io/](https://gnews.io/).
- **OpenAI API**: Used to generate quiz questions based on the news articles. Sign up for an API key at [https://openai.com/](https://openai.com/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
