---
id: adr-001-external-api-key-management
title: ADR 001 - External API Key Management
sidebar_position: 1
---

# ADR 001 - External API Key Management

## 1. Status
Accepted

## 2. Context
The project requires integration with several external services, including OpenAI (for embeddings and generative AI), Qdrant Cloud (for vector database storage), and Neon Serverless Postgres (for metadata storage). These services require API keys and database credentials to authenticate and authorize access.

## 3. Decision
Sensitive API keys and database credentials will be managed as environment variables. These variables will be loaded via `python-dotenv` in development environments and through secure injection mechanisms in production environments. They will **never** be hardcoded into the codebase or committed to version control.

## 4. Consequences
*   **Security:** Reduces the risk of credential exposure in source code repositories.
*   **Flexibility:** Allows for easy management and rotation of credentials across different development, staging, and production environments without code changes.
*   **Development Workflow:** Developers must ensure their local `.env` files are correctly configured with the necessary credentials for local development.
*   **Deployment:** Requires proper configuration of environment variables in CI/CD pipelines and deployment platforms.

## 5. Required Environment Variables
*   `OPENAI_API_KEY`: API key for OpenAI services (embeddings and chat completions).
*   `QDRANT_HOST`: Host URL for the Qdrant Cloud instance.
*   `QDRANT_API_KEY`: API key for authenticating with Qdrant Cloud.
*   `DATABASE_URL`: Connection string for the Neon Serverless Postgres database.

## 6. Adherence to Constitution
This decision aligns with the `Automated Record-Keeping` principle and has been explicitly documented in `4.1. External API Key Management` of the project's `constitution.md` to enforce the secure handling of sensitive credentials.