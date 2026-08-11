# Observasi Karakter API

A deterministic REST API engine using **FastAPI** and **Pydantic V2** to process talent assessments. This backend bridges raw HTTP requests with strongly-typed Python business logic, ensuring mathematical accuracy for talent scores and generating standard OpenAPI endpoints for Web AI consumption.

## Features
- **FastAPI & Pydantic V2**: Leveraging strict type validation and coercion.
- **Deterministic Scoring Logic**: Calculates exactly 40 talent scores without LLM arithmetic variance.
- **Web AI Ready**: Exposes API endpoints designed seamlessly for integration with custom chatbots (ChatGPT, Gemini, Claude).

## Requirements
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

## Setup and Installation

1. **Navigate to the project directory:**
   ```bash
   cd observasi-karakter-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi "uvicorn[standard]" pydantic
   ```
   *(If you later add a `requirements.txt`, you can install them via `pip install -r requirements.txt`)*

## Running the Development Server

Start the development server with live reload enabled using `uvicorn`:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once your server is running, you can test your endpoints directly from your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
