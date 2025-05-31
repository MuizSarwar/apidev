# FastAPI Posts API

This is a simple FastAPI project for learning REST API development with Python.  
It provides endpoints to create, read, and update posts.

## Features

- Home page endpoint
- Get all posts
- Get the latest post
- Get a post by ID
- Create a new post
- Update a post

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/apidev.git
   cd apidev
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the app:
   ```
   uvicorn app.main:app --reload
   ```

5. Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the interactive API docs.

## License

This project is for educational purposes.