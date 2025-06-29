
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
To run your FastAPI app with Docker, follow these steps:

---

### 1. Build and start the container

In the directory containing your `Dockerfile` and `docker-compose.yml`, run:

```bash
docker-compose up --build
```

This command will:

* Build the Docker image from your Dockerfile
* Start a container for your FastAPI app
* Map port 8000 on your local machine to port 8000 in the container

---

### 2. Access the app

Once the container is running, you can open your browser and go to:

```
http://localhost:8000
```

To view the interactive API documentation provided by FastAPI, go to:

```
http://localhost:8000/docs
```

---

### 3. Stop the container

To stop and remove the running container, press `Ctrl+C` and then run:

```bash
docker-compose down
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

## Demo
[demo/demo.mp4](demo/demo.mp4)
---

