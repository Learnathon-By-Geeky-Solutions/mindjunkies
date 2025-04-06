# Software Requirements Specification (SRS) for team MindJunkies

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to outline the functional and non-functional requirements for the BiddyaPeeth Learning Management System (LMS) of team MindJunkies. BiddyaPeeth aims to be a comprehensive, user-friendly e-learning platform similar to Udemy and coursera, allowing instructors to create, manage, and publish courses, while enabling students to enroll, learn, and track their progress.

### 1.2 Scope
MindJunkies LMS will support:
- Instructor and student roles
- Course creation and management
- Enrollment and progress tracking
- Assignments and quizzes
- Ratings and reviews
- Live classes and video conferencing
- Role-based dashboards

### 1.3 Definitions, Acronyms, and Abbreviations
- LMS: Learning Management System
- UI: User Interface
- AWS: Amazon Web Services
- DB: Database
- SRS: Software Requirements Specification

### 1.4 Overview
This document is organized to provide a detailed view of system features, architecture, constraints, interfaces, and design considerations for the development and deployment of MindJunkies LMS.

## 2. Overall Description

### 2.1 Product Perspective
BiddyaPeeth will be a web-based application built using Django. It will be accessible through modern web browsers and support integration with third-party services (e.g., Cloudinary for image storage, video conferencing APIs).

### 2.2 Product Functions
- User authentication and authorization
- Course management (create, update, delete)
- Assignment and quiz modules
- Role-based dashboards
- Ratings and reviews
- Video conferencing
- Notifications and announcements

### 2.3 User Classes and Characteristics
- **Admin**: Manages the platform, users, and content
- **Teacher**: Creates and manages courses
- **Student**: Enrolls in and completes courses

### 2.4 Operating Environment
- Development OS: Ubuntu/Arch Linux
- Server OS: Linux (AWS EC2)
- Browsers: Chrome, Firefox, Safari

### 2.5 Constraints
- Must use Django and PostgreSQL in production
- Deployment on AWS
- SQLite is only for local development

### 2.6 Assumptions and Dependencies
- Internet access is available
- Users have a valid email for registration

## 3. System Features and Requirements

### 3.1 Course Management
**Description:** Instructors can create, edit, and delete courses.
**Functional Requirements:**
- FR1: Instructor can upload course image and preview video
- FR2: Courses can be published/unpublished

### 3.2 Enrollment
**Description:** Students can enroll in free or paid courses.
**Functional Requirements:**
- FR3: Student can browse and enroll in available courses
- FR4: Payment integration for paid courses (future phase)

### 3.3 Ratings & Reviews
**Description:** Students can rate and review completed courses.
**Functional Requirements:**
- FR5: One rating per user per course
- FR6: Course average rating updates dynamically

### 3.4 Assignment Module
**Description:** Instructors can create assignments, students can submit.
**Functional Requirements:**
- FR7: File upload support
- FR8: Instructors can grade submissions

### 3.5 Video Conferencing
**Description:** Support for live classes.
**Functional Requirements:**
- FR9: Integration with Jitsi/Zoom (future)

## 4. External Interface Requirements

### 4.1 User Interfaces
- Built using Tailwind CSS and DaisyUI
- Responsive design for desktop and mobile

### 4.2 API Interfaces
- Internal APIs used to fetch dynamic content via HTMX and JavaScript
- Backend endpoints serve Django-rendered HTML via views
- No external-facing REST APIs in the MVP phase

### 4.3 Database
- SQLite (Development)
- PostgreSQL (Production)

### 4.4 Hardware Interfaces
- Hosted on AWS EC2
- S3 for media storage (future)

## 5. Architecture Design

### 5.1 System Architecture
The system follows a standard MVC pattern using Django. Deployment is handled via AWS.

![Architecture Overview]()

### 5.2 Components
- Frontend: HTMX, Tailwind CSS, DaisyUI
- Backend: Django (Python)
- Database: SQLite (Dev), PostgreSQL (Prod)
- Storage: Cloudinary for images and videos
- Testing: pytest
- Deployment: AWS

## 6. Technology Stack
- **Backend:** Django (Python)
- **Frontend:** Tailwind CSS, DaisyUI, HTMX
- **Database:** SQLite (Development), PostgreSQL (Production)
- **Testing:** pytest
- **Deployment:** AWS (EC2, S3 in future)
- **Version Control:** Git + GitHub

## 7. Testing Strategy
- Unit tests and integration tests using `pytest`
- Manual QA before each production deployment
- CI/CD pipeline (future phase)

## 8. Appendices

### 8.1 Glossary
- **Cloudinary:** A cloud service for media storage
- **pytest:** A testing framework for Python

### 8.2 References
- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [DaisyUI Docs](https://daisyui.com/)

### 8.3 Future Scope
- AI-assisted course suggestions
- Analytics dashboard for teachers and admins
- Mobile app version
