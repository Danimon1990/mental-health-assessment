# Mental Health Self-Assessment Form

A web-based self-assessment tool for mental health conditions, built with FastAPI and Firebase.

## Features

- Interactive self-assessment form for various mental health conditions
- Real-time assessment results
- Secure data storage using Firebase
- RESTful API built with FastAPI

## Prerequisites

- Python 3.8+
- Firebase account and project
- Firebase service account key

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Firebase:
   - Create a Firebase project
   - Generate a service account key
   - Place the service account key file as `serviceAccountKey.json` in the project root

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. Open the HTML form in your browser:
   - The form is available at `http://localhost:8000`
   - The API documentation is available at `http://localhost:8000/docs`

## Project Structure

```
.
├── main.py              # FastAPI server implementation
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── serviceAccountKey.json  # Firebase credentials (not in repo)
```

## API Endpoints

- `GET /`: Welcome message
- `POST /submit-form`: Submit assessment form data

## Security Notes

- The service account key should never be committed to the repository
- Always use HTTPS in production
- Consider implementing rate limiting for the API

## License

[Your chosen license]

## Contributing

[Your contribution guidelines] 