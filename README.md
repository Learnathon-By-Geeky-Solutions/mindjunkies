
<div align="center">

# 🚀 BiddyaPeeth

<h3>Modern EdTech Platform built with Django and Tailwind CSS</h3>

<img src="docs/resources/logo.png" alt="BiddyaPeeth Logo" width="200" height="auto">

### Explore Our Documentation, Demo, and Resources!

[![View Demo](https://img.shields.io/badge/View-Demo-22c55e?style=for-the-badge&logo=vercel&logoColor=white)](https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/)
[![Documentation](https://img.shields.io/badge/View-Docs-3b82f6?style=for-the-badge&logo=readthedocs&logoColor=white)](https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/tree/main/docs)
[![Contributing](https://img.shields.io/badge/Contribute-Guide-8b5cf6?style=for-the-badge&logo=github&logoColor=white)](docs/CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

### Tech Stack

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)

</div>

---

# 🔎 About BiddyaPeeth

**BiddyaPeeth** is an advanced, next-generation **EdTech platform** built with **Django** and **Tailwind CSS**, designed to revolutionize digital learning experiences.

It offers a **modern, scalable**, and **student-centric** environment for online education, empowering both learners and instructors with seamless tools for engagement and management.

### 🚀 Key Highlights

- **Role-based dashboards** tailored for students, teachers, and administrators.
- **Comprehensive course management** — from course creation to enrollment and content delivery.
- **Live virtual classrooms** with real-time video conferencing, chat, polls, and screen sharing.
- **Integrated payment solutions** enabling access to premium educational services.
- **Dynamic community forums** for collaborative learning and peer interactions.
- **Scalable and mobile-friendly** design for accessibility across devices.

---

### 🔥 Why BiddyaPeeth?

Traditional education platforms often suffer from:
- ❌ Poor user experience.
- ❌ Limited real-time interaction capabilities.
- ❌ Lack of modern design and scalability.

**BiddyaPeeth solves these challenges** by offering:
- 🔹 Seamless course and user management.
- 🔹 A modern Tailwind CSS frontend.
- 🔹 Fast deployment with Docker and Kubernetes-ready architecture.
- 🔹 Real-time communication tools to foster active learning environments.

### 🌍 Market Opportunity

- The global EdTech market is projected to reach **$404 billion** by 2025.
- Increasing demand for **virtual education** and **interactive learning tools** worldwide.

---

## 📋 Table of Contents
- [Team](#-team)
- [Project Overview](#-project-overview)
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Database Design](#-database-design)
- [Tech Stack](#-tech-stack)
- [Development Logs](#-development-logs)
- [Getting Started](#-getting-started)
- [Development Guidelines](#-development-guidelines)
- [Testing](#-testing)
- [Resources](#-resources)
- [Contributing](#-contributing)
- [License](#-license)

<div align="center">

# 🖌️ Team MindJunkies

<table style="width: 90%;">
<tr>
<td align="center" width="25%">
<h4>Shafayet Sadi</h4>
<img src="https://img.shields.io/badge/Team%20Leader-2D9CDB?style=for-the-badge">
<br><a href="https://github.com/Shafayetsadi"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
<td align="center" width="25%">
<h4>Md. Tonmoy</h4>
<img src="https://img.shields.io/badge/FullStack%20Developer-F2C94C?style=for-the-badge">
<br><a href="https://github.com/md-tonmoy007"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
<td align="center" width="25%">
<h4>Farhana Islam Saima</h4>
<img src="https://img.shields.io/badge/FullStack%20Developer-F2C94C?style=for-the-badge">
<br><a href="https://github.com/SaimaLearnathon"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
<td align="center" width="25%">
<h4>Md. Redwanuzzaman</h4>
<img src="https://img.shields.io/badge/Mentor-F2C94C?style=for-the-badge">
<br><a href="https://github.com/redwanuzzaman"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
</tr>
</table>

</div>

---

## 🏗 System Architecture

### 📌 Modules Overview

| Module         | Purpose                                  |
|----------------|------------------------------------------|
| Accounts       | User Authentication and Profile          |
| Courses        | Course Creation, Enrollment              |
| Dashboard      | Role-Based Dashboards (Student, Teacher) |
| Forums         | Community Discussions                   |
| Lecture        | Lecture and Assignment Management       |
| Live Classes   | Live Video Integration                   |
| Payments       | Payment and Billing                      |

### 📂 Project Structure

```bash
mindjunkies/
├── accounts/
├── courses/
├── dashboard/
├── forums/
├── lecture/
├── live_classes/
├── payments/
├── static/
├── templates/
project/
├── settings/
└── urls.py
config/  # JWT and Tokens
k8s/     # Kubernetes Deployment Files
docs/    # Documentation
Dockerfile
manage.py

```

----------

## Resources

- [Wiki Link](https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies/wiki)
- [Project Documentation](docs/)
- [Development Setup](docs/guides/getting-started.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)


----------


## Getting Started

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.11+
- uv
- PostgreSQL / SQLite

### Local Development Setup

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


### Using Docker

```bash
# Build and start containers
docker-compose up --build

```
----------
## 🤝 Contributing

We welcome contributions!  
Please read our [CONTRIBUTING.md](docs/CONTRIBUTING.md) for more information on how to get started.

----------



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
