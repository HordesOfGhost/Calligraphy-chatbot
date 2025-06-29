
# Calligraphy Chatbot API

This is a FastAPI-based application that provides a chatbot interface over a knowledge base of calligraphy-related content. It includes web scraping, semantic search, chatbot integration, authentication, and a simple frontend. Docker support is included for easy deployment.

---

## Features

* Gemini-powered conversational chatbot
* Semantic search using FAISS and HuggingFace MiniLM embeddings
* Web scraping
* Firebase Authentication for secure API access

---

## Getting Started

### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/calligraphy-chatbot.git
   cd calligraphy-chatbot
   ```

2. Create a virtual environment (optional):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   uvicorn app.main:app --reload
   ```

Visit the chat at: [http://localhost:8000](http://localhost:8000)

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3'

services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

### Build and Run with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

| Method | Path        | Description                   |
| ------ | ----------- | ----------------------------- |
| GET    | `/`         | Redirects to login page       |
| GET    | `/login`    | Displays login HTML page      |
| GET    | `/register` | Displays register HTML page   |
| GET    | `/chat`     | Displays chat HTML interface  |
| POST   | `/chat`     | Handles chat input with token |

---

## Scraping and Embedding

* Scrapes content from a base calligraphy website
* Cleans and converts HTML to plain markdown-safe text
* Stores cached content in `knowledge_base/calligraphy_content.json`
* Embeds content using `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace Inference API
* Semantic search is handled using FAISS

---

## Authentication

Firebase ID token verification is used to secure the `/chat` endpoint.

1. Setup Firebase in your project.
2. Download the service account JSON.
3. Use it inside the authentication module for verification.
4. Send the ID token in the `Authorization` header when posting messages.

---

