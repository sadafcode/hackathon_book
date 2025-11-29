# Constitution for "Physical AI & Humanoid Robotics" Project

## 1. Vision & Goal

- **Project:** To collaboratively create a high-quality, complete textbook titled "Physical AI & Humanoid Robotics: Bridging the Digital Brain and Physical Body" using a Spec-Driven Development (SDD) workflow. This book will serve as a textbook for teaching a Physical AI & Humanoid Robotics course, focusing on AI systems in the physical world and embodied intelligence. Students will apply their AI knowledge to control Humanoid Robots in simulated and real-world environments.
- **Toolchain:** The book will be built as a static website using Docusaurus, written in Markdown.
- **Methodology:** This project will strictly follow an AI-Driven, Spec-Driven model. The human author sets the direction and specifications, and the AI agent executes them.

## 2. Core Principles

- **Spec-First:** Every action, from creating a chapter to writing a paragraph, must begin with a clear, approved specification. No work should be done "ad-hoc."
- **AI as Implementer:** The AI agent is the primary executor of tasks. It handles scaffolding, content generation, code changes, and repository management based on the provided specs.
- **Human as Architect & Author:** The human user is the project lead. Their role is to define the vision, create high-level specifications (outlines), review the AI's output, and make all final creative and architectural decisions.
- **Iterative & Incremental:** The book will be built in small, manageable increments (e.g., section by section). Each increment will be a complete loop of Spec -> Implement -> Review.
- **Single Source of Truth:** The Git repository is the absolute source of truth for all specifications, content, and project history.
- **Automated Record-Keeping:** The development process will be transparently documented using Prompt History Records (PHRs) and Architectural Decision Records (ADRs) as needed.
- **Rigorous Quality Assurance:** All project artifacts, including content (prose), Docusaurus configuration, and custom components, will strive for 100% test coverage. This commitment ensures accuracy, consistency, functionality, and adherence to specifications.

## 3. Workflow (Spec-Driven Development)

We will follow the SpecKit Plus flow for all content creation:

1.  **`/sp.specify` (Book Outline):** The Author provides the high-level structure of the book, including parts, chapters, and a brief description of each. This is our master plan.
2.  **`/sp.plan` (Chapter Plan):** For each chapter, the Author and Agent collaborate to create a detailed plan. This spec includes the chapter's objective, key topics, target audience, and desired tone.
3.  **`/sp.tasks` (Section Tasks):** The chapter plan is broken down into a list of concrete, actionable tasks, typically one task per section or major concept.
4.  **`/sp.implement` (Content Generation):** The Agent executes a single task by generating the corresponding content in a Markdown file, following the spec precisely.
5.  **Review & Refine:** The Author reviews the generated content against the spec and a quality checklist. If it meets the standard, it's approved. If not, the Author provides specific, actionable feedback, and the Agent refines the content in a new iteration. A piece of content is not "done" until the Author approves it.

## 4. Technical & Style Standards

### 4.1. External API Key Management
Sensitive API keys and database credentials required for external services (e.g., Qdrant, Neon Serverless Postgres, Google Generative AI) must be managed securely. For embedding, Hugging Face SentenceTransformers models are used locally or client-side. They will be loaded from environment variables (e.g., `.env` files in development, secure injection in production environments) and will **never** be hardcoded into the codebase. This ensures that credentials are not exposed in source control and can be easily managed across different deployment environments.

- **Framework:** Docusaurus v3.
- **Language:** Markdown (with MDX for interactive components if needed).
- **Version Control:** Git. All changes must be committed with clear, descriptive messages.
- **File Structure:**
    - All book content resides in the `/docs` directory.
    - Files will be named using a numeric prefix for ordering (e.g., `01-introduction.md`, `02-getting-started.md`).
    - Images and other assets will be stored in `/static/img`.
- **Content Style:**
    - **Tone:** To be defined in the spec for each chapter (e.g., formal, conversational, technical).
    - **Formatting:** Use standard Markdown. Leverage Docusaurus admonitions (`:::note`, `:::tip`, `:::caution`) for emphasis.
- **Content Metadata for AI Readiness:** To ensure content is optimized for future search and RAG chatbot integration, each content page must include a front-matter block. This block should contain relevant `keywords` and `tags` that will be defined during the `/sp.tasks` stage.
- **Quality Assurance & Testing (100% Coverage Commitment):**
    - **Content Validation (Tests for Prose):**
        -   **Linting:** All Markdown content must adhere to a consistent style and structure, enforced automatically by `markdownlint`. A project-level configuration (`.markdownlint.json`) will define our specific rules.
        -   **Spelling & Grammar:** Content will undergo automated spelling and grammar checks to ensure professional quality.
        -   **Link Integrity:** All hyperlinks (internal and external) must be periodically validated to ensure they are not broken, providing a seamless reading experience.
        -   **Specification Compliance:** The primary "test" for AI-generated content is its direct compliance with the Author's explicit content specifications (`/sp.tasks`, `/sp.plan`). Content is not approved until it demonstrably meets its spec through Author review.
    -   **Code Validation (Tests for Docusaurus Configuration & Custom Components):**
        -   Docusaurus configuration (`docusaurus.config.js`), custom React components, and any MDX components will be subject to unit and integration tests. These tests will aim for 100% code coverage where applicable and meaningful, ensuring functionality and stability.
- **Accessibility:** All images must include descriptive `alt` text to be accessible to screen readers. Content should be structured semantically (e.g., correct heading levels) to ensure it is usable by everyone.
- **MDX Usage:** The use of custom React components via MDX should be minimized in favor of standard Markdown for simplicity and portability. Any proposed use of MDX must be justified as providing significant value in the `/sp.plan` stage and explicitly approved by the Author.

## 5. Roles & Responsibilities

- **The Author (Human):**
    - Owns the creative vision and intellectual property.
    - Creates and approves all specifications.
    - Reviews and provides final approval on all generated content.
    - Merges pull requests and manages the main branch.
- **The Agent (AI):**
    - Initializes and configures the Docusaurus project.
    - Generates content based on approved tasks.
    - Creates and modifies files as required.
    - Manages its own feature branches and submits work for review.
    - Enforces the rules of this constitution.

---

This constitution is a living document. It can be amended by the Author to adapt to the project's evolving needs.
