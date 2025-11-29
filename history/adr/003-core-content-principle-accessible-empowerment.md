# ADR-003: Core Content Principle: Accessible Empowerment

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-11-23
- **Feature:** 1-ai-millionaire-book
- **Context:** During the planning phase for Chapter 1, a critical decision was made about the book's core philosophy. To maximize engagement and impact, the book must be relatable and actionable for readers without significant financial resources.

## Decision

We will adopt the **"Principle of Accessible Empowerment"** as a guiding rule for all content creation.

This principle dictates that every strategy, example, and playbook presented in the book must be achievable by an individual with **minimal financial capital**. The focus must always be on creativity and intellectual leverage over large cash investments.

## Consequences

### Positive

- **Stronger Audience Connection:** Creates a more relatable and trusting relationship with the target reader.
- **Clear Niche:** Gives the book a clear, defensible position in a crowded market of business advice.
- **Forces Creativity:** This constraint forces the book's content to be more creative and focus on genuinely clever, leverage-based solutions.

### Negative

- **Excludes Certain Topics:** The book will intentionally ignore potentially valid, high-capital strategies (e.g., building a foundational AI model, large-scale hardware investments), thus narrowing the total scope of "AI wealth creation."
- **Potential for Oversimplification:** We must be careful not to oversimplify the challenges of bootstrapping, even in low-capital businesses.

## Alternatives Considered

- **Alternative A: Cover All Strategies**
  - **Description:** The book would cover all possible strategies for wealth creation, from zero-capital side hustles to venture-backed startups.
  - **Why Rejected:** This would dilute the book's core message and unique value proposition. It would make the content less focused and potentially intimidating for the primary target audience, violating the user's core requirement for the book to be engaging and empowering.

## References

- **Feature Spec:** `specs/1-ai-millionaire-book/spec.md`
- **Implementation Plan:** `specs/1-ai-millionaire-book/plan.md`
- **Related ADRs:** None
- **Evaluator Evidence:** None
