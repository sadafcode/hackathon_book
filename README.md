# Physical AI & Humanoid Robotics Textbook

This repository hosts the official textbook for "Physical AI & Humanoid Robotics: Bridging the Digital Brain and Physical Body." The book is built using [Docusaurus](https://docusaurus.io/), a modern static website generator, and is designed to provide a comprehensive and practical guide to the exciting and rapidly evolving field of physical artificial intelligence and humanoid robotics.

The project utilizes a Spec-Driven Development (SDD) workflow, where content is collaboratively created and managed using SpecKit Plus.

## Installation

```bash
yarn install
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
