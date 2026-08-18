AI Document Q&A

An AI-powered document question-answering application that lets users upload a PDF and ask questions about its contents.

Live Demo

Frontend: https://ai-document-qa-gcp.vercel.app/

Backend: https://ai-document-qa-backend-104102848745.asia-south1.run.app

Features

Upload PDF documents

Extract and store document content

Split documents into searchable chunks

Generate semantic embeddings with Gemini

Store documents and embeddings in Google Cloud Firestore

Store uploaded PDFs in Google Cloud Storage

Retrieve relevant document chunks for a question

Generate answers using Gemini

Show relevant sources and similarity scores

Responsive, modern React UI

Cloud deployment using Vercel and Google Cloud Run

Architecture

User
  |
  v
React + Vite (Vercel)
  |
  | HTTPS API requests
  v
FastAPI (Google Cloud Run)
  |
  +--> Google Cloud Storage
  |       |
  |       +--> Uploaded PDFs
  |
  +--> Firestore
  |       |
  |       +--> Documents
  |       +--> Chunks
  |       +--> Embeddings
  |
  +--> Gemini
          |
          +--> Text embeddings
          +--> AI-generated answers

Tech Stack

Frontend

React

Vite

JavaScript

CSS

Backend

Python

FastAPI

Uvicorn

Google Cloud

Cloud Run

Cloud Storage

Firestore

Artifact Registry

Vertex AI / Gemini

AI / RAG

Gemini Embeddings

Semantic search

Retrieval-Augmented Generation (RAG)

How It Works

The user selects a PDF.

The frontend sends the PDF to the FastAPI backend.

The backend uploads the PDF to Google Cloud Storage.

Text is extracted from the document.

The text is divided into chunks.

Gemini creates embeddings for the chunks.

Document data, chunks, and embeddings are stored in Firestore.

The user asks a question.

The backend finds the most relevant chunks using semantic similarity.

Gemini uses the relevant context to generate the answer.

The frontend displays the answer and source chunks.

Local Development

Backend

cd backend

Create/activate your Python virtual environment and install dependencies:

pip install -r requirements.txt

Run FastAPI:

uvicorn app.main:app --reload --port 8000

Frontend

cd frontend
npm.cmd install
npm.cmd run dev

The local frontend normally runs on:

http://localhost:5173

Deployment

Backend

The backend is containerized with Docker and pushed to Google Artifact Registry before deployment to Cloud Run.

Example:

docker build -t asia-south1-docker.pkg.dev/PROJECT_ID/ai-document-qa/ai-document-qa-backend:latest .
docker push asia-south1-docker.pkg.dev/PROJECT_ID/ai-document-qa/ai-document-qa-backend:latest

gcloud run deploy ai-document-qa-backend `
  --image=asia-south1-docker.pkg.dev/PROJECT_ID/ai-document-qa/ai-document-qa-backend:latest `
  --region=asia-south1 `
  --platform=managed `
  --port=8080 `
  --allow-unauthenticated

Frontend

The frontend is deployed through Vercel using the GitHub repository.

Environment Variables

Backend configuration uses environment variables such as:

PROJECT_ID
GOOGLE_CLOUD_PROJECT
BUCKET_NAME
LOCATION

Do not commit API keys, service-account JSON files, .env files containing secrets, or other credentials.

Project Structure

ai-document-qa-gcp/
|
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── config.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
|
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── ...
|
└── README.md

Security Notes

Credentials are provided through Google Cloud authentication and environment configuration.

Secrets should never be hard-coded in frontend source code.

Cloud Run uses a Google service account to access Google Cloud services.

CORS should allow only the deployed frontend domain and required local development origins.

Future Improvements

User authentication

Multiple document management

PDF page-level citations

Conversation history

Streaming AI responses

Better vector search at larger scale

Document deletion and management

Usage monitoring and rate limiting

Author

Raj Bhilare

Built as a cloud-based AI/RAG project using React, FastAPI, Google Cloud and Gemini.