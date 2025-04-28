<div align="center">

# 🚀 BiddyaPeeth

<h3>Modern Learning Management System (LMS) built with Django and Tailwind CSS</h3>

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

BiddyaPeeth is a comprehensive, next-generation **Learning Management System (LMS)** built with Django and Tailwind CSS.
It provides a modern platform for online learning with:

- **Role-based dashboards** for students, teachers, and admins.
- **Course management**, **live classes**, and **assignment evaluation**.
- **Integrated payment system** for premium features.
- **Real-time communication** and **live conferencing**.

### 🔥 Why BiddyaPeeth?

Traditional LMS platforms often suffer from:
- ❌ Poor user experience.
- ❌ Difficult management of live classes and assignments.
- ❌ Lack of modern UI and scalability.

**BiddyaPeeth solves these problems** by offering:
- 🔹 Seamless course and user management.
- 🔹 Modern Tailwind CSS frontend.
- 🔹 Fast deployment with Docker and Kubernetes-ready architecture.
- 🔹 Real-time communication tools for better engagement.

### 🌍 Market Opportunity

- The global LMS market is projected to reach **$29 billion** by 2026.
- Demand for **virtual learning platforms** and **interactive education tools** is growing rapidly.

---

<div align="center">

# 🖌️ Team MindJunkies

<table style="width: 90%;">
<tr>
<td align="center" width="33%">
<h4>Shafayet Sadi</h4>
<img src="https://img.shields.io/badge/Team%20Leader-2D9CDB?style=for-the-badge">
<br><a href="https://github.com/Shafayetsadi"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
<td align="center" width="33%">
<h4>Md. Tonmoy</h4>
<img src="https://img.shields.io/badge/FullStack%20Developer-F2C94C?style=for-the-badge">
<br><a href="https://github.com/md-tonmoy007"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
</td>
<td align="center" width="33%">
<h4>Farhana Islam Saima</h4>
<img src="https://img.shields.io/badge/FullStack%20Developer-F2C94C?style=for-the-badge">
<br><a href="https://github.com/SaimaLearnathon"><img src="https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white"></a>
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
