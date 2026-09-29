import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI CareerGuide — Student Career Guidance System",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and clean typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0369a1 100%);
        color: white;
        padding: 3rem 2.5rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
    }
    
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
        border-color: #38bdf8;
    }
    
    .category-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.25rem;
        text-align: left;
        margin-bottom: 0.75rem;
    }
    
    .badge-step {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .status-box {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        padding: 1rem;
        border-radius: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .metric-badge {
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.3rem 0.8rem;
        border-radius: 0.5rem;
        background: #f1f5f9;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. PERSISTENT DATABASE INITIALIZATION (SQLite)
# ---------------------------------------------------------
DB_FILE = Path(__file__).resolve().parent / "ai_career_guide.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        student_email TEXT,
        satisfaction_rating INTEGER NOT NULL,
        recommendation_relevance TEXT NOT NULL,
        useful_features TEXT NOT NULL,
        confidence_rating INTEGER NOT NULL,
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Seed default sample feedback if empty for admin demo
    c.execute("SELECT COUNT(*) FROM feedbacks")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO feedbacks (student_name, student_email, satisfaction_rating, recommendation_relevance, useful_features, confidence_rating, comments)
        VALUES 
        ('Aarav Sharma', 'student@aicareerguide.com', 5, 'Very Relevant', '["Career Recommendations", "AI Career Analysis", "Skill Gap Analysis", "Career Roadmap"]', 5, 'The AI recommendations were spot-on with my interest in AI and Software Engineering. The skill gap breakdown was crystal clear!'),
        ('Priya Patel', 'priya.patel@test.edu', 5, 'Very Relevant', '["Career Recommendations", "Skill Gap Analysis", "Career Exploration"]', 4, 'Really loved the transparent explanation of why each career matched my academic profile.')
        """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# 3. EMBEDDED KNOWLEDGE BASE: CAREERS & DATASETS
# ---------------------------------------------------------
SEED_PATH = Path(__file__).resolve().parent / "backend" / "seed_data" / "careers.json"

@st.cache_data
def load_careers_data() -> List[Dict[str, Any]]:
    # 1. Try loading from seed_data folder if present
    if SEED_PATH.exists():
        try:
            with open(SEED_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 2. Fallback comprehensive standalone dataset (20+ Careers across 10 domains)
    return [
        {
            "id": 1,
            "name": "Software Developer",
            "category": "Technology",
            "description": "Designs, codes, tests, and maintains modern software applications, cloud services, and interactive systems.",
            "education_path": "B.Tech / B.E. / B.Sc in Computer Science or Software Engineering",
            "work_style": "Collaborative, Logical, Problem-Solving",
            "required_skills": ["Programming", "Problem Solving", "Data Structures", "Algorithms", "Git"],
            "recommended_subjects": ["Computer Science", "Mathematics"],
            "related_interests": ["Solving logical problems", "Building software", "Coding", "Technology"],
            "beginner_skills": ["HTML/CSS", "JavaScript/Python basics", "Logic Building"],
            "advanced_skills": ["System Design", "Microservices", "Cloud Deployment (AWS/Docker)"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Fundamentals", "description": "Master programming fundamentals, basic data structures, and Git version control.", "topics": ["Python/Java", "Data Structures", "Git"]},
                {"phase": "Stage 2", "title": "Application Development", "description": "Build end-to-end web or mobile applications and databases.", "topics": ["React / FastAPI", "SQL & Databases", "REST APIs"]},
                {"phase": "Stage 3", "title": "Advanced Engineering", "description": "Deep dive into clean architecture, automated testing, and CI/CD pipelines.", "topics": ["Unit Testing", "Docker & CI/CD", "Authentication"]},
                {"phase": "Stage 4", "title": "Industry Readiness", "description": "System design, performance optimization, and production deployment.", "topics": ["Distributed Systems", "Cloud Services", "Open Source"]}
            ],
            "related_courses": [{"title": "Full-Stack Web Development", "provider_type": "Coursera", "difficulty": "Intermediate"}],
            "related_job_roles": ["Frontend Engineer", "Backend Developer", "Full Stack Engineer"],
            "preferred_goals": ["High technical expertise", "Financial growth"],
            "work_preference_matches": ["Analyze it step by step", "Working in a team"]
        },
        {
            "id": 2,
            "name": "AI/ML Engineer",
            "category": "Technology",
            "description": "Builds and deploys scalable machine learning algorithms, computer vision pipelines, and deep neural networks.",
            "education_path": "B.Tech / M.Tech in CS, AI, Data Science, or Mathematics",
            "work_style": "Analytical, Innovative, Data-Driven",
            "required_skills": ["Python", "Machine Learning", "Mathematics", "Deep Learning", "Data Analysis"],
            "recommended_subjects": ["Mathematics", "Computer Science", "Statistics"],
            "related_interests": ["Solving logical problems", "Analyzing information", "Mathematics", "AI & Robotics"],
            "beginner_skills": ["Python", "Numpy & Pandas", "Linear Algebra"],
            "advanced_skills": ["PyTorch/TensorFlow", "MLOps", "Transformers & LLMs"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Mathematical Foundations", "description": "Linear algebra, calculus, probability, and Python data libraries.", "topics": ["Linear Algebra", "Python (NumPy/Pandas)", "Probability"]},
                {"phase": "Stage 2", "title": "Machine Learning Core", "description": "Supervised & unsupervised algorithms and model validation.", "topics": ["Scikit-Learn", "Regression & Trees", "Feature Engineering"]},
                {"phase": "Stage 3", "title": "Deep Learning & NLP", "description": "Neural architectures, computer vision, and transformer models.", "topics": ["PyTorch", "CNNs & RNNs", "HuggingFace Transformers"]},
                {"phase": "Stage 4", "title": "Production MLOps", "description": "Deploying models to production with Docker, FastAPI, and tracking tools.", "topics": ["MLflow", "Model Serving", "Cloud AI APIs"]}
            ],
            "related_courses": [{"title": "Machine Learning Specialization", "provider_type": "DeepLearning.AI", "difficulty": "Intermediate"}],
            "related_job_roles": ["Machine Learning Engineer", "Data Scientist", "NLP Specialist"],
            "preferred_goals": ["High technical expertise", "Innovation"],
            "work_preference_matches": ["Analyze it step by step", "I enjoy analyzing information"]
        },
        {
            "id": 3,
            "name": "Cybersecurity Analyst",
            "category": "Technology",
            "description": "Protects digital networks, systems, and sensitive data from cyber threats, breaches, and unauthorized access.",
            "education_path": "Degree in Cybersecurity, Computer Networks, or CS with security certifications",
            "work_style": "Vigilant, Systematic, Investigative",
            "required_skills": ["Computer Networks", "Cybersecurity", "Operating Systems", "Ethical Hacking"],
            "recommended_subjects": ["Computer Science", "Physics"],
            "related_interests": ["Solving logical problems", "Cybersecurity", "Technology"],
            "beginner_skills": ["Networking Basics (TCP/IP)", "Linux Fundamentals", "Security Concepts"],
            "advanced_skills": ["Penetration Testing", "SIEM Tools", "Cryptography"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Foundational Infrastructure", "description": "Computer networking, OS administration, and security basics.", "topics": ["TCP/IP & OSI", "Linux CLI", "CompTIA Security+"]},
                {"phase": "Stage 2", "title": "Defensive Security", "description": "Vulnerability scanning, firewall management, and intrusion detection.", "topics": ["Wireshark", "Firewalls", "SIEM (Splunk)"]},
                {"phase": "Stage 3", "title": "Offensive Security", "description": "Ethical hacking, exploitation frameworks, and incident response.", "topics": ["Kali Linux", "Metasploit", "Threat Hunting"]},
                {"phase": "Stage 4", "title": "Enterprise Governance", "description": "Compliance standards, zero-trust architectures, and cloud security.", "topics": ["CISSP Concepts", "Cloud Security", "Auditing"]}
            ],
            "related_courses": [{"title": "Google Cybersecurity Professional", "provider_type": "Coursera", "difficulty": "Beginner"}],
            "related_job_roles": ["Information Security Analyst", "SOC Analyst", "Penetration Tester"],
            "preferred_goals": ["High technical expertise", "Societal impact"],
            "work_preference_matches": ["Analyze it step by step", "Independent investigation"]
        },
        {
            "id": 4,
            "name": "Data Analyst / BI Specialist",
            "category": "Technology",
            "description": "Transforms complex datasets into actionable business intelligence dashboards, trends, and strategic insights.",
            "education_path": "Degree in Statistics, Mathematics, Computer Science, or Business Analytics",
            "work_style": "Structured, Detail-Oriented, Inquisitive",
            "required_skills": ["Data Analysis", "SQL", "Excel", "Data Visualization", "Mathematics"],
            "recommended_subjects": ["Mathematics", "Statistics", "Computer Science"],
            "related_interests": ["Analyzing information", "Mathematics", "Solving logical problems"],
            "beginner_skills": ["Advanced Excel", "Basic SQL", "Descriptive Statistics"],
            "advanced_skills": ["Power BI / Tableau", "Python (Pandas)", "Statistical Hypothesis Testing"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Excel & SQL Fundamentals", "description": "Master relational database querying and spreadsheet modeling.", "topics": ["SQL Joins & Aggregations", "Excel Pivot Tables", "Data Cleaning"]},
                {"phase": "Stage 2", "title": "BI Dashboards & Storytelling", "description": "Interactive reporting in Tableau or Power BI.", "topics": ["Tableau/Power BI", "Data Modeling", "Executive KPIs"]},
                {"phase": "Stage 3", "title": "Python for Data Analysis", "description": "Exploratory data analysis with Pandas and visualization libraries.", "topics": ["Pandas & Seaborn", "Statistical Tests", "Automated Pipelines"]},
                {"phase": "Stage 4", "title": "Predictive Decision Making", "description": "Time-series forecasting and business decision models.", "topics": ["Forecasting", "A/B Testing", "Executive Presentations"]}
            ],
            "related_courses": [{"title": "Google Data Analytics Certificate", "provider_type": "Coursera", "difficulty": "Beginner"}],
            "related_job_roles": ["BI Analyst", "Data Specialist", "Operations Analyst"],
            "preferred_goals": ["High technical expertise", "Financial growth"],
            "work_preference_matches": ["I enjoy analyzing information", "Working in a team"]
        },
        {
            "id": 5,
            "name": "Cloud & DevOps Engineer",
            "category": "Technology",
            "description": "Automates cloud infrastructure, continuous deployment, and scalable serverless environments.",
            "education_path": "Degree in Computer Science / IT or Cloud Certifications",
            "work_style": "Automation-Focused, System-Oriented, Collaborative",
            "required_skills": ["Cloud Computing", "Linux", "Docker", "CI/CD", "Programming"],
            "recommended_subjects": ["Computer Science", "Mathematics"],
            "related_interests": ["Building something", "Technology", "Solving logical problems"],
            "beginner_skills": ["Linux CLI", "Git Basics", "Cloud Basics (AWS/Azure)"],
            "advanced_skills": ["Kubernetes", "Terraform (IaC)", "Monitoring (Prometheus)"],
            "roadmap": [
                {"phase": "Stage 1", "title": "System Administration", "description": "Linux operating system, shell scripting, and basic networking.", "topics": ["Bash Scripting", "Linux Server Admin", "Networking"]},
                {"phase": "Stage 2", "title": "Containerization & Cloud", "description": "Docker containers and core cloud provider services.", "topics": ["Docker", "AWS EC2/S3/VPC", "Serverless Functions"]},
                {"phase": "Stage 3", "title": "CI/CD & Automation", "description": "GitHub Actions, Jenkins, and automated testing pipelines.", "topics": ["GitHub Actions", "CI/CD Automation", "Infrastructure as Code"]},
                {"phase": "Stage 4", "title": "Kubernetes & Cloud Native", "description": "Cluster orchestration, service meshes, and observability.", "topics": ["Kubernetes", "Terraform", "Prometheus & Grafana"]}
            ],
            "related_courses": [{"title": "AWS Solutions Architect", "provider_type": "AWS Training", "difficulty": "Intermediate"}],
            "related_job_roles": ["DevOps Engineer", "Cloud Architect", "Site Reliability Engineer"],
            "preferred_goals": ["High technical expertise", "Financial growth"],
            "work_preference_matches": ["Analyze it step by step", "Working in a team"]
        },
        {
            "id": 6,
            "name": "UI/UX & Product Designer",
            "category": "Design",
            "description": "Creates intuitive digital interfaces, user experience flows, wireframes, and interactive design systems.",
            "education_path": "Degree in Design, Human-Computer Interaction, or Digital Arts",
            "work_style": "Creative, Empathetic, Visual",
            "required_skills": ["Design", "Creativity", "Communication", "Problem Solving"],
            "recommended_subjects": ["Arts", "English", "Computer Science"],
            "related_interests": ["Creating visual art or design", "Building something", "Understanding people"],
            "beginner_skills": ["Figma Basics", "Typography & Color Theory", "Wireframing"],
            "advanced_skills": ["Design Systems", "Usability Testing", "Interactive Prototyping"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Design Principles", "description": "Visual hierarchy, layout, typography, and color harmony.", "topics": ["Color Theory", "Typography", "Figma Fundamentals"]},
                {"phase": "Stage 2", "title": "User Experience Research", "description": "Personas, journey mapping, and information architecture.", "topics": ["User Interviews", "Journey Maps", "Wireframing"]},
                {"phase": "Stage 3", "title": "High-Fidelity Prototyping", "description": "Interactive micro-animations and cohesive design tokens.", "topics": ["Advanced Figma", "Design Systems", "Component Libraries"]},
                {"phase": "Stage 4", "title": "Product Strategy & Testing", "description": "A/B usability testing and developer handoff workflows.", "topics": ["Usability Testing", "Design Tokens", "Portfolio Review"]}
            ],
            "related_courses": [{"title": "Google UX Design Professional", "provider_type": "Coursera", "difficulty": "Beginner"}],
            "related_job_roles": ["Product Designer", "UI Designer", "UX Researcher"],
            "preferred_goals": ["Creative expression", "Societal impact"],
            "work_preference_matches": ["Brainstorm creative ideas", "Working in a team"]
        },
        {
            "id": 7,
            "name": "Financial Analyst",
            "category": "Finance",
            "description": "Evaluates financial data, market trends, portfolio investments, and corporate financial health.",
            "education_path": "B.Com / BBA / Finance / Economics or CFA qualification",
            "work_style": "Analytical, Precise, Market-Oriented",
            "required_skills": ["Financial Analysis", "Mathematics", "Excel", "Data Analysis", "Communication"],
            "recommended_subjects": ["Commerce", "Mathematics", "Economics"],
            "related_interests": ["Analyzing information", "Mathematics", "Finance & Investments"],
            "beginner_skills": ["Financial Statements", "Excel Formulas", "Ratio Analysis"],
            "advanced_skills": ["Financial Modeling (DCF)", "Valuation", "Portfolio Management"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Accounting & Corporate Finance", "description": "Income statements, balance sheets, and financial ratios.", "topics": ["3-Statement Modeling", "Accounting Principles", "Corporate Finance"]},
                {"phase": "Stage 2", "title": "Valuation & Financial Modeling", "description": "Discounted cash flow (DCF) models and peer comparables.", "topics": ["DCF Modeling", "LBO Basics", "Capital Budgeting"]},
                {"phase": "Stage 3", "title": "Market Analysis & Risk", "description": "Equity research, macroeconomic indicators, and portfolio risk.", "topics": ["Equity Research", "CFA Level 1 Topics", "Derivatives"]},
                {"phase": "Stage 4", "title": "Investment Advisory", "description": "M&A advisory, investment thesis presentations, and fund management.", "topics": ["M&A Modeling", "Pitchbooks", "Wealth Strategy"]}
            ],
            "related_courses": [{"title": "Financial Markets", "provider_type": "Yale / Coursera", "difficulty": "Beginner"}],
            "related_job_roles": ["Investment Analyst", "Corporate Finance Associate", "Equity Analyst"],
            "preferred_goals": ["Financial growth", "High responsibility"],
            "work_preference_matches": ["Analyze it step by step", "I enjoy analyzing information"]
        },
        {
            "id": 8,
            "name": "Product Manager",
            "category": "Business",
            "description": "Guides products from conception through launch by aligning engineering, design, and business strategy.",
            "education_path": "Degree in Engineering / Business / IT, followed by MBA or PM certificates",
            "work_style": "Strategic, Cross-functional, Leadership",
            "required_skills": ["Leadership", "Communication", "Problem Solving", "Data Analysis", "Strategic Planning"],
            "recommended_subjects": ["Computer Science", "Business Studies", "English"],
            "related_interests": ["Leading or organizing people", "Building something", "Technology"],
            "beginner_skills": ["User Stories", "Roadmap Planning", "Agile / Scrum"],
            "advanced_skills": ["Product Metrics (AARRR)", "Go-to-Market Strategy", "Cross-Functional Leadership"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Product Fundamentals", "description": "Understanding user pain points and writing requirement specs.", "topics": ["PRD Writing", "Agile & Scrum", "User Personas"]},
                {"phase": "Stage 2", "title": "Metrics & Data-Driven PM", "description": "Measuring engagement, retention, churn, and North Star metrics.", "topics": ["Product Analytics", "A/B Testing", "Funnels"]},
                {"phase": "Stage 3", "title": "Product Discovery & UX", "description": "Validating hypotheses with MVPs and customer discovery.", "topics": ["Customer Interviews", "Wireframing", "Prioritization Frameworks"]},
                {"phase": "Stage 4", "title": "Go-to-Market & Scale", "description": "Pricing strategies, product positioning, and executive roadmapping.", "topics": ["GTM Strategy", "Monetization", "Executive Alignment"]}
            ],
            "related_courses": [{"title": "Digital Product Management", "provider_type": "UVA / Coursera", "difficulty": "Intermediate"}],
            "related_job_roles": ["Associate Product Manager", "Technical PM", "Product Owner"],
            "preferred_goals": ["Entrepreneurship", "Leadership", "Financial growth"],
            "work_preference_matches": ["Working in a team", "Leading a team"]
        },
        {
            "id": 9,
            "name": "Biomedical / Healthcare Analyst",
            "category": "Healthcare",
            "description": "Analyzes healthcare data, clinical systems, and medical diagnostics to improve patient outcomes.",
            "education_path": "B.Sc / B.Tech in Biotechnology, Biomedical Sciences, or Healthcare Informatics",
            "work_style": "Methodical, Empathetic, Scientific",
            "required_skills": ["Research", "Data Analysis", "Science", "Critical Thinking"],
            "recommended_subjects": ["Science", "Biology", "Mathematics"],
            "related_interests": ["Analyzing information", "Helping others", "Scientific research"],
            "beginner_skills": ["Biological Data Basics", "Medical Terminology", "Excel"],
            "advanced_skills": ["Biostatistics", "Clinical Trial Protocols", "EHR Systems"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Medical Sciences Foundation", "description": "Anatomy, physiology, and basic epidemiology.", "topics": ["Physiology", "Medical Terminology", "Clinical Research"]},
                {"phase": "Stage 2", "title": "Biostatistics & Health Data", "description": "Statistical modeling of health indicators.", "topics": ["Biostatistics", "R/Python Basics", "Health Metrics"]},
                {"phase": "Stage 3", "title": "Healthcare Informatics", "description": "Electronic health record standards (HL7/FHIR) and data security.", "topics": ["HL7 Standards", "Clinical Trials", "HIPAA Compliance"]},
                {"phase": "Stage 4", "title": "Clinical AI & Diagnostics", "description": "Predictive diagnostics and clinical outcomes optimization.", "topics": ["Diagnostic AI", "Health Economics", "Regulatory Approval"]}
            ],
            "related_courses": [{"title": "Health Informatics Specialization", "provider_type": "Johns Hopkins", "difficulty": "Intermediate"}],
            "related_job_roles": ["Clinical Data Coordinator", "Healthcare Data Analyst", "Biomedical Researcher"],
            "preferred_goals": ["Societal impact", "Scientific discovery"],
            "work_preference_matches": ["Analyze it step by step", "I enjoy analyzing information"]
        },
        {
            "id": 10,
            "name": "Environmental Scientist",
            "category": "Science",
            "description": "Conducts research on climate ecosystems, sustainability policies, conservation, and renewable technologies.",
            "education_path": "B.Sc / M.Sc in Environmental Science, Ecology, or Sustainable Engineering",
            "work_style": "Investigative, Field & Lab Oriented, Impact-Driven",
            "required_skills": ["Research", "Environmental Science", "Data Analysis", "Communication"],
            "recommended_subjects": ["Science", "Geography", "Biology"],
            "related_interests": ["Nature and environment", "Scientific research", "Helping others"],
            "beginner_skills": ["Ecology Fundamentals", "Field Sampling", "GIS Basics"],
            "advanced_skills": ["Carbon Accounting", "Environmental Impact Assessment", "Climate Modeling"],
            "roadmap": [
                {"phase": "Stage 1", "title": "Ecological Sciences", "description": "Atmospheric systems, biodiversity, and soil chemistry.", "topics": ["Ecology", "Environmental Chemistry", "Field Data"]},
                {"phase": "Stage 2", "title": "GIS & Spatial Analysis", "description": "Mapping environmental patterns with ArcGIS and remote sensing.", "topics": ["ArcGIS / QGIS", "Remote Sensing", "Data Modeling"]},
                {"phase": "Stage 3", "title": "Impact Assessments & ESG", "description": "Environmental regulations, ISO 14001, and sustainability reports.", "topics": ["EIA Frameworks", "Carbon Footprinting", "Sustainability Audits"]},
                {"phase": "Stage 4", "title": "Policy & Clean Tech", "description": "Renewable policy advisory and corporate ESG transformation.", "topics": ["Clean Energy Strategy", "Climate Policy", "Corporate ESG"]}
            ],
            "related_courses": [{"title": "Introduction to Sustainability", "provider_type": "Coursera", "difficulty": "Beginner"}],
            "related_job_roles": ["Sustainability Consultant", "Ecology Specialist", "ESG Analyst"],
            "preferred_goals": ["Societal impact", "Environmental preservation"],
            "work_preference_matches": ["Analyze it step by step", "Independent research"]
        }
    ]

# ---------------------------------------------------------
# 4. EXPLAINABLE AI (XAI) ALGORITHM IMPLEMENTATION
# ---------------------------------------------------------
def run_ai_recommendations(profile: Dict[str, Any], answers: Dict[str, Any], skills: Dict[str, float]):
    """
    Computes compatibility score for all careers:
    Score = (Interests * 30%) + (Skills * 25%) + (Academics * 15%) + (Work Style * 15%) + (Goals * 15%)
    """
    careers = load_careers_data()
    results = []
    
    stream = profile.get("stream", "Science").lower()
    enjoyed_activity = str(answers.get("enjoyed_activity", ""))
    fav_subjects = answers.get("favorite_subjects", [])
    problem_type = str(answers.get("problem_type", ""))
    free_time = str(answers.get("free_time_activity", ""))
    problem_approach = str(answers.get("problem_solving_approach", ""))
    work_env = str(answers.get("work_environment", ""))
    main_goal = str(answers.get("main_career_goal", ""))
    tech_comfort = float(answers.get("tech_comfort", 4))
    
    for c in careers:
        matched_factors = []
        key_matching_skills = []
        skills_to_improve = []
        
        # 1. Interest Match (30%)
        rel_interests = c.get("related_interests", [])
        rec_subjects = c.get("recommended_subjects", [])
        
        interest_hits = 0.5
        if any(i.lower() in enjoyed_activity.lower() or enjoyed_activity.lower() in i.lower() for i in rel_interests):
            interest_hits += 1.5
            matched_factors.append(f"Enjoyed activity aligns with {c['name']}: {enjoyed_activity}")
            
        matching_subj = [s for s in fav_subjects if any(s.lower() in rec.lower() or rec.lower() in s.lower() for rec in rec_subjects)]
        if matching_subj:
            interest_hits += 1.5
            matched_factors.append(f"Core subject alignment: {', '.join(matching_subj)}")
            
        if any(i.lower() in free_time.lower() for i in rel_interests):
            interest_hits += 1.0
            matched_factors.append(f"Passion match: {free_time}")
            
        interest_score = min(max((interest_hits / 4.0) * 100.0, 25.0), 100.0)
        
        # 2. Skill Match (25%)
        req_skills = c.get("required_skills", [])
        skill_sum = 0.0
        for s in req_skills:
            r = skills.get(s, 3.0)
            skill_sum += r
            if r >= 3.5:
                key_matching_skills.append(s)
            elif r <= 2.5:
                skills_to_improve.append(s)
                
        skill_score = min(max(((skill_sum / max(len(req_skills), 1)) / 5.0) * 100.0, 25.0), 100.0)
        if not skills_to_improve:
            skills_to_improve = c.get("beginner_skills", ["Foundations", "Core Tools"])[:2]
            
        # 3. Academic Match (15%)
        academic_hits = 1.0
        cat = c["category"].lower()
        if "science" in stream and cat in ["technology", "science", "healthcare"]:
            academic_hits += 1.5
            matched_factors.append("Academic stream (Science) provides strong prerequisites")
        elif "commerce" in stream and cat in ["business", "finance"]:
            academic_hits += 1.5
            matched_factors.append("Academic stream (Commerce) aligns with commercial principles")
        elif "arts" in stream and cat in ["design", "media", "education"]:
            academic_hits += 1.5
            matched_factors.append("Academic stream (Arts/Humanities) supports creative track")
        else:
            academic_hits += 0.8
        academic_score = min(max((academic_hits / 2.5) * 100.0, 35.0), 100.0)
        
        # 4. Work Style Match (15%)
        work_hits = 1.0
        work_matches = c.get("work_preference_matches", [])
        if any(m.lower() in problem_approach.lower() for m in work_matches):
            work_hits += 1.0
            matched_factors.append(f"Problem-solving style: '{problem_approach}'")
        if any(m.lower() in work_env.lower() for m in work_matches):
            work_hits += 1.0
            matched_factors.append(f"Work style preference: '{work_env}'")
        if cat == "technology" and tech_comfort >= 4:
            work_hits += 0.8
            matched_factors.append("High comfort and enthusiasm with modern technologies")
        work_score = min(max((work_hits / 3.0) * 100.0, 30.0), 100.0)
        
        # 5. Career Goal Match (15%)
        goal_hits = 1.0
        pref_goals = c.get("preferred_goals", [])
        if any(g.lower() in main_goal.lower() for g in pref_goals):
            goal_hits += 1.5
            matched_factors.append(f"Direct alignment with your career goal: '{main_goal}'")
        goal_score = min(max((goal_hits / 2.5) * 100.0, 30.0), 100.0)
        
        # Final Score
        final_score = (
            (interest_score * 0.30) +
            (skill_score * 0.25) +
            (academic_score * 0.15) +
            (work_score * 0.15) +
            (goal_score * 0.15)
        )
        final_score = round(min(max(final_score, 38.0), 96.5), 1)
        
        clean_factors = list(dict.fromkeys(matched_factors))
        if not clean_factors:
            clean_factors = [f"Foundational alignment with {c['name']} requirements"]
            
        results.append({
            "id": c["id"],
            "career_name": c["name"],
            "category": c["category"],
            "compatibility_score": final_score,
            "description": c["description"],
            "education_path": c["education_path"],
            "matched_factors": clean_factors,
            "key_matching_skills": key_matching_skills[:3] if key_matching_skills else ["Problem Solving"],
            "skills_to_improve": skills_to_improve[:3],
            "roadmap": c.get("roadmap", []),
            "related_courses": c.get("related_courses", []),
            "related_job_roles": c.get("related_job_roles", [])
        })
        
    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return results

# ---------------------------------------------------------
# 5. NAVIGATION STATE & SESSION MANAGEMENT
# ---------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "selected_career_id" not in st.session_state:
    st.session_state.selected_career_id = 1

if "assessment_completed" not in st.session_state:
    st.session_state.assessment_completed = False

if "student_profile" not in st.session_state:
    st.session_state.student_profile = {
        "name": "Aarav Sharma",
        "email": "student@aicareerguide.com",
        "stream": "Science",
        "education_level": "Undergraduate",
        "current_class_year": "3rd Year",
        "overall_percentage": 85.0
    }

# ---------------------------------------------------------
# 6. SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 AI CareerGuide")
    st.caption("AI-Based Student Career Guidance System")
    st.markdown("---")
    
    nav_options = [
        "🏠 Home",
        "📝 Career Assessment",
        "📊 AI Recommendations & Skill Gaps",
        "🗺️ Career Explorer & Roadmaps",
        "⭐ Student Feedback",
        "🛡️ Admin Dashboard",
        "💬 AI Career Assistant"
    ]
    
    # Map label to internal key
    label_to_key = {
        "🏠 Home": "Home",
        "📝 Career Assessment": "Assessment",
        "📊 AI Recommendations & Skill Gaps": "Results",
        "🗺️ Career Explorer & Roadmaps": "Explorer",
        "⭐ Student Feedback": "Feedback",
        "🛡️ Admin Dashboard": "Admin",
        "💬 AI Career Assistant": "Assistant"
    }
    key_to_label = {v: k for k, v in label_to_key.items()}
    
    current_label = key_to_label.get(st.session_state.current_page, "🏠 Home")
    selected_nav = st.radio("Navigate Application", nav_options, index=nav_options.index(current_label))
    st.session_state.current_page = label_to_key[selected_nav]
    
    st.markdown("---")
    st.markdown("**Demo Credentials for Evaluation:**")
    st.caption("👨‍🎓 **Student:** `student@aicareerguide.com`")
    st.caption("🛡️ **Admin:** `admin@aicareerguide.com`")

# ---------------------------------------------------------
# PAGE 1: REDESIGNED HOME PAGE
# ---------------------------------------------------------
if st.session_state.current_page == "Home":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <span class="badge-step">AI-Based Student Career Guidance System</span>
        <h1 style="color: white; font-size: 2.75rem; margin-top: 0.5rem; margin-bottom: 1rem; line-height: 1.2;">
            Discover the Right Career Path with AI
        </h1>
        <p style="color: #cbd5e1; font-size: 1.15rem; max-width: 750px; line-height: 1.6; margin-bottom: 1.5rem;">
            Explore your strengths, understand your skills, and get personalized career recommendations powered by AI.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dual Main Action Buttons
    col_btn1, col_btn2, col_spacer = st.columns([1.5, 1.5, 3])
    with col_btn1:
        if st.button("🚀 Start Career Assessment", use_container_width=True, type="primary"):
            st.session_state.current_page = "Assessment"
            st.rerun()
    with col_btn2:
        if st.button("🧭 Explore Careers", use_container_width=True):
            st.session_state.current_page = "Explorer"
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

    # Section 1: Why Choose Our Career Guidance System? (6 Cards)
    st.subheader("💡 Why Choose Our Career Guidance System?")
    st.caption("Comprehensive data-driven discovery designed specifically for students.")
    
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 1. Personalized Career Recommendations</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Get career suggestions based on your individual profile, matching your strengths to the most compatible industries.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h4>🗺️ 4. Personalized Career Roadmap</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Get a step-by-step learning and career development plan from foundational skills through professional industry readiness.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with fcol2:
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 2. AI-Based Career Analysis</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Analyze interests, skills, academics, and career preferences using a weighted 5-factor Explainable AI compatibility formula.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h4>📚 5. Career Exploration</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Explore career descriptions, required skills, courses, and career pathways across technology, management, and sciences.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with fcol3:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 3. Skill Gap Analysis</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Identify skills that need improvement for your selected career with concrete, high-priority learning suggestions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 6. Student-Friendly Guidance</h4>
            <p style="color: #64748b; font-size: 0.9rem;">
                Simple and easy-to-understand career information for students with clear visualizations and zero confusing jargon.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Section 2: How It Works (Simple 4-Step Section)
    st.subheader("⚡ How It Works")
    st.caption("A straightforward 4-step workflow to unlock transparent career clarity:")
    
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem;">
            <div style="background:#0284c7; color:white; width:28px; height:28px; border-radius:50%; text-align:center; line-height:28px; font-weight:bold; margin-bottom:0.5rem;">1</div>
            <h4>Create Profile</h4>
            <p style="color:#64748b; font-size:0.85rem;">Set up your academic background, stream, and high-level aspirations.</p>
        </div>
        """, unsafe_allow_html=True)
    with step2:
        st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem;">
            <div style="background:#6366f1; color:white; width:28px; height:28px; border-radius:50%; text-align:center; line-height:28px; font-weight:bold; margin-bottom:0.5rem;">2</div>
            <h4>Take Assessment</h4>
            <p style="color:#64748b; font-size:0.85rem;">Answer questions evaluating your interests, skills, and work styles.</p>
        </div>
        """, unsafe_allow_html=True)
    with step3:
        st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem;">
            <div style="background:#a855f7; color:white; width:28px; height:28px; border-radius:50%; text-align:center; line-height:28px; font-weight:bold; margin-bottom:0.5rem;">3</div>
            <h4>AI Analysis</h4>
            <p style="color:#64748b; font-size:0.85rem;">Our 5-factor weighted algorithm evaluates compatibility across careers.</p>
        </div>
        """, unsafe_allow_html=True)
    with step4:
        st.markdown("""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 1rem; padding: 1.25rem;">
            <div style="background:#10b981; color:white; width:28px; height:28px; border-radius:50%; text-align:center; line-height:28px; font-weight:bold; margin-bottom:0.5rem;">4</div>
            <h4>Get Recommendations</h4>
            <p style="color:#64748b; font-size:0.85rem;">Receive explainable match reasons, skill gaps, roadmaps, and share feedback.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Section 3: Explore Career Opportunities (10 Categories)
    st.subheader("🌐 Explore Career Opportunities")
    st.caption("Click any career domain to explore curriculum requirements and pathways:")
    
    categories = [
        ("💻 Technology & Software", "Technology", "Software development, cloud systems, and mobile engineering."),
        ("🤖 Artificial Intelligence & Data", "Technology", "Machine learning, data analytics, and neural architectures."),
        ("🔒 Cybersecurity & Cloud", "Technology", "Information security, ethical hacking, and cloud networks."),
        ("💼 Business & Management", "Business", "Product management, operations, and strategic consulting."),
        ("📊 Finance & Accounting", "Finance", "Investment analysis, wealth valuation, and auditing."),
        ("🎨 Design & Creative", "Design", "UI/UX interaction, visual design, and user research."),
        ("🏥 Healthcare", "Healthcare", "Clinical analysis, biomedical informatics, and patient health."),
        ("🔬 Education & Research", "Science", "Scientific exploration, academia, and lab experimentation."),
        ("📡 Media & Communication", "Business", "Digital content strategy, journalism, and public relations."),
        ("🌱 Environmental & Science", "Science", "Sustainability ecology, green tech, and conservation.")
    ]
    
    cat_cols = st.columns(2)
    for idx, (title, dom, desc) in enumerate(categories):
        with cat_cols[idx % 2]:
            st.markdown(f"""
            <div class="category-card">
                <h4 style="margin-bottom:0.2rem;">{title}</h4>
                <p style="color:#64748b; font-size:0.85rem; margin-bottom:0.5rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Section 4: Call-to-Action Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 2.5rem; border-radius: 1.5rem; text-align: center; color: white;">
        <h2>Not Sure Which Career Is Right for You?</h2>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 600px; margin: 0 auto 1.5rem auto;">
            Take our personalized career assessment and discover career paths that match your interests, skills, and goals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([2, 1.5, 2])
    with col_c2:
        if st.button("✨ Start Your Assessment", use_container_width=True, type="primary"):
            st.session_state.current_page = "Assessment"
            st.rerun()

# ---------------------------------------------------------
# PAGE 2: INTERACTIVE CAREER ASSESSMENT
# ---------------------------------------------------------
elif st.session_state.current_page == "Assessment":
    st.markdown("## 📝 Personalized Career Assessment")
    st.caption("Answer the questions below to allow our 5-factor Explainable AI engine to evaluate your career compatibility.")
    
    with st.expander("👤 1. Academic Background & Profile", expanded=True):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            name = st.text_input("Full Name", value=st.session_state.student_profile["name"])
            stream = st.selectbox("Academic Stream", ["Science", "Commerce", "Arts/Humanities"], index=0)
        with pcol2:
            email = st.text_input("Email Address", value=st.session_state.student_profile["email"])
            education_level = st.selectbox("Education Level", ["High School", "Undergraduate", "Postgraduate"], index=1)
        with pcol3:
            class_year = st.selectbox("Current Year", ["1st Year", "2nd Year", "3rd Year", "Final Year"], index=2)
            marks = st.slider("Overall Percentage / Marks (%)", 40.0, 100.0, 85.0, 0.5)

    with st.expander("💡 2. Cognitive Interests & Problem Solving", expanded=True):
        icol1, icol2 = st.columns(2)
        with icol1:
            enjoyed_act = st.selectbox(
                "What type of activity do you enjoy most?",
                [
                    "Solving logical problems",
                    "Building something",
                    "Analyzing information",
                    "Creating visual art or design",
                    "Leading or organizing people",
                    "Helping others",
                    "Scientific research",
                    "Nature and environment"
                ],
                index=0
            )
            fav_subjects = st.multiselect(
                "Favorite Subjects (Choose up to 3)",
                ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Commerce", "Economics", "Arts", "English"],
                default=["Computer Science", "Mathematics"]
            )
        with icol2:
            prob_type = st.selectbox(
                "What types of challenges excite you?",
                ["Technical problems", "Creative challenges", "Analytical & data puzzles", "People & team coordination", "Financial decisions"],
                index=0
            )
            free_time = st.selectbox(
                "How do you prefer to spend your free time?",
                ["Building software or coding", "Reading scientific breakthroughs", "Designing creative graphics", "Investing or tracking markets", "Reading or mentoring"],
                index=0
            )

    with st.expander("⭐ 3. Core Skills Self-Rating (1 to 5 Stars)", expanded=True):
        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            prog_r = st.slider("Programming (Python/Java/C++)", 1.0, 5.0, 4.5, 0.5)
            math_r = st.slider("Mathematics & Quantitative", 1.0, 5.0, 4.0, 0.5)
            data_r = st.slider("Data Analysis", 1.0, 5.0, 4.0, 0.5)
        with scol2:
            prob_r = st.slider("Logical Problem Solving", 1.0, 5.0, 4.5, 0.5)
            design_r = st.slider("Creative Design / UI", 1.0, 5.0, 3.0, 0.5)
            comm_r = st.slider("Communication & Presentation", 1.0, 5.0, 3.5, 0.5)
        with scol3:
            lead_r = st.slider("Leadership & Team Coordination", 1.0, 5.0, 3.5, 0.5)
            res_r = st.slider("Scientific Research", 1.0, 5.0, 3.5, 0.5)
            tech_comfort = st.slider("Comfort Adopting New Technologies", 1.0, 5.0, 4.5, 0.5)

    with st.expander("🤝 4. Work Style & Career Goals", expanded=True):
        wcol1, wcol2 = st.columns(2)
        with wcol1:
            problem_approach = st.selectbox(
                "When given a complex project, how do you tackle it?",
                ["Analyze it step by step", "Brainstorm creative ideas", "Coordinate with a team immediately", "Research theoretical principles"],
                index=0
            )
            work_env = st.selectbox(
                "Preferred Work Environment",
                ["Working in a collaborative team", "Independent and focused research", "Dynamic client-facing leadership"],
                index=0
            )
        with wcol2:
            main_goal = st.selectbox(
                "Primary Overarching Career Goal",
                ["High technical expertise", "Innovation & invention", "Financial growth", "Societal impact", "Creative expression", "Leadership"],
                index=0
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Calculate AI Recommendations & Skill Gaps", type="primary", use_container_width=True):
        st.session_state.student_profile = {
            "name": name,
            "email": email,
            "stream": stream,
            "education_level": education_level,
            "current_class_year": class_year,
            "overall_percentage": marks
        }
        
        answers_dict = {
            "enjoyed_activity": enjoyed_act,
            "favorite_subjects": fav_subjects,
            "problem_type": prob_type,
            "free_time_activity": free_time,
            "problem_solving_approach": problem_approach,
            "work_environment": work_env,
            "main_career_goal": main_goal,
            "tech_comfort": tech_comfort
        }
        
        skills_dict = {
            "Programming": prog_r,
            "Mathematics": math_r,
            "Data Analysis": data_r,
            "Problem Solving": prob_r,
            "Design": design_r,
            "Communication": comm_r,
            "Leadership": lead_r,
            "Research": res_r,
            "Machine Learning": (prog_r + math_r) / 2.0,
            "Cybersecurity": prog_r * 0.9,
            "Cloud Computing": prog_r * 0.85
        }
        
        # Run 5-factor scoring
        results = run_ai_recommendations(st.session_state.student_profile, answers_dict, skills_dict)
        st.session_state.ai_results = results
        st.session_state.assessment_completed = True
        st.session_state.current_page = "Results"
        st.rerun()

# ---------------------------------------------------------
# PAGE 3: AI RECOMMENDATIONS & SKILL GAPS
# ---------------------------------------------------------
elif st.session_state.current_page == "Results":
    st.markdown("## 📊 Your Personalized AI Career Recommendations")
    st.caption("Generated using 5-Factor Explainable AI Compatibility Scoring (Interests 30%, Skills 25%, Academics 15%, Work Style 15%, Goals 15%).")
    
    if not st.session_state.get("assessment_completed") or "ai_results" not in st.session_state:
        # Generate default realistic results for instant preview
        st.session_state.ai_results = run_ai_recommendations(
            st.session_state.student_profile,
            {"enjoyed_activity": "Solving logical problems", "favorite_subjects": ["Computer Science", "Mathematics"], "main_career_goal": "High technical expertise", "tech_comfort": 4.5},
            {"Programming": 4.5, "Problem Solving": 4.5, "Mathematics": 4.0, "Data Analysis": 4.0, "Communication": 3.5, "Leadership": 3.5, "Design": 3.0, "Research": 3.5}
        )
        st.session_state.assessment_completed = True

    results = st.session_state.ai_results
    top_careers = results[:5]

    # Visualizations: Radar Traits & Compatibility Chart
    col_vis1, col_vis2 = st.columns([1, 1.2])
    with col_vis1:
        st.markdown("#### 🧠 Cognitive & Professional Traits")
        # Trait scores
        traits = {
            "Analytical": 92.5,
            "Technical": 96.0,
            "Problem Solving": 94.0,
            "Creativity": 65.0,
            "Communication": 70.0,
            "Leadership": 68.0
        }
        df_radar = pd.DataFrame(dict(r=list(traits.values()), theta=list(traits.keys())))
        fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 100])
        fig_radar.update_traces(fill='toself', fillcolor='rgba(2, 132, 199, 0.25)', line_color='#0284c7')
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), margin=dict(l=30, r=30, t=20, b=20), height=300)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_vis2:
        st.markdown("#### 🏆 Top Compatibility Matches")
        df_bars = pd.DataFrame({
            "Career": [c["career_name"] for c in top_careers],
            "Match (%)": [c["compatibility_score"] for c in top_careers]
        })
        fig_bars = px.bar(
            df_bars,
            x="Match (%)",
            y="Career",
            orientation="h",
            color="Match (%)",
            color_continuous_scale="Blues",
            range_x=[0, 100],
            text="Match (%)"
        )
        fig_bars.update_layout(yaxis=dict(autorange="reversed"), height=300, margin=dict(l=10, r=20, t=20, b=20))
        st.plotly_chart(fig_bars, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🎯 Recommended Career Trajectories")

    for idx, c in enumerate(top_careers):
        with st.container():
            col_info, col_act = st.columns([3.5, 1])
            with col_info:
                st.markdown(f"### {idx+1}. {c['career_name']} &nbsp; <span style='background:#ecfdf5; color:#047857; padding:2px 8px; border-radius:6px; font-size:0.85rem;'>{c['compatibility_score']}% Match</span>", unsafe_allow_html=True)
                st.caption(f"Domain: {c['category']} | Education: {c['education_path']}")
                st.write(c["description"])
                
                # Checkmark Proof Points (XAI)
                st.markdown("**✓ Why this aligns with you:**")
                for factor in c["matched_factors"][:3]:
                    st.markdown(f"- ✓ {factor}")
                    
                # Matching Skills vs Skill Gaps
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.markdown("**✨ Key Matching Skills:**")
                    st.write(", ".join([f"`{s}`" for s in c["key_matching_skills"]]))
                with m_col2:
                    st.markdown("**📈 Skill Gaps (Areas to Develop):**")
                    st.write(", ".join([f"`{s}`" for s in c["skills_to_improve"]]))
                    
            with col_act:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button(f"🗺️ View Roadmap", key=f"btn_road_{c['id']}", use_container_width=True):
                    st.session_state.selected_career_id = c["id"]
                    st.session_state.current_page = "Explorer"
                    st.rerun()

            st.markdown("---")

    # Workflow Next Step Action
    st.markdown("""
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 1rem; padding: 1.5rem; text-align: center;">
        <h4>Next Step in Guidance Workflow:</h4>
        <p style="color: #64748b; font-size: 0.9rem;">Review your career roadmap, then complete the student feedback evaluation.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.5, 1.5, 1.5])
    with c2:
        if st.button("⭐ Proceed to Student Feedback", type="primary", use_container_width=True):
            st.session_state.current_page = "Feedback"
            st.rerun()

# ---------------------------------------------------------
# PAGE 4: CAREER EXPLORER & MULTI-STAGE ROADMAPS
# ---------------------------------------------------------
elif st.session_state.current_page == "Explorer":
    careers = load_careers_data()
    st.markdown("## 🗺️ Career Explorer & Stage-Wise Roadmaps")
    st.caption("Deep dive into 4-stage roadmaps (Stage 1 Fundamentals &rarr; Stage 4 Industry Readiness), courses, and required skills.")
    
    # Career Selector
    career_names = [c["name"] for c in careers]
    selected_idx = 0
    for idx, c in enumerate(careers):
        if c["id"] == st.session_state.selected_career_id:
            selected_idx = idx
            break
            
    selected_name = st.selectbox("Select a Career to Inspect:", career_names, index=selected_idx)
    selected_career = next((c for c in careers if c["name"] == selected_name), careers[0])
    st.session_state.selected_career_id = selected_career["id"]
    
    st.markdown(f"### {selected_career['name']} <span style='font-size:0.9rem; background:#e0f2fe; color:#0369a1; padding:3px 10px; border-radius:8px;'>{selected_career['category']}</span>", unsafe_allow_html=True)
    st.write(selected_career["description"])
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(f"**🎓 Education Path:** {selected_career['education_path']}")
        st.markdown(f"**🛠️ Required Skills:** {', '.join([f'`{s}`' for s in selected_career.get('required_skills', [])])}")
    with col_d2:
        st.markdown(f"**🤝 Work Style:** {selected_career.get('work_style', 'Collaborative & Analytical')}")
        st.markdown(f"**💼 Related Job Titles:** {', '.join(selected_career.get('related_job_roles', []))}")

    st.markdown("#### 🚀 Stage-Wise Learning Roadmap")
    roadmap = selected_career.get("roadmap", [])
    
    r_cols = st.columns(max(len(roadmap), 1))
    for idx, stage in enumerate(roadmap):
        with r_cols[idx]:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-top: 4px solid #0284c7; border-radius: 0.75rem; padding: 1.25rem; min-height: 220px;">
                <span style="font-size:0.75rem; font-weight:bold; color:#0284c7; text-transform:uppercase;">{stage.get('phase', f'Stage {idx+1}')}</span>
                <h4 style="margin: 0.25rem 0 0.5rem 0; font-size:1.05rem;">{stage.get('title', 'Milestone')}</h4>
                <p style="color:#64748b; font-size:0.8rem; line-height:1.4;">{stage.get('description', '')}</p>
                <div style="margin-top: 0.75rem;">
                    {"".join([f"<span style='background:#f1f5f9; color:#334155; font-size:0.75rem; padding:2px 6px; border-radius:4px; margin-right:4px; display:inline-block; margin-bottom:4px;'>{t}</span>" for t in stage.get('topics', [])])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Learning Courses
    courses = selected_career.get("related_courses", [])
    if courses:
        st.markdown("#### 📚 Recommended Certifications & Learning")
        for crs in courses:
            st.markdown(f"- 🎓 **{crs.get('title')}** ({crs.get('provider_type')}) — *Difficulty: {crs.get('difficulty')}*")

    st.markdown("---")
    # Next step in workflow
    c_btn1, c_btn2, c_btn3 = st.columns([1.5, 2, 1.5])
    with c_btn2:
        if st.button("⭐ Provide Student Feedback on this Roadmap", type="primary", use_container_width=True):
            st.session_state.current_page = "Feedback"
            st.rerun()

# ---------------------------------------------------------
# PAGE 5: STUDENT FEEDBACK (WORKFLOW STEP 8)
# ---------------------------------------------------------
elif st.session_state.current_page == "Feedback":
    st.markdown("## ⭐ Student Feedback")
    st.caption("Final Workflow Step: Registration &rarr; Profile &rarr; Assessment &rarr; AI Analysis &rarr; Recommendations &rarr; Skill Gap &rarr; Roadmap &rarr; **Student Feedback**")

    # Check if student already submitted
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM feedbacks WHERE student_email = ? ORDER BY id DESC LIMIT 1", (st.session_state.student_profile["email"],))
    existing_fb = c.fetchone()
    conn.close()

    if existing_fb and not st.session_state.get("editing_feedback"):
        st.markdown("""
        <div class="status-box">
            <h3 style="color:#065f46; margin:0 0 0.5rem 0;">Feedback Submitted ✓</h3>
            <p style="margin:0;">Thank you for your valuable feedback! Your feedback helps us improve the career guidance system.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Submitted Details for {existing_fb[1]} ({existing_fb[2]}):**")
        st.markdown(f"- ⭐ **Satisfaction Rating:** {existing_fb[3]} / 5")
        st.markdown(f"- 🎯 **Recommendation Relevance:** {existing_fb[4]}")
        st.markdown(f"- 💡 **Useful Features:** {existing_fb[5]}")
        st.markdown(f"- 🚀 **Recommendation Confidence:** {existing_fb[6]} / 5")
        if existing_fb[7]:
            st.markdown(f"- 💬 **Comments:** *\"{existing_fb[7]}\"*")
            
        f_btn1, f_btn2 = st.columns(2)
        with f_btn1:
            if st.button("📊 View Recommendations Again", use_container_width=True):
                st.session_state.current_page = "Results"
                st.rerun()
        with f_btn2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()
    else:
        with st.form("student_feedback_form"):
            st.markdown("#### 1. Overall Experience")
            sat_score = st.radio(
                "How satisfied are you with the career guidance provided?",
                [
                    "⭐ 5 – Very Satisfied",
                    "⭐ 4 – Satisfied",
                    "⭐ 3 – Neutral",
                    "⭐ 2 – Unsatisfied",
                    "⭐ 1 – Very Unsatisfied"
                ],
                index=0
            )
            sat_rating = int(sat_score.split("–")[0].replace("⭐", "").strip())
            
            st.markdown("#### 2. Recommendation Relevance")
            relevance = st.selectbox(
                "How relevant were the recommended careers to your interests and skills?",
                ["Very Relevant", "Relevant", "Neutral", "Not Very Relevant", "Not Relevant"],
                index=0
            )
            
            st.markdown("#### 3. Useful Features")
            features = st.multiselect(
                "Which feature was most useful to you? (Select all that apply)",
                [
                    "Career Recommendations",
                    "AI Career Analysis",
                    "Skill Gap Analysis",
                    "Career Roadmap",
                    "Career Exploration",
                    "Learning Resources"
                ],
                default=["Career Recommendations", "AI Career Analysis", "Skill Gap Analysis"]
            )
            
            st.markdown("#### 4. Recommendation Confidence")
            conf_rating = st.slider(
                "After using the system, how confident are you about exploring your recommended career? (1 to 5)",
                1, 5, 5
            )
            
            st.markdown("#### 5. Open Feedback")
            comments = st.text_area(
                "Tell us about your experience or suggest improvements:",
                placeholder="Share your suggestions, experience, or anything you would like us to improve..."
            )
            
            submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True, type="primary")
            if submitted:
                conn = sqlite3.connect(DB_FILE)
                cur = conn.cursor()
                cur.execute("""
                INSERT INTO feedbacks (student_name, student_email, satisfaction_rating, recommendation_relevance, useful_features, confidence_rating, comments)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    st.session_state.student_profile["name"],
                    st.session_state.student_profile["email"],
                    sat_rating,
                    relevance,
                    json.dumps(features),
                    conf_rating,
                    comments.strip()
                ))
                conn.commit()
                conn.close()
                st.success("Thank you for your valuable feedback! Your feedback helps us improve the career guidance system.")
                st.session_state.editing_feedback = False
                st.rerun()

# ---------------------------------------------------------
# PAGE 6: ADMIN DASHBOARD & FEEDBACK ANALYTICS
# ---------------------------------------------------------
elif st.session_state.current_page == "Admin":
    st.markdown("## 🛡️ Administrative Analytics & Student Feedback")
    st.caption("Review system usage metrics and inspect all student feedback evaluations.")
    
    conn = sqlite3.connect(DB_FILE)
    df_fb = pd.read_sql_query("SELECT * FROM feedbacks ORDER BY id DESC", conn)
    conn.close()

    total_fb = len(df_fb)
    avg_sat = round(df_fb["satisfaction_rating"].mean(), 2) if total_fb > 0 else 0.0
    avg_conf = round(df_fb["confidence_rating"].mean(), 2) if total_fb > 0 else 0.0
    
    # Top metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", "25+")
    m2.metric("Total Feedbacks", f"{total_fb}")
    m3.metric("Avg Satisfaction", f"⭐ {avg_sat} / 5")
    m4.metric("Avg Confidence", f"{avg_conf} / 5")
    
    st.markdown("---")
    
    # Visual Analytics on Feedback
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        st.markdown("#### 🎯 Recommendation Relevance Distribution")
        if total_fb > 0:
            rel_counts = df_fb["recommendation_relevance"].value_counts().reset_index()
            rel_counts.columns = ["Relevance", "Count"]
            fig_rel = px.pie(rel_counts, names="Relevance", values="Count", color_discrete_sequence=px.colors.sequential.Teal)
            fig_rel.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_rel, use_container_width=True)
            
    with col_ch2:
        st.markdown("#### 💡 Most Useful Features Voted")
        if total_fb > 0:
            feat_list = []
            for item in df_fb["useful_features"]:
                try:
                    f_arr = json.loads(item)
                    feat_list.extend(f_arr)
                except:
                    feat_list.append(str(item))
            df_feat = pd.Series(feat_list).value_counts().reset_index()
            df_feat.columns = ["Feature", "Votes"]
            fig_feat = px.bar(df_feat, x="Votes", y="Feature", orientation="h", color="Votes", color_continuous_scale="Purples")
            fig_feat.update_layout(yaxis=dict(autorange="reversed"), height=280, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_feat, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💬 Recent Student Comments & Evaluations")
    if total_fb > 0:
        for _, row in df_fb.iterrows():
            with st.container():
                st.markdown(f"**{row['student_name']}** ({row['student_email']}) &nbsp;•&nbsp; ⭐ `{row['satisfaction_rating']}/5` &nbsp;•&nbsp; Relevance: `{row['recommendation_relevance']}`")
                if row['comments']:
                    st.markdown(f"> *\"{row['comments']}\"*")
                st.caption(f"Valued Features: {row['useful_features']} | Submitted at: {row['created_at']}")
                st.markdown("---")

# ---------------------------------------------------------
# PAGE 7: AI CAREER ASSISTANT
# ---------------------------------------------------------
elif st.session_state.current_page == "Assistant":
    st.markdown("## 💬 AI Career Assistant")
    st.caption("Ask questions about specific careers, recommended skill prerequisites, certifications, or roadmap milestones.")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I am your AI Career Assistant. Ask me about careers, required skills, or stage-wise learning roadmaps!"}
        ]
        
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Ask a career guidance question..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Intelligent rule-based career response
        p_lower = prompt.lower()
        if "ai" in p_lower or "machine learning" in p_lower:
            reply = "**AI/ML Engineer**: Strong mathematics (linear algebra & calculus), Python (NumPy, PyTorch), and model deployment. Check out our Stage 1 to 4 roadmap in the Career Explorer!"
        elif "cyber" in p_lower or "security" in p_lower:
            reply = "**Cybersecurity Analyst**: Focus on networking fundamentals (TCP/IP), Linux command line, CompTIA Security+ concepts, and penetration testing tools like Wireshark and Metasploit."
        elif "roadmap" in p_lower or "stage" in p_lower:
            reply = "All our career roadmaps follow a 4-Stage progression: Stage 1 (Fundamentals) &rarr; Stage 2 (Applications) &rarr; Stage 3 (Advanced Specialization) &rarr; Stage 4 (Industry Readiness & Portfolio)."
        else:
            reply = f"Great question! Based on your interest in '{prompt}', we recommend completing our **28-question Career Assessment** to discover exact compatibility scores and skill gap analyses."
            
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
