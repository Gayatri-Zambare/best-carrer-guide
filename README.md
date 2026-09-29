# AI CareerGuide — AI-Based Student Career Guidance System

> **"Discover Your Strengths. Explore Your Future."**  
> *A full-stack, responsive Explainable AI (XAI) career guidance application designed for college project demonstration and viva evaluation in Fundamentals of Artificial Intelligence (FAI).*

---

## 🌟 1. Project Overview

**AI CareerGuide** is an intelligent web application engineered to help students discover optimal career paths based on their cognitive strengths, skills, academic stream, work style preferences, and career aspirations.

Unlike traditional static questionnaires, **AI CareerGuide** features:
1. **Explainable AI (XAI)**: Generates transparent checkmark rationales and exact skill gap breakdowns for every recommendation.
2. **Weighted 5-Factor Scoring**: Algorithmic compatibility formula:
   $$\text{Compatibility Score} = (\text{Interests} \times 30\%) + (\text{Skills} \times 25\%) + (\text{Academics} \times 15\%) + (\text{Work Style} \times 15\%) + (\text{Goals} \times 15\%)$$
3. **Interactive 28-Question Assessment**: Categorized, responsive assessment featuring custom sliders, rating cards, and multi-select tags.
4. **Interactive Multi-Stage Roadmaps**: Detailed progression paths (Stage 1 Fundamentals &rarr; Stage 4 Industry Readiness) for 20+ careers.
5. **AI Career Assistant Chatbot**: Conversational guidance widget providing personalized answers and learning advice.
6. **Administrative Dashboard**: Analytics on student streams, popular career recommendations, and full CRUD over careers and questions.
7. **Student Feedback & Viva Evaluation System**: End-to-end evaluation cycle with 5-star ratings, recommendation relevance audits, feature voting, and admin analytics.

---

## 🔑 2. Demo Credentials for Viva Evaluation

Pre-seeded accounts are immediately available for instant evaluation:

| Role | Email | Password | Access / Features |
| :--- | :--- | :--- | :--- |
| **Demo Student** | `student@aicareerguide.com` | `Student@123` | Completed profile, pre-calculated assessment report, top recommendations, roadmaps, history & feedback submission |
| **Demo Admin** | `admin@aicareerguide.com` | `Admin@123` | Administrative analytics, student evaluations & satisfaction metrics, student roster, add/edit/delete careers & questions |

*(You can also register a brand-new student account directly on the registration page with custom answers).*

---

## 🚀 3. Quick Start & Setup Instructions

### Prerequisites
* **Python**: 3.10 to 3.14
* **Node.js**: v18.0 or v20.0+ (and `npm`)

---

### Step A: Backend Setup (FastAPI + SQLite)

1. Open a terminal in the project root:
   ```bash
   cd backend
   ```

2. Activate the existing virtual environment or create a new one:
   * **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify database initialization and seed data:
   ```bash
   python -m app.database.seed
   ```
   *(This creates `ai_career_guide.db` with 21 careers, 15 skills, 28 questions, and default student/admin accounts).*

5. Start the FastAPI backend server:
   ```bash
   python run.py
   ```
   The backend will be running at: **`http://127.0.0.1:8000`**  
   Interactive Swagger API Documentation: **`http://127.0.0.1:8000/docs`**

---

### Step B: Frontend Setup (React + TypeScript + Vite + Tailwind CSS)

1. Open a second terminal and navigate to `frontend`:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be running at: **`http://localhost:5173`**

---

## 🛠️ 4. Technology Stack

### Frontend
* **React 18 & TypeScript**: Robust, type-safe component architecture.
* **Tailwind CSS**: Sleek modern design system with custom palettes, glassmorphism, and responsive layouts.
* **Lucide React**: Clean vector iconography.
* **Recharts**: Responsive Radar Chart (for cognitive profiling) and Bar Charts (for career compatibility).
* **Vite 5**: Fast development server and optimized production bundling.

### Backend
* **Python 3.14 & FastAPI**: High-performance asynchronous REST API framework.
* **SQLAlchemy ORM**: Flexible database modeling with full SQLite and PostgreSQL compatibility.
* **PyJWT**: Stateless JSON Web Token authentication.
* **PBKDF2 Hashing**: Cryptographically secure 100,000-round password hashing with random salt.
* **Pydantic v2**: Strict schema validation and serialization.

### Database
* **SQLite** (local zero-configuration database, easily adaptable to PostgreSQL via `DATABASE_URL`).

---

## 📐 5. Architecture & Recommendation Methodology

### Weighted 5-Factor Compatibility Engine
The engine computes compatibility without external paid API dependencies using transparent mathematical vectors:
1. **Interest Match (30%)**: Compares chosen activities, subjects, and preferred free-time pursuits with career domains.
2. **Skill Match (25%)**: Compares the student's ratings (1: Beginner &rarr; 5: Excellent) across 15 skills with prerequisite skill benchmarks.
3. **Academic Match (15%)**: Assesses alignment between student stream (Science, Commerce, Arts) and high-school / college grades.
4. **Work Style Preferences (15%)**: Incorporates team environment, problem-solving habits, technology adoption comfort, and public speaking confidence.
5. **Career Goals (15%)**: Factors in overarching aspirations (Leadership, High technical expertise, Entrepreneurship, Social impact).

### Transparent Explainability (XAI)
Every recommendation outputs:
* **Percentage Compatibility Score** (e.g. `88% Match`).
* **Why this matches you**: Transparent checkmarks detailing the exact factors.
* **Key matching skills**: Existing capabilities the student demonstrates.
* **Areas to develop (Skill gaps)**: Concrete skills to improve before entering the field.
* **Step-by-step Roadmaps**: Progressive guidance from beginner concepts to capstone projects.

---

## 📋 6. Complete Demonstration Flow (Viva Guide)

1. **Landing Page**:
   * Review Hero Section, custom architecture diagram (*Student &rarr; AI Analysis &rarr; Career Path*), 6 feature cards, and animated statistics.
   * Note the top quick-demo banner with one-click evaluator credentials.

2. **Login / Authentication**:
   * Click **"Demo Student"** for instant login, or create a new student account on the **Register** page.

3. **Student Dashboard**:
   * Observe the circular **Profile Completion** indicator (e.g. 75% or 100%).
   * View **Assessment Status** and top recommended career cards.

4. **Take Career Assessment**:
   * Interactive 28 questions categorized into Interests, Skills (1-5 rating sliders), Preferences, and Career Goals.
   * Progress bar updating per question.
   * Click **"Review & Submit"** to see the pre-submission review screen.
   * Experience the animated **"Analyzing your profile..."** evaluation loader.

5. **Personalized Results Page & Viva Evaluation**:
   * **Radar Chart**: Visualizes Analytical, Creativity, Communication, Leadership, Technical Interest, and Research dimensions.
   * **Compatibility Bar Chart**: Compares top 5 recommended careers.
   * **Explainable AI Breakdown**: Explains *Why it matches you*, highlights *Key matching skills*, and pinpoints *Areas to develop*.
   * **Student Guidance Feedback Form**: Interactive 5-star satisfaction rating, recommendation relevance assessment, multi-select feature evaluation, confidence rating, and qualitative comments.

6. **Career Details & Roadmap**:
   * Click **"View Career Roadmap"** on any career card.
   * Inspect the 4-stage chronological roadmap (Stage 1 Fundamentals &rarr; Stage 4 Industry Readiness).
   * Review recommended courses, required education, and "You Have" vs "You Should Improve" skill gap analysis.

7. **Career Explorer**:
   * Search through 20+ careers.
   * Filter by category tabs (*Technology, Business, Finance, Healthcare, Design, Science, Education, Media, Environment, Entrepreneurship*).
   * Sort alphabetically A-Z.

8. **AI Career Assistant Chatbot**:
   * Click the floating **AI Career Assistant** button at the bottom-right.
   * Click quick suggestion chips (e.g., *"What is the difference between a data analyst and data scientist?"* or *"What skills should I learn for data analysis?"*).
   * Review personalized responses derived from the student's profile.

9. **Admin Panel & Viva Evaluation Analytics**:
   * Sign in as `admin@aicareerguide.com` (`Admin@123`).
   * Inspect dashboard analytics: total students, completed assessments, popular career recommendations, and student stream distribution charts.
   * **Student Feedback & Evaluation Tab**: View overall student satisfaction score (stars), career confidence metrics, recommendation relevance breakdown chart, most valued features bar chart, and individual student feedback records with filters.
   * Test adding or editing a career in the **Careers** tab.
   * Test adding or editing a question in the **Questions** tab.

---

## 📡 7. API Endpoints Reference

### Authentication
* `POST /auth/register` — Register a student account
* `POST /auth/login` — Sign in and obtain JWT Bearer token
* `GET /auth/me` — Retrieve authenticated user identity

### Student
* `GET /student/profile` — Get profile, academic details, and completion percentage
* `PUT /student/profile` — Update student profile and subject grades
* `GET /student/skills` — Retrieve student's rated skills

### Career Assessment & AI Recommendations
* `GET /questions` — Fetch assessment question catalog (28 questions)
* `POST /assessment/start` — Initialize a new assessment
* `POST /assessment/submit` — Submit answers, calculate traits, and run AI matching
* `GET /recommendations` — Fetch latest assessment recommendation report
* `GET /recommendations/{id}` — Fetch specific recommendation report
* `GET /assessment/history` — Retrieve historical assessment attempts

### Student Feedback & Evaluation
* `POST /feedback` — Submit student satisfaction, relevance, and feature feedback
* `GET /feedback/status` — Check student's feedback submission status
* `GET /admin/feedbacks` — Retrieve all student evaluations (Admin)
* `GET /admin/feedbacks/summary` — Analytics summary of satisfaction, relevance, and valued features (Admin)

### Career Explorer
* `GET /careers` — Search and filter careers (`?q=...&category=...&sort=asc`)
* `GET /careers/{id}` — Full career roadmap, skills, and courses
* `GET /careers/meta/categories` — Get category distribution

### AI Career Assistant
* `POST /assistant/chat` — Conversational chatbot endpoint with student context

### Administrative Controls
* `GET /admin/dashboard` — Platform statistics and analytics charts
* `GET /admin/students` — Registered students roster
* `POST /admin/careers` — Create a new career profile
* `PUT /admin/careers/{id}` — Update an existing career
* `DELETE /admin/careers/{id}` — Delete a career profile
* `POST /admin/questions` — Add an assessment question
* `PUT /admin/questions/{id}` — Update an assessment question
* `DELETE /admin/questions/{id}` — Remove an assessment question

---

## 🔮 8. Future Enhancements

* Integration with cloud LLM providers (Google Gemini API / OpenAI API) for free-form essay evaluation.
* Direct integration with university LMS platforms via LTI standards.
* Live job market salary feeds and regional hiring trend integrations.
* PDF report export with institutional college branding.

---

## 📄 9. License

Developed for academic presentation and viva evaluation under the **MIT License**.
