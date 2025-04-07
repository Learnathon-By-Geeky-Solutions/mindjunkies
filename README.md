<div align="center">

  <img src="docs/resources/logo.png" alt="logo" width="200" height="auto" />
  <h1>BiddyaPeeth</h1>

  <p>
    A modern Learning Management System (LMS) built with Django and Tailwind CSS.
  </p>


<!-- Badges -->
<p>
  <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/Learnathon-By-Geeky-Solutions/mindjunkies" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/Learnathon-By-Geeky-Solutions/mindjunkies" alt="last update" />
  </a>
  <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/network/members">
    <img src="https://img.shields.io/github/forks/Learnathon-By-Geeky-Solutions/mindjunkies" alt="forks" />
  </a>
  <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/stargazers">
    <img src="https://img.shields.io/github/stars/Learnathon-By-Geeky-Solutions/mindjunkies" alt="stars" />
  </a>
  <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/issues/">
    <img src="https://img.shields.io/github/issues/Learnathon-By-Geeky-Solutions/mindjunkies" alt="open issues" />
  </a>
  <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Learnathon-By-Geeky-Solutions/mindjunkies.svg" alt="license" />
  </a>

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</p>

<h4>
    <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/blob/main/docs">Documentation</a>
  <span> · </span>
    <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/issues/">Request Feature</a>
  </h4>
</div>

---

# Team MindJunkies

**BiddyaPeeth** is a modern Learning Management System (LMS) built with Django and Tailwind CSS. It offers a seamless platform for managing courses, users, assignments, and learning content efficiently. Designed to empower teachers and students, MindJunkies focuses on scalability, user experience, and modern web standards.

## Table of Contents
- [Team Members](#team-members)
- [Mentor](#mentor)
- [Project Description](#project-description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Development Guidelines](#development-guidelines)
- [Project Structure](#project-structure)
- [Resources](#resources)
- [Tools and Technologies](#tools-and-technologies)
- [License](#license)


## Team Members

- [shafayetsadi](https://github.com/Shafayetsadi/)  (Team Leader)
- [md-tonmoy007](https://github.com/md-tonmoy007)
- [SaimaLearnathon](https://github.com/SaimaLearnathon)

## Mentor

- [Md. Redwanuzzaman](https://github.com/redwanuzzaman)

## Project Description

BiddyaPeeth is a comprehensive Learning Management System (LMS) designed to facilitate online learning and course management. The platform allows teachers to create, manage, and publish courses while enabling students to enroll, learn, and track their progress. With features like live video conferencing, assignment submission, and role-based dashboards, BiddyaPeeth aims to provide a seamless and engaging learning experience.


## Features

- User Authentication (Registration, Login, Social Auth, Email Verification)
- Role-based Access Control (Teachers, Students, Moderators)
- Course Management (Create, Join, Edit)
- Markdown-based Content Writing for Teachers
- Live Video Conferencing with Chat, Polls, and Screen Sharing
- Assignment Submission and Evaluation
- Payment Integration for Premium Features
- Responsive Design with Tailwind CSS

---

## Getting Started

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.11+
- uv
- PostgreSQL / SQLite

### Setup Instructions

1. Clone the repository:
    ```sh
    git clone https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies
    cd mindjunkies
    ```
2. Install dependencies:
    ```sh
    pip install uv
    uv sync
    ```
3. Start development:
    ```sh
    cp .env.example .env # Modify the environment variables
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    python manage.py tailwind watch
    ```
4. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Development Guidelines

1. Create feature branches:
    ```sh
    git checkout -b feature/your-feature-name
    ```
2. Commit Changes:
    - Keep commits small and focused.
    - Use clear and descriptive commit messages.
    ```sh
    git add .
    git commit -m "Add feature: [feature-name]"
    ```
3. Push Your Changes:
    ```sh
    git push origin feature/your-feature-name
    ```
4. Submit a Pull Request:
    - Open a Pull Request against the `develop` branch.
    - Add a clear title and description.
    - Mention the issue number (if any) in the description.
    - Assign the PR to the appropriate reviewer.

## Project Structure

```plaintext
mindjunkies/
├── manage.py
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── mindjunkies/
│   ├── __init__.py
│   ├── accounts/
│   ├── courses/
│   ├── dashboard/
│   ├── forums/
│   ├── home/
│   ├── lecture/
│   ├── live_classes/
│   ├── payments/
│   ├── static/
│   ├── templates/
├── tests/
```

## Resources

- [Project Documentation](docs/)
- [Development Setup](docs/guides/getting-started.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## Tools and Technologies

- Django
- Tailwind CSS
- DaisyUI
- SQLite (Development), PostgreSQL (Production)
- AWS (Deployment)
- Git and GitHub

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
