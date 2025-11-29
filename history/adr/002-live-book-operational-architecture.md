# ADR-002: Live Book Operational Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-11-23
- **Feature:** 1-ai-millionaire-book
- **Context:** The specification requires the project to be a "live book" that is continuously updated with minimal friction. We need a defined architecture for how content updates are deployed and how community feedback is managed.

## Decision

The operational architecture for the live book will be a cluster of three components:
1.  **CI/CD Pipeline:** A **GitHub Actions** workflow will automatically build and deploy the Docusaurus site on every push to the `master` branch.
2.  **Public Changelog:** The built-in **Docusaurus blog feature** will be used to document all significant content updates, serving as a public changelog.
3.  **Community Feedback Loop:** **GitHub Discussions** will be enabled on the repository to serve as the primary channel for reader feedback, error reporting, and suggestions.

## Consequences

### Positive

- **Automation:** Updates are seamless and require no manual deployment steps, which encourages frequent improvements and keeps the book current.
- **Integration:** The feedback loop and source code live in the same ecosystem (GitHub), creating a tight-knit development process.
- **Standardization:** This architecture uses well-supported, standard tools, making it easy to maintain.

### Negative

- **Setup Complexity:** The CI/CD workflow adds an initial layer of configuration complexity to the project.
- **Platform Dependency:** This architecture is tightly coupled to the GitHub ecosystem (Actions, Discussions). Migrating to another platform like GitLab would require rework.

## Alternatives Considered

- **Alternative A: Manual Operations**
  - **Description:** Manually build the site locally and upload the static files to a web host via FTP or a web dashboard after every change. Use email or a Google Form for feedback.
  - **Why Rejected:** This process is slow, error-prone, and creates a significant barrier to making small, frequent updates, which defeats the core purpose of a "live book."

- **Alternative B: Third-Party Feedback System**
  - **Description:** Use an external tool like Disqus, Canny, or a dedicated forum for community feedback.
  - **Why Rejected:** For the initial launch, this adds unnecessary complexity and cost. GitHub Discussions is sufficient, free, and keeps all project-related artifacts in one location. We can re-evaluate this if the community scales significantly.

## References

- **Feature Spec:** `specs/1-ai-millionaire-book/spec.md`
- **Implementation Plan:** `specs/1-ai-millionaire-book/plan.md`
- **Related ADRs:** `ADR-001`
- **Evaluator Evidence:** None
