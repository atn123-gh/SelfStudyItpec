# SelfStudy ITPEC

SelfStudy ITPEC is a web application for practicing ITPEC IP (Information
Technology Passport) and FE (Fundamental Engineer) exam questions.

The application provides past exam questions, answer checking, and
AI-generated explanations to support self-study.

**Live demo:** https://168.144.218.68 (real, publicly trusted HTTPS
certificate — no domain name needed)

### Main Features

- ITPEC IP / FE exam question practice
- Answer checking and solution display
- Quiz data stored with PostgreSQL and MongoDB
- AI-generated explanations for select questions, using a retrieval-augmented
  generation (RAG) workflow grounded in reference textbook content
- Docker Compose setup for local development and deployment, including a
  no-domain HTTPS deployment option

### RAG Explanation

A small RAG workflow generates explanations for exam questions:

```text
Exam question
    ↓
Retrieve relevant textbook content
    ↓
Send the question and retrieved context to an LLM
    ↓
Generate an explanation
    ↓
Store the explanation in MongoDB
    ↓
Display it on the quiz page
```

Explanations are generated ahead of time by an offline utility script and
stored in the database, rather than being generated on every page load - the
website itself never calls an LLM at request time.

### Technologies

- Python / Django
- PostgreSQL
- MongoDB
- RAG / LLM (Google Gemini)
- Docker Compose
- Nginx

### Getting Started

See [DEVELOPMENT.md](DEVELOPMENT.md) for how to run this project locally or
deploy it yourself.
