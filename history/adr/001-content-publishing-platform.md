# ADR-001: Content Publishing Platform

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-11-23
- **Feature:** 1-ai-millionaire-book
- **Context:** We need to select a platform to build, manage, and deploy a 'live book'. The platform must support Markdown, be easy to update via Git, have good SEO, and allow for potential future customization with interactive components.

## Decision

We will use **Docusaurus** as our content publishing platform. It will be the foundation for the entire book website, rendering our Markdown content into a navigable static site.

## Consequences

### Positive

- **React-based:** Allows for rich, custom interactivity using React components within Markdown (MDX).
- **Extensible:** Strong community and plugin ecosystem.
- **Live Book Features:** Built-in features like versioning, search, and a blog are ideal for our "live book" concept and public changelog requirement.
- **Performance & Security:** Generates a static site which is inherently fast, secure, and easy to host.

### Negative

- **Operational Overhead:** Requires management of a Node.js environment and a CI/CD deployment pipeline, unlike a fully hosted solution.
- **Build Times:** As the book grows, site build times may increase.

## Alternatives Considered

- **Alternative A: GitBook**
  - **Description:** A fully hosted platform for documentation and books.
  - **Why Rejected:** While simpler to set up, it offers significantly less customization, control over the deployment pipeline, and potential for custom interactive components. It would limit our ability to create a unique product.

- **Alternative B: Custom Next.js Site**
  - **Description:** Building the book site from scratch using a framework like Next.js.
  - **Why Rejected:** This would provide maximum flexibility but require building many core features (theming, sidebars, search, MDX processing) from scratch, which is an unnecessary engineering effort given that Docusaurus provides this out-of-the-box.

## References

- **Feature Spec:** `specs/1-ai-millionaire-book/spec.md`
- **Implementation Plan:** `specs/1-ai-millionaire-book/plan.md`
- **Related ADRs:** None
- **Evaluator Evidence:** None
