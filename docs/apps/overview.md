# 🧩 App Overview

This section provides a structured overview of the **Django apps** that make up the **MindJunkies LMS (BiddyaPeeth)** platform. Each app follows the **Single Responsibility Principle**, helping to keep the system modular, testable, and easy to maintain.

---

## 🗂 Django Apps Structure

| App Name       | Description |
|----------------|-------------|
| **`accounts`** | Handles user authentication, registration, login/logout, password reset, social login (via allauth), and user role management (Student, Teacher, Admin). |
| **`courses`** | Manages course creation, editing, deletion (CRUD), student enrollment, module structure, rating and tagging, and category organization. |
| **`dashboard`** | Provides role-based dashboards (Student, Teacher, Admin) showing relevant data and actions like course progress, income reports, course approvals, etc. |
| **`forums`** | A built-in discussion board for each course where students and teachers can ask questions, reply to threads, and upvote answers (threaded discussions). |
| **`home`** | Manages landing pages, static info pages, and the main homepage content. Also handles custom 404, about us, and contact pages. |
| **`lecture`** | Handles lecture content such as PDFs, videos, text descriptions, and student lecture progress tracking. Includes lecture creation, editing, and completion. |
| **`live_classes`** | Supports real-time live classes using Jitsi Meet with secure JWT token generation. Teachers can schedule, start, and manage live classes. |
| **`payments`** | Processes secure payments using SSLCommerz and Stripe. Handles transactions, balance tracking, withdrawal logic, and post-payment enrollment. |

---

## 🏗️ App Modularity Benefits

- 🔄 Easy to reuse and extend
- 🧪 Each app is independently testable
- 📦 Clear separation of business logic
- 👥 Makes team collaboration easier (each dev can own an app)
