# AI Smart Inbox Router

An autonomous AI agent designed to automate operational triage for email inboxes.

## 🚀 Overview
This project solves the problem of manual email sorting by deploying a serverless AI agent that:
1.  **Ingests** emails via IMAP (Gmail).
2.  **Analyzes** intent and urgency using OpenAI (GPT-4o).
3.  **Routes** alerts to Slack via Webhooks.
4.  **Runs** autonomously on a schedule using Google Cloud Run Jobs.

## 🛠️ Tech Stack
* **Language:** Python 3.9
* **Containerization:** Docker
* **Cloud Infrastructure:** Google Cloud Platform (Cloud Run Jobs)
* **AI/ML:** OpenAI API
* **Secrets Management:** Environment Variables (12-Factor App principles)

## 📂 Project Structure
* `src/classifier.py`: LLM logic for semantic categorization.
* `src/ingestor.py`: Secure IMAP connection handler.
* `src/notifier.py`: Slack Webhook integration.
* `Dockerfile`: Multi-stage build for production deployment.
