📋
Hiring Intelligence Platform - Complete Documentation
README.md
Hiring Intelligence Platform
A hiring decision system that reads resumes and job descriptions as data, not documents.

Vision Statement
This platform transforms the hiring process by extracting structured intelligence from resumes and job descriptions, then producing clear, explainable match scores. Unlike traditional job portals that rely on keyword matching and manual data entry, this system understands context, evaluates evidence, and provides actionable feedback to both candidates and recruiters.

Table of Contents
Project Overview
The Problem We're Solving
Core Solution Approach
Key Features
User Journeys
Technology Stack
System Capabilities
Getting Started Guide
API Overview
Data Structure Examples
Testing Strategy
Security & Compliance
Contributing Guidelines
Project Differentiators
1. Project Overview
The Hiring Intelligence Platform is designed to bring clarity, fairness, and efficiency to the recruitment process. It serves three user types:

Candidates receive automatic skill extraction from resumes, transparent match scores for jobs, and constructive feedback on gaps.

Recruiters get ranked applicants with evidence-based reasoning, quality-checked job descriptions, and insights into hiring bottlenecks.

Admins monitor system health, track hiring metrics, and ensure compliance through comprehensive audit logs.

What Makes This Different
This is not a job board clone. Traditional platforms focus on volume and basic filtering. This platform focuses on:

Understanding over keywords: Context matters more than exact matches
Explanation over automation: Every decision comes with clear reasoning
Learning over rejection: Candidates get actionable improvement suggestions
Evidence over claims: Skills are validated through projects and experience
2. The Problem We're Solving
Current Pain Points in Hiring
For Candidates:

Manual skill selection after uploading resumes (redundant and error-prone)
No feedback on rejections (silence instead of learning)
Projects and education treated as plain text (valuable context ignored)
Same evaluation criteria for freshers and experienced professionals (unfair comparison)
Keyword guessing games (gaming the system instead of showcasing real skills)
For Recruiters:

Overwhelming volumes of unranked applications
No quality checks on job descriptions (unrealistic requirements slip through)
Limited insight into why candidates match or don't match
Difficulty understanding skill acquisition (project work vs. professional experience)
No visibility into recruitment funnel bottlenecks
For the Hiring Ecosystem:

Lack of transparency breeds distrust
Inefficient processes waste everyone's time
Talent gets overlooked due to poor matching
No continuous improvement feedback loop
3. Core Solution Approach
Treating Documents as Data
The platform transforms unstructured documents into structured, queryable data:

Resume Processing:

Extract skills with evidence (where and how each skill was used)
Identify projects with technologies and outcomes
Capture education with institutions and timelines
Quantify experience duration for each skill
Normalize skill names to handle synonyms
Job Description Analysis:

Separate required skills from preferred skills
Extract realistic experience ranges
Identify red flags (missing salary, unrealistic combinations)
Assign quality scores to job postings
Validate requirement feasibility
Intelligent Matching:

Use transparent, deterministic scoring logic
Weight factors based on role level (entry vs. senior)
Provide detailed breakdowns for every score
Generate human-readable explanations
Show evidence for each matching element
4. Key Features
Core Functionality
Multi-Role Account System
Candidate accounts with resume management
Recruiter accounts with job posting and applicant tracking
Admin accounts with system monitoring and analytics
Role-based access control and permissions
Intelligent Resume Processing
PDF upload with automatic text extraction using PyMuPDF
Asynchronous parsing via Celery workers
LLM-powered structured data extraction using Groq API
Ollama fallback for offline development and testing
Skill normalization against canonical skill database
Evidence tagging for each extracted skill
Job Description Intelligence
Automatic requirement extraction and categorization
Quality scoring for job postings
Red flag detection (missing information, unrealistic demands)
Skill requirement validation
Experience level appropriateness checking
Explainable Matching Engine
Transparent scoring algorithm with defined weights
Role-level adjusted matching (entry level vs. senior)
Evidence-based skill validation
Detailed score breakdowns
Human-readable explanations for every match
Streamlined Application Flow
One-click apply (no redundant data entry)
Automatic match score display before applying
Application status tracking
Feedback collection on rejections
Candidate Dashboard
Personalized job matches sorted by score
Gap analysis for each position
Improvement suggestions
Application history and status
Match explanation details
Recruiter Dashboard
Ranked applicant lists with evidence
Filtering by required skills and experience
Skill acquisition context (project vs. professional)
Application management workflow
Hiring funnel analytics
Asynchronous Processing Architecture
Redis-backed task queue
Celery workers for heavy computation
Non-blocking user experience
Scalable task distribution
Progress tracking and status updates
Comprehensive Audit Logging
All matching decisions logged with reasoning
LLM input and output tracking
User action history
Compliance and explainability support
System event timeline
5. User Journeys
Candidate Journey
Step 1: Registration and Profile Setup

Create account with basic information
Receive confirmation and onboarding guidance
Step 2: Resume Upload

Upload PDF resume (single action, no forms)
System queues parsing task
Receive notification when parsing completes
Step 3: Review Parsed Profile

View extracted skills with evidence
See identified projects and technologies
Verify education and experience timeline
Make corrections if needed (future enhancement)
Step 4: Browse Jobs with Intelligence

View job listings with personalized match scores
See score breakdown before applying
Understand gaps and strengths for each position
Filter by match score, required skills, or experience level
Step 5: Apply with Context

Click apply (no forms to fill)
Application includes resume, match score, and evidence
Receive confirmation with next steps
Step 6: Learn from Outcomes

Track application status in dashboard
Receive constructive feedback on rejections
Get specific improvement suggestions
Understand skill gaps for desired roles
Recruiter Journey
Step 1: Create Recruiter Account

Register as recruiter with company information
Set up profile and preferences
Step 2: Post Job Opening

Input job description (paste or type)
System analyzes and extracts requirements
Review quality score and detected red flags
Refine description based on suggestions
Publish job to platform
Step 3: Receive and Review Applications

See applications in ranked order by match score
View detailed candidate profiles with evidence
Understand skill sources (projects, education, work)
Filter by required qualifications
Step 4: Make Informed Decisions

Review match explanations for each candidate
Compare candidates with standardized metrics
Move candidates through pipeline stages
Provide rejection feedback for system learning
Step 5: Analyze Hiring Metrics

View application funnel statistics
Identify requirement bottlenecks
Track time-to-hire and quality-of-hire
Refine job requirements based on data
Admin Journey
Step 1: Monitor System Health

View real-time processing metrics
Track parse success rates and errors
Monitor LLM API usage and costs
Check worker queue depths
Step 2: Ensure Quality

Review parsing accuracy samples
Validate matching score distributions
Audit LLM outputs for hallucinations
Maintain canonical skill mappings
Step 3: Support Compliance

Access audit logs for decision traceability
Generate compliance reports
Manage data retention policies
Handle user data requests
Step 4: Drive Improvements

Analyze recruitment funnel metrics
Identify common skill gaps
Track job quality trends
Recommend platform enhancements
6. Technology Stack
Backend Technologies
Core Framework

Python 3.11 (modern async support, type hints, performance)
FastAPI (high performance, automatic API documentation, async support)
Data Storage

PostgreSQL via Neon (managed, scalable relational database)
JSONB columns for flexible structured data (parsed resumes, jobs, scores)
SQLAlchemy ORM (type-safe database interactions)
Asynchronous Processing

Redis via Upstash (managed, reliable message broker)
Celery (distributed task queue, proven at scale)
Async task patterns for heavy operations
Authentication & Security

JWT tokens via python-jose (stateless authentication)
Password hashing with industry standards
Role-based access control
Document Processing

PyMuPDF (fast, accurate PDF text extraction)
Text preprocessing and cleaning utilities
AI Integration

Groq API (primary LLM for production, fast inference)
Ollama (local fallback for development and testing)
Structured output validation
Prompt engineering with few-shot examples
Frontend Technologies
Core Framework

React 18 with TypeScript (type safety, modern hooks, performance)
React Router v6 (declarative routing)
State Management & Data Fetching

TanStack Query (server state management, caching, optimistic updates)
Axios (HTTP client with interceptors)
UI Development

Tailwind CSS (utility-first styling, consistent design)
Shadcn UI (accessible, customizable components)
Responsive design patterns
DevOps & Infrastructure
Development Environment

Docker (containerized local development)
Docker Compose (multi-service orchestration)
Hot reload for rapid iteration
Database & Cache

Neon (managed PostgreSQL with autoscaling)
Upstash (managed Redis with global distribution)
Deployment Options

Frontend: Vercel (optimized React deployment, edge network)
Backend: Railway or Render (container hosting, auto-scaling)
Workers: Same platform as backend for simplicity
Monitoring & Observability

Structured logging for all components
Prometheus metrics export (planned)
Grafana dashboards (planned)
Sentry error tracking (planned)
7. System Capabilities
Resume Parsing Capabilities
Text Extraction

Multi-page PDF support
Layout-aware text extraction
Table and column handling
Special character support
Structured Data Extraction

Contact information (name, email, phone)
Skills with evidence sources
Project details (title, technologies, description)
Work experience (company, role, duration)
Education (degree, institution, year)
Certifications (name, issuer, date)
Skill Intelligence

Skill name normalization (React.js → React)
Synonym resolution (JS → JavaScript)
Evidence categorization (project, job, course)
Experience duration estimation
Skill level inference from context
Quality Assurance

Schema validation for all extracted data
Confidence scoring for extractions
Human review flagging for low confidence
Parsing failure handling and retry logic
Job Description Analysis Capabilities
Requirement Extraction

Required skills identification
Preferred skills separation
Experience range extraction
Education requirements
Location and work arrangement details
Quality Assessment

Requirement realism checking
Red flag detection (missing salary, excessive requirements)
Language clarity scoring
Completeness validation
Overall quality score (0-100)
Enhancement Suggestions

Missing information highlights
Unrealistic combination warnings
Inclusive language recommendations
Clarity improvement suggestions
Matching Intelligence
Scoring Components

Required skill match (50% weight default)
Preferred skill match (20% weight)
Experience alignment (20% weight)
Education alignment (10% weight)
Evidence quality bonus
Role-Level Adjustments

Entry level: Increase project and education weight
Mid level: Balanced weighting
Senior level: Increase experience weight, add leadership indicators
Explanation Generation

Score breakdown by component
Matched requirements listing with evidence
Gap identification with specificity
Improvement suggestions
Ranking context (percentile among applicants)
Caching Strategy

Compute on first view or application
Cache results with expiration
Invalidate on resume or job updates
Batch recomputation for efficiency
8. Getting Started Guide
Prerequisites
System Requirements

Python 3.11 or higher
Node.js 18 or higher
npm or yarn package manager
Docker and Docker Compose (for local development)
Git for version control
External Services

Groq API key (sign up at groq.com)
Neon database account (or local PostgreSQL)
Upstash Redis account (or local Redis)
Environment Configuration
Required Environment Variables

GROQ_API_KEY: Your Groq API key for LLM tasks
DATABASE_URL: PostgreSQL connection string
REDIS_URL: Redis connection string with authentication
JWT_SECRET: Secure random string for token signing
OLLAMA_ENDPOINT: Local Ollama endpoint (default: http://localhost:11434)
Optional Configuration

MAX_FILE_SIZE_MB: Maximum resume file size (default: 5)
ALLOWED_FILE_TYPES: Permitted upload formats (default: pdf)
CELERY_WORKERS: Number of worker processes (default: 4)
LOG_LEVEL: Logging verbosity (default: INFO)
Local Development Setup
Backend Setup Process

Install Python dependencies using pip or poetry
Configure environment variables in .env file
Start Redis using Docker or Upstash connection
Run database migrations to create schema
Start Celery worker for async task processing
Launch FastAPI server with hot reload enabled
Frontend Setup Process

Install Node dependencies using npm or yarn
Configure API endpoint in environment file
Start development server with hot reload
Access application at localhost:3000
Command Reference
Database Operations

Run migrations: alembic upgrade head
Rollback migration: alembic downgrade -1
Create new migration: alembic revision --autogenerate -m "description"
Reset database: alembic downgrade base && alembic upgrade head
Celery Operations

Start worker: celery -A app.tasks worker --loglevel info
Monitor tasks: celery -A app.tasks flower (requires flower package)
Purge queue: celery -A app.tasks purge
Backend Operations

Start dev server: uvicorn app.main:app --reload
Run tests: pytest
Generate OpenAPI spec: python -m app.main --export-schema
Frontend Operations

Start dev server: npm run dev
Build production: npm run build
Run tests: npm test
Lint code: npm run lint
Initial Data Setup
Seed Canonical Skills

Import standard skill taxonomy
Add common synonyms mapping
Categorize skills by domain (frontend, backend, data, etc.)
Create Admin Account

Run admin creation script
Set secure password
Configure admin permissions
Test Data Loading

Upload sample resumes
Create test job postings
Verify matching logic
9. API Overview
Authentication Endpoints
POST /api/auth/register

Purpose: Create new user account
Input: name, email, password, role (candidate/recruiter)
Output: User ID, JWT token, profile data
Validation: Email uniqueness, password strength, valid role
POST /api/auth/login

Purpose: Authenticate existing user
Input: email, password
Output: JWT token, user profile, role information
Error handling: Invalid credentials, account lockout
Resume Management Endpoints
POST /api/resumes/upload

Purpose: Upload and queue resume for parsing
Input: PDF file (multipart form data)
Output: Resume ID, parsing status
Side effects: Enqueues Celery task for async processing
Validation: File size, file type, user authentication
GET /api/resumes/{id}

Purpose: Retrieve parsed resume data
Input: Resume ID in path
Output: Full resume JSON with skills, projects, education
Status handling: Pending, parsed, failed states
GET /api/resumes/me

Purpose: Get current user's resumes
Output: List of all user's resumes with status
Job Management Endpoints
POST /api/jobs

Purpose: Create job posting with automatic analysis
Input: Title, description, requirements (raw text)
Output: Job ID, parsed requirements, quality score
Side effects: Enqueues JD analysis task
GET /api/jobs

Purpose: List available jobs
Input: Optional filters (skills, experience, location)
Output: Jobs with match scores (if candidate authenticated)
Special: Computes/caches match scores on demand
GET /api/jobs/{id}

Purpose: Get detailed job information
Output: Full job data with parsed requirements
For candidates: Includes personalized match score and explanation
Application Management Endpoints
POST /api/applications

Purpose: Apply to job opening
Input: Job ID, resume ID
Output: Application ID, initial status
Validation: User is candidate, hasn't already applied
GET /api/applications/me

Purpose: Get candidate's application history
Output: Applications with status and feedback
GET /api/recruiter/jobs/{job_id}/applicants

Purpose: View applicants for a job
Output: Ranked list with match scores and evidence
Authorization: Must be job owner
Sorting: By match score descending (default)
PATCH /api/applications/{id}/status

Purpose: Update application status
Input: New status (reviewed, rejected, offered)
Optional: Rejection reason for analytics
Authorization: Must be recruiter who owns job
Admin Endpoints
GET /api/admin/metrics

Purpose: System health and usage metrics
Output: Parse rates, match computations, API usage
GET /api/admin/audit

Purpose: Access audit log
Input: Optional filters (user, date range, event type)
Output: Paginated event log
10. Data Structure Examples
Resume JSON Structure
Complete Example:

Resume for Jenny Joseph
Email: jenny@example.com
Phone: +1-555-0123

Skills:
- React (12 months experience)
  Evidence: Used in todo app project, internship at TechCo
- Java (6 months experience)
  Evidence: Course project for algorithms class
- Python (18 months experience)
  Evidence: Movie recommender project, data science coursework

Projects:
- Movie Recommender System
  Technologies: Python, Flask, scikit-learn
  Description: Built collaborative filtering engine for movie recommendations
- Todo Application
  Technologies: React, Node.js, MongoDB
  Description: Full stack task management app with user authentication

Education:
- MCA at Lovely Professional University (2025)
- BSc Computer Science at State University (2023)
Key Characteristics:

Evidence tracking for each skill
Experience quantification in months
Project-skill linkage for validation
Education timeline for recency assessment
Job Description JSON Structure
Complete Example:

Title: Software Development Engineer 1 (SDE 1)

Required Skills:
- Java (core language)
- Data Structures and Algorithms (fundamental)

Preferred Skills:
- Spring Boot (framework experience)
- React (frontend capability)
- SQL (database knowledge)

Experience Range: 0-2 years
Education: Bachelor's in Computer Science or related field

Quality Score: 85/100
Analysis: Requirements are realistic for entry level. Red flag detected: Salary range not mentioned. Consider adding compensation details for better transparency.
Quality Indicators:

Clear separation of required vs. preferred
Realistic experience expectations
Specific skill requirements
Red flag identification for improvement
Match Score Structure
Complete Example:

Overall Score: 78/100

Breakdown:
- Required Skill Match: 50/50
  ✓ Java (from course project + 6 months)
  ✓ Data Structures (from education + coursework)

- Preferred Skill Match: 15/20
  ✓ React (from todo app + 12 months)
  ✗ Spring Boot (not found)
  ✗ SQL (not found)

- Experience Alignment: 8/20
  Note: Strong project experience but lacks professional work history

- Education Alignment: 5/10
  ✓ MCA degree matches requirement

Explanation:
Candidate demonstrates solid required skills through academic projects and some practical experience. React proficiency from personal project is valuable. Main gaps are Spring Boot framework and 1 year of professional experience. Recommend: Build a Spring Boot project and consider internships to strengthen profile.

Ranking: Top 25% of applicants for this position
Explanation Components:

Numerical breakdown for transparency
Evidence for matched skills
Specific gap identification
Actionable improvement suggestions
Comparative ranking context
11. Testing Strategy
Unit Testing Scope
Parser Functions

Text extraction accuracy from PDF samples
Skill normalization logic (synonyms, variations)
Evidence tagging correctness
Experience duration calculation
Contact information extraction
Scoring Logic

Score calculation with known inputs
Weight adjustment by role level
Evidence-based bonus application
Edge cases (missing data, partial matches)
Score breakdown generation
Data Validation

Schema validation for all JSON structures
Input sanitization and cleaning
Type conversion and coercion
Required field enforcement
Integration Testing Scope
Resume Upload to Parse Flow

End-to-end file upload
Celery task execution
LLM API interaction
Database persistence
Status update propagation
Job Posting to Analysis Flow

Job creation with raw description
Async analysis triggering
Quality score computation
Red flag detection
Parsed data storage
Matching Flow

Score computation on demand
Cache hit and miss scenarios
Explanation generation
Breakdown accuracy
End-to-End Testing Scope
Complete Application Flow

Candidate registration
Resume upload and parsing wait
Job browsing with match scores
Application submission
Recruiter dashboard view
Application status update
Testing with Mock LLM

Use local Ollama for predictable outputs
Avoid API costs in CI/CD
Faster test execution
Controlled response validation
Testing Tools and Practices
Backend Testing

pytest for unit and integration tests
pytest-asyncio for async code testing
Factory pattern for test data generation
Fixtures for database setup and teardown
Frontend Testing

Jest for unit tests
React Testing Library for component tests
Mock Service Worker for API mocking
Cypress or Playwright for E2E tests
Test Data Management

Sample resumes with known structure
Job descriptions with various quality levels
Expected match score mappings
Edge case documents (formatting, languages)
12. Security & Compliance
Authentication Security
Password Management

Strong password requirements enforcement
Secure hashing (bcrypt or Argon2)
Salt generation per user
No plaintext storage ever
Token Security

JWT with secure secret key
Short expiration times (refresh pattern)
Token revocation capability
HTTPS-only transmission
Session Management

Stateless authentication preferred
Optional refresh tokens for long sessions
Device tracking for suspicious activity
Logout invalidation
File Upload Security
Validation

File type verification (not just extension)
File size limits enforcement (default 5MB)
Virus scanning integration (future)
Sanitization before storage
Storage Security

Encrypted at rest
Access control by user ID
Temporary URL generation for downloads
Automatic cleanup of old files
API Security
Request Protection

Rate limiting per user and IP
CORS configuration for trusted origins
Input validation and sanitization
SQL injection prevention via ORM
XSS prevention in all outputs
External API Security

API keys in environment variables only
Secret manager for production (AWS Secrets Manager, etc.)
Key rotation capability
Usage monitoring and alerting
Data Privacy
User Data Handling

Minimal data collection principle
Clear privacy policy and consent
User data export capability
Account deletion and data removal
Compliance Support

Audit logging for all decisions
Data retention policy configuration
Right to explanation (GDPR-aligned)
Opt-out from analytics aggregation
LLM Security
Prompt Injection Prevention

Input sanitization before LLM calls
Output validation against expected schemas
No user input directly in system prompts
Hallucination detection and flagging
Data Leakage Prevention

No sensitive data in LLM prompts when possible
API provider terms review
Local LLM option for sensitive deployments
Audit trail of all LLM interactions
13. Contributing Guidelines
How to Contribute
Getting Started

Fork the repository to your account
Clone your fork locally
Create a feature branch from main
Set up development environment
Make your changes with tests
Open pull request with description
Branch Naming Convention

Feature: feature/short-description
Bug fix: fix/issue-number-description
Documentation: docs/what-changed
Refactor: refactor/component-name
Commit Message Guidelines

Use present tense ("Add feature" not "Added feature")
First line under 50 characters
Detailed description after blank line
Reference issue numbers when applicable
Code Quality Standards
Python Code

Follow PEP 8 style guide
Type hints for all functions
Docstrings for public APIs
Maximum line length 100 characters
Run Black formatter before commit
TypeScript/React Code

ESLint configuration compliance
Prettier formatting
Component documentation
Prop type definitions
Meaningful variable names
Testing Requirements

Unit tests for new functions
Integration tests for new endpoints
Maintain or improve code coverage
All tests must pass before merge
Pull Request Process
PR Description Must Include:

What problem does this solve?
What approach was taken?
What testing was done?
Any breaking changes?
Screenshots (for UI changes)
Review Process

At least one approval required
All CI checks must pass
No unresolved conversations
Squash and merge preferred
Areas Welcome for Contribution
High Priority

Skill taxonomy expansion
Parsing accuracy improvements
Additional LLM provider support
Monitoring and observability
Performance optimization
Medium Priority

UI/UX enhancements
Additional test coverage
Documentation improvements
Internationalization
Accessibility improvements
14. Project Differentiators
This is Not a Job Board Clone
Traditional Platforms Focus On:

High volume of postings
Keyword-based filtering
Manual skill selection
Binary match (yes/no)
Opaque rejection process
This Platform Focuses On:

Quality over quantity
Context-aware understanding
Automatic data extraction
Graduated match scores with reasoning
Transparent feedback loops
Unique Value Propositions
For Candidates:

Zero redundant data entry: Upload resume once, data extracted automatically
Learning from rejection: Specific feedback on gaps and improvement path
Fair evaluation: Projects and education count, not just years of experience
Transparency: Understand exactly why you match or don't match
For Recruiters:

Evidence-based hiring: See how candidates gained each skill
Quality-checked job posts: System validates requirement realism
Ranked applicants: Focus on best fits first with clear reasoning
Continuous improvement: Learn which requirements are bottlenecks
For the Platform:

Explainable AI: LLM supports but doesn't decide, logic is deterministic
Fairness by design: Role-level adjustments prevent bias against freshers
Audit trail: Every decision logged for accountability
Responsible automation: Assists human judgment, doesn't replace it
Technical Sophistication
System Design Thinking

Separation of concerns (parsing, scoring, presentation)
Asynchronous processing for scalability
Caching strategy for performance
Event-driven audit logging
AI Integration Philosophy

AI for extraction and explanation only
Scoring remains deterministic and transparent
Fallback mechanisms for reliability
Validation of all AI outputs
Data Architecture

Structured storage for queryability
JSONB for flexibility without schema chaos
Normalization for consistency
Partitioning strategy for scale
License
Choose an appropriate open source license for your use case:

MIT License (permissive, allows commercial use)
Apache 2.0 (permissive with patent grant)
GPL v3 (copyleft, requires derivatives to be open source)
Contact and Support
Project Maintainer: [Your Name]

Email: [Your Email]

Issues: Use GitHub Issues for bug reports and feature requests

Discussions: Use GitHub Discussions for questions and ideas

ARCHITECTURE.md
System Architecture Documentation
Purpose: This document provides comprehensive technical guidance for implementing and deploying the Hiring Intelligence Platform. It covers component design, data flows, integration patterns, and operational considerations.

Table of Contents
Architecture Overview
System Components
Data Model Design
Sequence Flows
Matching Algorithm Design
LLM Integration Patterns
Security Architecture
Scalability Considerations
Observability Strategy
Deployment Architecture
Open Questions and Decisions
1. Architecture Overview
High-Level Architecture Diagram
[Candidate Browser] ←→ [React Frontend] ←→ [FastAPI Backend] ←→ [PostgreSQL]
[Recruiter Browser] ↑                      ↓                      ↑
[Admin Dashboard]   └─────[Static Assets]  └─→ [Redis Queue]     │
                                                     ↓             │
                                              [Celery Workers] ────┘
                                                     ↓
                                              [Groq API / Ollama]
Component Interaction Flow
Request Path:

User interacts with React frontend
Frontend sends authenticated API request
FastAPI validates JWT and processes request
For async operations: Task enqueued to Redis
Celery worker picks up task
Worker processes (may call LLM)
Results written to PostgreSQL
Frontend polls or receives notification
Data Flow:

User uploads → S3/File Storage → Database reference → Worker processes → Structured JSON
Job posted → Database → Worker analyzes → Structured requirements → Match computation
Match requested → Check cache → Compute if needed → Store → Return with explanation
Architectural Principles
Separation of Concerns

Frontend: Presentation and user interaction only
API Server: Request validation, orchestration, lightweight logic
Workers: Heavy computation, LLM calls, data processing
Database: Single source of truth for canonical data
Asynchronous by Default

All heavy operations run in workers
Users never wait for LLM calls
Progress updates via polling or WebSocket
Graceful degradation if workers are busy
Deterministic Core Logic

Matching scores computed with explicit formulas
Weights defined in configuration, not AI-generated
LLM provides data extraction, not decisions
All business logic auditable and testable
API-First Design

Backend exposes OpenAPI specification
Frontend is one of many potential clients
Mobile app could consume same APIs
Third-party integrations possible
2. System Components
Component 1: Web Client (React Frontend)
Responsibilities:

Render user interfaces for all roles
Handle file uploads with progress tracking
Display structured data (resumes, jobs, matches)
Manage client-side routing
Cache API responses for performance
Provide responsive, accessible experience
Key Technologies:

React 18: Component library with concurrent features
TypeScript: Type safety for reduced runtime errors
TanStack Query: Server state management with caching
React Router: Declarative routing and navigation
Tailwind CSS: Utility-first styling for consistency
Shadcn UI: Accessible component primitives
State Management Strategy:

Server state: TanStack Query with cache invalidation
UI state: React hooks (useState, useReducer)
Auth state: Context API with persistence
Form state: Controlled components or React Hook Form
File Upload Handling:

Direct upload to API endpoint (future: presigned S3 URLs)
Progress tracking with chunked upload support
Client-side validation before upload
Error handling with retry capability
Deployment:

Build artifacts served via Vercel or similar CDN
Environment-based API endpoint configuration
Automatic preview deployments for PRs
Production builds with minification and tree-shaking
Component 2: API Server (FastAPI Backend)
Responsibilities:

Authenticate and authorize all requests
Validate input data against schemas
Orchestrate business logic workflows
Enqueue tasks for asynchronous processing
Query database for structured data
Compute or retrieve cached match scores
Generate API documentation automatically
Key Technologies:

FastAPI: High-performance async web framework
Pydantic: Data validation and serialization
SQLAlchemy: ORM for type-safe database access
Alembic: Database migration management
python-jose: JWT token handling
PyMuPDF: PDF text extraction (could move to worker)
API Design Patterns:

RESTful endpoints with resource-based URLs
JWT authentication via Authorization header
Role-based access control middleware
Pagination for list endpoints (limit/offset)
Filtering and sorting via query parameters
Standardized error response format
Request Lifecycle:

Request received and logged
JWT validated and user extracted
Route handler invoked with validated inputs
Permission check based on user role
Business logic execution or task enqueue
Response serialization and return
Error handling with appropriate status codes
Minimal Scoring Logic:

API can compute match scores synchronously for small datasets
For large-scale matching, offload to workers
Caching layer to avoid recomputation
Score computation uses imported matching module
Deployment:

Containerized with Docker
Deployed on Railway, Render, or AWS ECS
Environment variables for all configuration
Health check endpoint for monitoring
Automatic restarts on failure
Component 3: Async Worker Pool (Celery)
Responsibilities:

Process resume parsing tasks
Analyze job descriptions
Compute batch match scores
Enrich data with external APIs (future)
Send notification emails (future)
Clean up old files and data
Key Technologies:

Celery: Distributed task queue with proven scalability
Redis: Message broker and result backend
Python async/await: Concurrent processing within workers
Task Types:

Resume Parsing Task:

Input: Resume file reference and user ID
Process: Extract text → Call LLM → Normalize skills → Validate
Output: Parsed JSON saved to database
Duration: 10-30 seconds depending on LLM latency
Retry: Yes, with exponential backoff
Job Description Analysis Task:

Input: Job ID and raw description text
Process: Call LLM with extraction prompt → Validate → Score quality
Output: Structured requirements saved to database
Duration: 5-15 seconds
Retry: Yes, with exponential backoff
Match Score Batch Computation:

Input: List of candidate-job pairs
Process: Load data → Apply scoring logic → Generate explanations
Output: Match scores written to match_scores table
Duration: Variable based on batch size
Retry: Partial retry for failed items
Worker Configuration:

Concurrency: 4-8 workers per instance
Prefetch: 1 task per worker (for fair distribution)
Time limits: Soft 300s, hard 600s
Queue priority: High (parse), medium (match), low (cleanup)
Error Handling:

Max retries: 3 with exponential backoff
Failed tasks logged with full context
Dead letter queue for manual investigation
Alerts on high failure rates
Deployment:

Same platform as API server for simplicity
Separate container with worker command
Auto-scaling based on queue depth
Graceful shutdown on deployment
Component 4: Database (PostgreSQL via Neon)
Responsibilities:

Store canonical data for all entities
Maintain referential integrity
Support complex queries for analytics
Provide ACID guarantees for transactions
Enable full-text search (future)
Key Technologies:

PostgreSQL 15+: Advanced features like JSONB, CTEs
Neon: Managed Postgres with autoscaling and branching
Alembic: Schema migration tracking
Schema Design Philosophy:

Normalized tables for core entities
JSONB columns for flexible, schema-evolving data
Separate audit/event table for immutable log
Indexes on frequently queried columns
Constraints for data integrity
JSONB Usage:

resumes.parsed_json: Full extracted resume data
jobs.parsed_json: Structured job requirements
match_scores.breakdown: Score component details
events.payload: Flexible event data
Performance Considerations:

Indexes: Primary keys, foreign keys, frequently filtered columns
Partial indexes: For status-based queries
JSONB GIN indexes: For nested JSON queries (if needed)
Connection pooling: Via SQLAlchemy engine
Query optimization: EXPLAIN ANALYZE for slow queries
Backup and Recovery:

Neon automated daily backups
Point-in-time recovery capability
Test restoration process regularly
Export critical data for redundancy
Deployment:

Neon managed instance in production
Local Postgres in Docker for development
Separate databases per environment (dev, staging, prod)
Migration runs before deployment
Component 5: Cache and Queue (Redis via Upstash)
Responsibilities:

Message broker for Celery tasks
Cache frequently computed match scores
Store ephemeral session data (future)
Rate limiting state
Distributed locks (if needed)
Key Technologies:

Redis 7+: In-memory data structure store
Upstash: Managed Redis with global distribution
Cache Strategy:

Match Score Caching:

Key pattern: match:{job_id}:{candidate_id}
Value: JSON with score, breakdown, explanation
TTL: 1 hour (invalidate on resume or job update)
Eviction: LRU if memory limit reached
Resume Parse Status:

Key pattern: resume:status:{resume_id}
Value: Parsing progress percentage
TTL: 1 hour after completion
Purpose: Real-time progress updates to frontend
Rate Limiting:

Key pattern: ratelimit:{user_id}:{endpoint}
Value: Request count
TTL: 1 minute or 1 hour depending on limit
Purpose: Prevent abuse and ensure fair usage
Queue Configuration:

Default queue: General tasks
Priority queues: High (parse), medium (match), low (cleanup)
Visibility timeout: 300 seconds
Max message size: 1MB
Deployment:

Upstash managed instance for production
Local Redis in Docker for development
TLS connection for security
Connection pooling for efficiency
Component 6: LLM Service Integration
Responsibilities:

Extract structured data from unstructured text
Generate human-readable explanations
Validate and improve data quality
Support both cloud and local execution
Key Technologies:

Groq API: Primary cloud LLM (fast inference)
Ollama: Local LLM for development and fallback
Prompt templates: Versioned few-shot examples
Integration Architecture:

Primary: Groq API

Endpoint: HTTPS API with authentication
Model: Llama 3 or similar (configurable)
Timeout: 30 seconds with retry
Error handling: Fallback to Ollama on failure
Fallback: Ollama Local

Endpoint: HTTP localhost or Docker service
Model: Llama 2 or Mistral (smaller, faster)
Use cases: Development, testing, cloud provider outages
Limitations: Slower, less accurate than cloud
Prompt Engineering:

Resume Extraction Prompt Structure:

System message: Role and task definition
Few-shot examples: 2-3 sample resumes with expected output
Schema definition: JSON structure to return
Input text: Actual resume content
Output constraint: "Return only valid JSON, no explanation"
Job Description Extraction Prompt Structure:

System message: Extract requirements and assess quality
Few-shot examples: Sample JDs with good vs. poor quality
Schema definition: Required, preferred, experience, quality score
Input text: Job description
Output constraint: JSON only
Explanation Generation Prompt:

System message: Generate candidate-friendly explanation
Input: Match score breakdown, candidate data, job requirements
Output: 2-3 sentences explaining score and gaps
Tone: Constructive and encouraging
Usage Limits and Cost Management:

Token counting before API calls
Budget alerts at 80% and 100% of monthly limit
Graceful degradation: Skip explanations if budget exceeded
Local fallback for non-critical tasks
Output Validation:

Schema validation against expected JSON structure
Confidence scoring based on completeness
Hallucination detection: Flag unexpected fields
Human review queue for low-confidence outputs
Deployment:

API keys in environment variables or secrets manager
Ollama container alongside workers for fallback
Prompt templates versioned in repository
A/B testing capability for prompt improvements
Component 7: Admin Analytics Service
Responsibilities:

Aggregate event data for reporting
Generate hiring funnel metrics
Track job quality trends
Monitor system health indicators
Provide data export capabilities
Implementation Approach:

Phase 1: Query-Based Analytics

SQL queries against events and match_scores tables
Real-time computation for admin dashboard
No separate analytics database initially
Phase 2: Materialized Views

Precomputed aggregations refreshed periodically
Faster dashboard load times
Still using primary database
Phase 3: Separate Analytics Pipeline

Export events to data warehouse (BigQuery, Snowflake)
Complex analytics without impacting production DB
Machine learning on aggregate data
Key Metrics:

System Health:

Resume parse success rate and average time
Job analysis completion rate
Match score computation latency
LLM API error rate and cost per call
Worker queue depth and processing rate
Recruitment Funnel:

Jobs posted per recruiter
Applications per job (average, median, distribution)
Match score distribution across applicants
Application status conversion rates
Time from application to decision
Quality Metrics:

Job quality score distribution
Most common red flags in job postings
Skill normalization accuracy (sample validation)
User-reported parsing errors
Deployment:

Admin endpoints in main API server initially
Separate analytics service if load increases
Read replicas for expensive queries
Caching for frequently accessed reports
Component 8: Logging and Monitoring
Responsibilities:

Capture structured logs from all components
Track application metrics and performance
Alert on errors and anomalies
Provide debugging context for issues
Support compliance and audit needs
Logging Strategy:

Log Levels:

DEBUG: Detailed information for development
INFO: General informational messages (user actions, task starts)
WARNING: Unexpected but handled situations
ERROR: Errors that should be investigated
CRITICAL: System failures requiring immediate action
Structured Logging Format:

Timestamp in ISO 8601
Log level
Component name (api, worker, frontend)
User ID or session ID if applicable
Request ID for tracing
Message and structured data (JSON)
Key Events to Log:

All API requests with latency
Authentication attempts (success and failure)
Resume parse start, success, failure
Job analysis results with quality score
Match score computations with inputs
LLM API calls with token usage and cost
Application status changes
Admin actions
Metrics to Track:

Application Metrics:

Request count by endpoint and status code
Request latency percentiles (p50, p95, p99)
Active user sessions
Database query count and duration
Cache hit/miss rates
Business Metrics:

Resumes uploaded per day
Jobs posted per day
Applications submitted per day
Match scores computed per day
Infrastructure Metrics:

CPU and memory usage per service
Database connection pool utilization
Redis memory usage and eviction rate
Worker queue depth and latency
Monitoring Tools:

Phase 1: Basic Logging

Stdout/stderr logs collected by platform
Log aggregation via platform (Vercel, Railway)
Manual log search and filtering
Phase 2: Dedicated Logging Service

Export to Datadog, Logtail, or similar
Log search with filters and queries
Basic dashboards for key metrics
Phase 3: Full Observability Stack

Metrics: Prometheus + Grafana
Logs: ELK or Loki
Traces: OpenTelemetry + Jaeger
Alerts: PagerDuty or similar
Alerting Rules:

Error rate > 5% for 5 minutes
API latency p95 > 2 seconds
Worker queue depth > 100 for 10 minutes
LLM API error rate > 10%
Database connection pool exhausted
Deployment:

Logging configuration in application code
Metrics exported from application to Prometheus
Dashboards defined as code in repository
Alert rules versioned and reviewed
3. Data Model Design
Primary Entities and Relationships
Entity Relationship Overview:

users (1) ←→ (M) resumes
users (1) ←→ (M) jobs (via recruiter_id)
jobs (1) ←→ (M) applications
users (1) ←→ (M) applications (via candidate_id)
resumes (1) ←→ (M) applications
jobs (1) + users (1) ←→ (1) match_scores
skills (M) ←→ (M) resume skills (via parsed JSON)
Table: users
Purpose: Store user accounts for all roles

Schema:

id (UUID, primary key): Unique user identifier
name (VARCHAR): Full name for display
email (VARCHAR, unique): Email address for login
password_hash (VARCHAR): Securely hashed password
role (ENUM: candidate, recruiter, admin): User role
created_at (TIMESTAMP): Account creation time
updated_at (TIMESTAMP): Last profile update
is_active (BOOLEAN): Account status (for soft deletion)
Indexes:

Primary key on id
Unique index on email
Index on role for filtering
Constraints:

Email must be valid format
Role must be one of allowed values
Password hash cannot be null
Table: resumes
Purpose: Store resume files and parsed data

Schema:

id (UUID, primary key): Unique resume identifier
user_id (UUID, foreign key → users.id): Owner
original_filename (VARCHAR): Uploaded file name
file_path (VARCHAR): Storage location or S3 key
file_size_bytes (INTEGER): File size for validation
parsed_json (JSONB): Extracted structured data
status (ENUM: pending, parsing, parsed, failed): Parse state
error_message (TEXT): Failure reason if status=failed
created_at (TIMESTAMP): Upload time
parsed_at (TIMESTAMP): Completion time
Indexes:

Primary key on id
Foreign key index on user_id
Index on status for filtering pending tasks
JSONB Structure for parsed_json:

{
  "name": string,
  "email": string,
  "phone": string (optional),
  "skills": [
    {
      "skill": string (canonical name),
      "evidence": [string] (sources like "project:X", "job:Y"),
      "months_experience": integer
    }
  ],
  "projects": [
    {
      "title": string,
      "skills_used": [string],
      "description": string,
      "start_date": string (optional),
      "end_date": string (optional)
    }
  ],
  "experience": [
    {
      "company": string,
      "role": string,
      "start_date": string,
      "end_date": string (optional, if current),
      "description": string
    }
  ],
  "education": [
    {
      "degree": string,
      "institution": string,
      "year": integer,
      "major": string (optional)
    }
  ]
}
Table: jobs
Purpose: Store job postings and analyzed requirements

Schema:

id (UUID, primary key): Unique job identifier
recruiter_id (UUID, foreign key → users.id): Job owner
title (VARCHAR): Job title for display
raw_description (TEXT): Original job description text
parsed_json (JSONB): Extracted requirements
quality_score (INTEGER 0-100): Job posting quality
status (ENUM: draft, pending_analysis, active, closed): Job state
created_at (TIMESTAMP): Posting time
analyzed_at (TIMESTAMP): Analysis completion time
closes_at (TIMESTAMP): Application deadline (optional)
Indexes:

Primary key on id
Foreign key index on recruiter_id
Index on status for filtering active jobs
Index on created_at for sorting
JSONB Structure for parsed_json:

{
  "required_skills": [string],
  "preferred_skills": [string],
  "experience_years": [min: integer, max: integer],
  "education_required": string,
  "location": string (optional),
  "work_arrangement": string (remote/hybrid/onsite),
  "quality_analysis": string (explanation),
  "red_flags": [string]
}
Table: applications
Purpose: Track candidate applications to jobs

Schema:

id (UUID, primary key): Unique application identifier
job_id (UUID, foreign key → jobs.id): Target job
candidate_id (UUID, foreign key → users.id): Applicant
resume_id (UUID, foreign key → resumes.id): Resume version used
status (ENUM: applied, reviewed, shortlisted, rejected, offered): Application state
rejection_reason (VARCHAR, optional): Quick reason if rejected
recruiter_notes (TEXT, optional): Private notes
created_at (TIMESTAMP): Application time
updated_at (TIMESTAMP): Last status change
Indexes:

Primary key on id
Foreign key indexes on job_id, candidate_id, resume_id
Composite index on (job_id, status) for recruiter dashboard
Unique constraint on (job_id, candidate_id) to prevent duplicate applications
Table: skills
Purpose: Canonical skill taxonomy with synonyms

Schema:

id (UUID, primary key): Unique skill identifier
canonical_name (VARCHAR, unique): Standard skill name
synonyms (TEXT[]): Alternative names and variations
category (VARCHAR): Skill domain (frontend, backend, data, etc.)
created_at (TIMESTAMP): Entry creation time
Examples:

canonical_name: "React", synonyms: ["React.js", "ReactJS"]
canonical_name: "JavaScript", synonyms: ["JS", "ECMAScript"]
canonical_name: "Python", synonyms: ["Python3"]
Indexes:

Primary key on id
Unique index on canonical_name
GIN index on synonyms for array searching
Table: match_scores
Purpose: Store computed match scores for auditability

Schema:

id (UUID, primary key): Unique score record
job_id (UUID, foreign key → jobs.id): Target job
candidate_id (UUID, foreign key → users.id): Evaluated candidate
resume_id (UUID, foreign key → resumes.id): Resume version used
score (INTEGER 0-100): Overall match score
breakdown (JSONB): Component scores and details
explanation (TEXT): Human-readable explanation
computed_at (TIMESTAMP): Calculation time
Indexes:

Primary key on id
Composite unique index on (job_id, candidate_id, resume_id)
Index on job_id for recruiter ranking queries
Index on computed_at for cleanup of stale scores
JSONB Structure for breakdown:

{
  "required_skill_match": integer (0-50),
  "preferred_skill_match": integer (0-20),
  "experience_alignment": integer (0-20),
  "education_alignment": integer (0-10),
  "matched_required_skills": [string],
  "missing_required_skills": [string],
  "matched_preferred_skills": [string],
  "evidence_bonus": integer (0-10 optional)
}
Table: events
Purpose: Immutable audit log for all significant actions

Schema:

id (UUID, primary key): Unique event identifier
event_type (VARCHAR): Event category (resume_parsed, job_created, etc.)
user_id (UUID, optional): Actor if applicable
entity_type (VARCHAR): Affected entity type
entity_id (UUID): Affected entity ID
payload (JSONB): Event-specific data
created_at (TIMESTAMP): Event occurrence time
Indexes:

Primary key on id
Index on event_type for filtering
Index on user_id for user activity logs
Index on (entity_type, entity_id) for entity timelines
Index on created_at for time-based queries
Event Types:

user_registered: New account creation
resume_uploaded: File upload initiated
resume_parsed: Parsing completed successfully
resume_parse_failed: Parsing error occurred
job_created: New job posting
job_analyzed: JD analysis completed
application_submitted: Candidate applied
application_status_changed: Status update by recruiter
match_computed: Score calculation occurred
Example Payload:

{
  "resume_id": "uuid",
  "status": "parsed",
  "skills_extracted": 12,
  "projects_found": 3,
  "llm_tokens_used": 1500
}
4. Sequence Flows
Flow 1: Resume Upload and Parsing
Actors: Candidate, Frontend, API Server, Celery Worker, Database, LLM

Steps:

Candidate uploads PDF file via frontend
Frontend validates file type and size client-side
Shows upload progress bar
Frontend sends file to POST /api/resumes/upload
Multipart form data with file
JWT token in Authorization header
API Server receives and validates request
Verify JWT and extract user ID
Check user role is candidate
Validate file size (< 5MB) and type (PDF)
API Server stores file and creates resume record
Save file to storage (local FS or S3)
Insert row in resumes table with status='pending'
Return resume ID and status to frontend
API Server enqueues parse task
Create Celery task with resume ID
Push to Redis queue (high priority)
Return immediately to frontend (non-blocking)
Frontend shows parsing status
Poll GET /api/resumes/{id} every 2 seconds
Display "Parsing in progress" message
Celery Worker picks up task
Fetch resume record from database
Download file from storage
Update status to 'parsing'
Worker extracts text from PDF
Use PyMuPDF to extract all text
Clean and preprocess text (remove extra whitespace)
Worker calls LLM for structured extraction
Build prompt with few-shot examples and schema
Call Groq API (or Ollama if Groq fails)
Parse JSON response
Validate against expected schema
Worker normalizes skills
For each extracted skill, query skills table
Match against canonical_name or synonyms array
Replace with canonical name if found
Flag unknown skills for admin review
Worker validates and stores results
Check all required fields present (name, skills)
Update resumes.parsed_json with structured data
Set status='parsed' and parsed_at=now()
Commit database transaction
Worker emits event
Insert event with type='resume_parsed'
Include metadata: skill count, project count, LLM tokens
Frontend receives updated status
Next poll returns status='parsed'
Display success message
Redirect to parsed resume view
Error Handling:

File upload fails: Frontend shows error, allows retry
LLM API error: Worker retries 3 times, then falls back to Ollama
Parsing fails completely: Set status='failed', store error_message, notify user
Invalid JSON from LLM: Log warning, request human review, return partial data if possible
Flow 2: Job Posting and Analysis
Actors: Recruiter, Frontend, API Server, Celery Worker, Database, LLM

Steps:

Recruiter composes job description
Fill form with title and description (paste or type)
Submit via POST /api/jobs
API Server validates request
Verify JWT and extract user ID
Check user role is recruiter
Validate title and description not empty
API Server creates job record
Insert row in jobs table with status='pending_analysis'
Store raw_description as provided
Return job ID immediately
API Server enqueues analysis task
Create Celery task with job ID
Push to Redis queue (medium priority)
Celery Worker picks up task
Fetch job record from database
Extract raw_description text
Worker calls LLM for JD analysis
Build prompt to extract requirements and assess quality
Call Groq API with job description
Parse JSON response with required_skills, preferred_skills, etc.
Worker computes quality score
Check for missing information (salary, location)
Detect unrealistic combinations (10 years + junior level)
Count red flags
Assign score 0-100 (100 = excellent, clear, realistic)
Worker stores analysis results
Update jobs.parsed_json with extracted requirements
Set quality_score
Update status='active'
Set analyzed_at=now()
Worker emits event
Insert event with type='job_analyzed'
Include quality_score and red_flag count
Worker optionally triggers match precomputation
If configured, enqueue tasks to compute matches for all active candidates
This is optional; can also compute on-demand when candidate views job
Recruiter views analysis results
Frontend polls or receives notification
Display quality score and suggestions
Allow recruiter to edit and resubmit if needed
Error Handling:

LLM extraction fails: Set status='active' with empty parsed_json, log error
Quality score cannot be determined: Default to 50 (neutral)
Red flags detected: Show warnings to recruiter, allow override
Flow 3: Candidate Views Jobs with Match Scores
Actors: Candidate, Frontend, API Server, Database, Cache

Steps:

Candidate navigates to job browse page
Frontend sends GET /api/jobs with JWT token
API Server identifies user
Extract candidate_id from JWT
Fetch candidate's latest parsed resume
API Server fetches active jobs
Query jobs table where status='active'
Sort by created_at descending (newest first)
Paginate (e.g., 20 per page)
For each job, API computes or retrieves match score
Step 4a: Check cache

Key: match:{job_id}:{candidate_id}
If hit: Use cached score and explanation
If miss: Proceed to computation
Step 4b: Compute match score

Load job parsed_json (requirements)
Load candidate resume parsed_json (skills, experience, education)
Apply scoring algorithm (see section 5)
Generate breakdown and explanation
Step 4c: Cache result

Store score, breakdown, explanation in Redis
Set TTL to 1 hour
Also insert into match_scores table for audit
API Server returns job list with scores
Each job includes match score and brief explanation
Sort by score descending (best matches first) if requested
Frontend displays ranked jobs
Show score as percentage or visual indicator
Display matched skills and gaps
Allow filtering by minimum score
Optimizations:

Batch scoring: Compute multiple matches in parallel
Lazy loading: Only compute scores for visible jobs (first page)
Background precomputation: Worker task to compute common matches during off-peak
Flow 4: Candidate Applies to Job
Actors: Candidate, Frontend, API Server, Database

Steps:

Candidate clicks "Apply" button
Frontend sends POST /api/applications
Body: {job_id, resume_id}
JWT token authenticates candidate
API Server validates request
Verify candidate hasn't already applied (check uniqueness constraint)
Verify job is still open (status='active')
Verify resume belongs to candidate
API Server creates application record
Insert into applications table
Set status='applied'
Link job_id, candidate_id, resume_id
API Server emits event
Insert event with type='application_submitted'
Include job title, candidate name for analytics
API Server returns success
Frontend shows confirmation message
Update UI to reflect "Applied" state
Optional: Notify recruiter
Future enhancement: Send email or in-app notification
Include candidate summary and match score
Error Handling:

Duplicate application: Return 409 Conflict with message
Job closed: Return 400 Bad Request with explanation
Resume not parsed: Return 400 with "Please wait for resume processing"
Flow 5: Recruiter Reviews Applicants
Actors: Recruiter, Frontend, API Server, Database

Steps:

Recruiter opens job applicants page
Frontend sends GET /api/recruiter/jobs/{job_id}/applicants
JWT token identifies recruiter
API Server validates authorization
Verify recruiter owns this job
Return 403 Forbidden if not
API Server fetches applications
Query applications table where job_id matches
Join with users (candidate name, email)
Join with resumes (parsed data)
Join with match_scores (score and breakdown)
API Server ranks applicants
Sort by match score descending (highest first)
Apply filters if requested (e.g., status='applied')
Paginate results
API Server returns ranked list
Each applicant includes:
Name, email, application date
Match score and explanation
Resume summary (skills, projects, education)
Current status
Frontend displays applicant cards
Visual score indicator (color-coded)
Expandable details for each applicant
Action buttons: Review, Shortlist, Reject
Recruiter updates application status
Click "Shortlist" or "Reject" button
Frontend sends PATCH /api/applications/{id}/status
Body: {status: 'shortlisted', rejection_reason: '...'}
API Server updates application
Verify recruiter owns the job
Update applications.status and updated_at
Store optional rejection_reason or recruiter_notes
API Server emits event
Insert event with type='application_status_changed'
Include old status, new status, reason
Frontend updates UI
Move applicant to appropriate section
Show confirmation message
Future Enhancement: Feedback Loop

Track which skill gaps most often lead to rejection
Suggest job requirement adjustments if too few qualified applicants
Analyze time-to-hire by match score range
5. Matching Algorithm Design
Scoring Components and Weights
Default Weight Distribution (Total = 100 points):

Required Skills Match: 50 points
Measures coverage of must-have skills
Critical for role functionality
Preferred Skills Match: 20 points
Measures coverage of nice-to-have skills
Differentiates strong candidates
Experience Alignment: 20 points
Measures years of experience fit
Considers both total and skill-specific experience
Education Alignment: 10 points
Measures degree and field of study match
Less weight as practical skills matter more
Role-Level Weight Adjustments
Entry Level (0-2 years experience):

Required Skills: 40 points (reduced, as freshers may not have all)
Preferred Skills: 15 points
Experience: 10 points (reduced weight)
Education: 15 points (increased, as it's their main credential)
Projects: 20 points (new component, demonstrates initiative)
Mid Level (2-5 years):

Use default weights
Senior Level (5+ years):

Required Skills: 45 points
Preferred Skills: 20 points
Experience: 30 points (increased, proven track record matters)
Education: 5 points (reduced, experience speaks louder)
Detailed Scoring Logic
1. Required Skills Match (max 50 points)

Inputs:

Job required_skills: ["Java", "Data Structures", "Spring Boot"]
Candidate skills from parsed resume
Algorithm:

matched_count = 0
evidence_bonus = 0

for each required_skill in job.required_skills:
    if required_skill in candidate.skills (normalized):
        matched_count += 1
        
        # Evidence bonus: +10% if skill has project evidence
        skill_data = candidate.skills[required_skill]
        if "project:" in skill_data.evidence:
            evidence_bonus += 1

base_score = (matched_count / total_required) * 50
evidence_score = (evidence_bonus / total_required) * 5

final_score = min(50, base_score + evidence_score)
Example:

Job requires: ["Java", "Data Structures", "Spring Boot"] (3 skills)
Candidate has: ["Java" (with project evidence), "Data Structures" (coursework only)]
Matched: 2 out of 3 = 66.7%
Base score: 0.667 * 50 = 33.3
Evidence bonus: 1 out of 3 with evidence = 0.333 * 5 = 1.7
Final: 35 points
2. Preferred Skills Match (max 20 points)

Algorithm:

matched_count = 0

for each preferred_skill in job.preferred_skills:
    if preferred_skill in candidate.skills:
        matched_count += 1

score = (matched_count / total_preferred) * 20
Example:

Job prefers: ["React", "SQL", "Docker"] (3 skills)
Candidate has: ["React", "Docker"]
Matched: 2 out of 3 = 66.7%
Score: 0.667 * 20 = 13.3 points
3. Experience Alignment (max 20 points)

Inputs:

Job experience range: [min: 0, max: 2] (years)
Candidate total experience: Sum of all work experience durations
Candidate skill-specific experience: From resume.skills[].months_experience
Algorithm:

# Calculate total professional experience
total_months = sum(candidate.experience[].duration_months)
total_years = total_months / 12

# Check if within range
if total_years >= job.experience_years.min and total_years <= job.experience_years.max:
    base_score = 20
elif total_years < job.experience_years.min:
    # Penalize proportionally to shortfall
    ratio = total_years / job.experience_years.min
    base_score = ratio * 20
else:  # Overqualified
    # Mild penalty for being overqualified (risk of leaving)
    years_over = total_years - job.experience_years.max
    penalty = min(5, years_over * 2)
    base_score = max(15, 20 - penalty)

score = base_score
Example 1: Perfect fit

Job requires 0-2 years
Candidate has 1.5 years
Score: 20 points
Example 2: Underqualified

Job requires 2-5 years
Candidate has 1 year
Ratio: 1/2 = 0.5
Score: 0.5 * 20 = 10 points
Example 3: Overqualified

Job requires 0-2 years
Candidate has 5 years
Years over: 5 - 2 = 3
Penalty: min(5, 3*2) = 5
Score: 20 - 5 = 15 points
4. Education Alignment (max 10 points)

Inputs:

Job education requirement: e.g., "Bachelor's in Computer Science"
Candidate education: List of degrees
Algorithm:

score = 0

for each degree in candidate.education:
    if degree.level >= job.required_level:  # Bachelor's, Master's, PhD
        score += 5
    
    if degree.major matches job.field (CS, related, or any):
        score += 5
    
    # Cap at 10
    score = min(10, score)
Example:

Job requires Bachelor's in Computer Science
Candidate has MCA (Master's in Computer Applications)
Level match: +5 (Master's >= Bachelor's)
Field match: +5 (Computer Applications is related)
Score: 10 points
Explanation Generation
Structure:

Opening: Overall score and ranking context
Strengths: Matched skills with evidence
Gaps: Missing skills or experience
Recommendations: Specific improvement suggestions
Example Template:

Score: {score}/100 (Top {percentile}% of applicants)

Strengths:
- Strong match on required skills: {matched_required}
- {matched_preferred_count} preferred skills demonstrated
- {education_summary}

Gaps:
- Missing required skills: {missing_required}
- Missing preferred skills: {missing_preferred}
- Experience: {experience_gap_explanation}

Recommendations:
- Build a project using {missing_skill_1} to gain practical experience
- Consider {certification} to strengthen {area}
- {experience_advice if applicable}
LLM-Enhanced Explanation (Optional):

After computing score and breakdown, pass to LLM
Request natural language summary
LLM makes explanation more conversational and encouraging
Validate LLM output for factual accuracy against breakdown
Caching and Invalidation
Cache Key: match:{job_id}:{candidate_id}:{resume_id}

TTL: 1 hour (3600 seconds)

Invalidation Triggers:

Resume re-parsed (new resume version)
Job requirements updated
Scoring algorithm weights changed (requires full cache flush)
Cache Miss Handling:

Compute score synchronously if under 100ms expected
Otherwise, return "computing" status and queue worker task
Frontend polls for result

6. LLM Integration Patterns
Prompt Engineering Strategy
Core Principles:

Use few-shot learning with 2-3 examples
Provide explicit JSON schema definitions
Constrain output format strictly
Validate all outputs against schemas
Version prompts in repository
Resume Parsing Prompt
Prompt Structure:

System Message:

You are a resume parser. Your task is to extract structured information from resume text and return it as valid JSON. Be precise and only extract information that is explicitly stated. Do not infer or hallucinate details.
Few-Shot Examples (2-3 samples):

Example 1:
Input: "John Doe, john@example.com. Skills: Python, Django. Built a blog using Django."
Output: {"name": "John Doe", "email": "john@example.com", "skills": [{"skill": "Python", "evidence": ["project:blog"], "months_experience": 0}]}

Example 2:
[Another complete example]
Schema Definition:

Return JSON with these fields:
- name (string, required)
- email (string, required)
- phone (string, optional)
- skills (array of objects with: skill, evidence array, months_experience)
- projects (array with: title, skills_used, description)
- experience (array with: company, role, start_date, end_date, description)
- education (array with: degree, institution, year, major)
Output Constraint:

Return ONLY valid JSON. No explanatory text before or after. No markdown code blocks.
Full Prompt Assembly:

[System Message]
[Few-shot Examples]
[Schema Definition]
[Output Constraint]

Now extract from this resume:
[ACTUAL RESUME TEXT]
Job Description Analysis Prompt
Prompt Structure:

System Message:

You are a job description analyzer. Extract requirements and assess quality. Identify unrealistic expectations and missing information. Return valid JSON only.
Few-Shot Examples:

Example 1 - Good JD:
Input: "Senior Python Developer. Required: Python, Django, 3-5 years. Preferred: React. Salary: $80-100k."
Output: {"required_skills": ["Python", "Django"], "preferred_skills": ["React"], "experience_years": [3,5], "quality_score": 95, "red_flags": []}

Example 2 - Poor JD:
Input: "Junior developer needed. Must have 10 years experience in Python, Java, React, ML, DevOps."
Output: {"required_skills": ["Python", "Java", "React", "Machine Learning", "DevOps"], "experience_years": [0,2], "quality_score": 30, "red_flags": ["Unrealistic skill count for junior role", "Experience mismatch with level", "Salary not mentioned"]}
Schema Definition:

Return JSON with:
- required_skills (array of strings)
- preferred_skills (array of strings)
- experience_years (object with min and max)
- education_required (string)
- location (string)
- work_arrangement (remote/hybrid/onsite)
- quality_score (integer 0-100)
- quality_analysis (string explanation)
- red_flags (array of strings)
Quality Scoring Guidelines:

90-100: Excellent - Clear, realistic, complete information
70-89: Good - Minor issues, mostly complete
50-69: Fair - Missing information or some unrealistic expectations
30-49: Poor - Multiple red flags or unclear requirements
0-29: Very Poor - Unrealistic or incomplete
Match Explanation Prompt
Prompt Structure:

System Message:

You are a career advisor. Given a match score breakdown, generate a constructive, encouraging 2-3 sentence explanation for the candidate. Focus on gaps and actionable improvements.
Input Format:

Candidate: {name}
Job: {job_title}
Score: {score}/100

Matched Required Skills: {list}
Missing Required Skills: {list}
Matched Preferred Skills: {list}
Experience: {candidate_years} years, job requires {job_min}-{job_max}

Generate explanation:
Output Examples:

High Score (75+): "You're a strong match with {score}% compatibility. Your {strength} aligns well. To further improve, consider {suggestion}."

Medium Score (50-74): "You meet {percentage}% of requirements with solid {strengths}. Key gaps are {missing_skills}. Recommend building a project with {skill} to strengthen your profile."

Low Score (below 50): "Your current profile shows {strengths}, but this role requires {missing_critical}. Focus on gaining experience in {top_3_gaps} through projects or courses."
Prompt Version Management
Versioning Strategy:

Store prompts in prompts/ directory
Use semantic versioning (v1.0.0, v1.1.0, v2.0.0)
Track prompt performance metrics
A/B test prompt variations
Roll back if quality degrades
File Structure:

prompts/
├── resume_extraction_v1.0.json
├── resume_extraction_v1.1.json
├── job_analysis_v1.0.json
├── match_explanation_v1.0.json
└── README.md (changelog)
Prompt Metadata:

{
  "version": "1.1.0",
  "created_date": "2024-01-15",
  "description": "Improved skill evidence extraction",
  "system_message": "...",
  "few_shot_examples": [...],
  "schema": {...},
  "output_constraint": "...",
  "performance_metrics": {
    "avg_extraction_accuracy": 0.92,
    "avg_tokens": 1200
  }
}
LLM Output Validation
Validation Pipeline:

JSON Validity Check
Attempt to parse response as JSON
If fails, log error and retry with modified prompt
Max 2 retries before fallback
Schema Validation
Validate against expected schema using Pydantic
Check required fields present
Validate field types
Ensure arrays are not empty where required
Semantic Validation
Skills: Check against known skill taxonomy
Dates: Validate format and logical consistency
Experience: Ensure months_experience >= 0
Email: Validate format
Confidence Scoring
Completeness: % of expected fields filled
Consistency: Cross-field validation (e.g., skills mentioned in projects match skills list)
Realism: Flag unusual values (e.g., 20 years experience with technology from 2020)
Hallucination Detection
Flag skills not mentioned in original text
Flag projects without clear evidence
Flag overly specific details not in source
Confidence Thresholds:

High confidence (90-100%): Auto-accept
Medium confidence (70-89%): Accept but flag for review
Low confidence (<70%): Queue for human review
Error Handling and Fallbacks
Groq API Error Scenarios:

Rate Limit Exceeded
Wait and retry with exponential backoff
If persistent, fall back to Ollama
Queue for retry during off-peak hours
API Timeout
Retry up to 3 times
Fall back to Ollama on third failure
Log for investigation
Invalid API Key
Alert admin immediately
Switch to Ollama for all tasks
Block new parse requests until resolved
Model Unavailable
Try alternate model if configured
Fall back to Ollama
Notify admin
Ollama Fallback Strategy:

Automatically used when Groq fails
Slightly different prompt tuning (Ollama models may need simpler instructions)
Longer timeout (local inference can be slower)
Same validation pipeline
Flag outputs as "fallback-generated" in database
Cost Management
Token Usage Tracking:

Count input and output tokens per request
Log tokens used per resume, job, explanation
Aggregate daily and monthly usage
Alert at 80% of budget
Cost Optimization Strategies:

Prompt Optimization
Remove unnecessary examples after validation
Use concise system messages
Limit output verbosity
Caching
Cache skill normalization results
Reuse job analysis if description unchanged
Cache common explanation templates
Batching
Batch multiple skill normalizations in one API call
Process multiple resumes in single request if possible
Graceful Degradation
If budget exceeded, skip non-essential LLM calls
Use template-based explanations instead of LLM-generated
Resume parsing continues, but with reduced enhancement
7. Security Architecture
Authentication and Authorization
Multi-Layer Security Model:

Layer 1: Transport Security

HTTPS/TLS 1.3 for all connections
HSTS headers to force HTTPS
Certificate pinning for API clients (optional)
Layer 2: Authentication

JWT-based stateless authentication
Access token: Short-lived (15 minutes)
Refresh token: Long-lived (7 days), stored securely
Token rotation on refresh
Layer 3: Authorization

Role-based access control (RBAC)
Resource ownership validation
Endpoint-level permission checks
JWT Token Structure
Access Token Payload:

{
  "user_id": "uuid",
  "email": "user@example.com",
  "role": "candidate|recruiter|admin",
  "iat": 1234567890,
  "exp": 1234568790,
  "type": "access"
}
Security Measures:

Sign with HS256 or RS256 algorithm
Use strong secret (min 256 bits) or private key
Include expiration time (exp)
Include issued-at time (iat)
Validate signature on every request
Check expiration before processing
Token Storage:

Frontend: HTTP-only cookies (preferred) or secure localStorage
Never log tokens
Clear tokens on logout
Revoke on password change
Password Security
Hashing Strategy:

Algorithm: bcrypt or Argon2id (recommended)
Cost factor: 12 (bcrypt) or memory=64MB, time=3, parallelism=4 (Argon2)
Unique salt per password (automatic with bcrypt/Argon2)
Never store plaintext passwords
Password Policy:

Minimum length: 8 characters
Require: At least one letter and one number
No common passwords (check against breach database)
No password reuse (store hash of last 3 passwords)
Account Protection:

Rate limit login attempts: 5 per 15 minutes per IP
Temporary lockout after 5 failed attempts
Email notification on suspicious login
Optional 2FA (future enhancement)
File Upload Security
Upload Validation:

File Type Verification
Check magic bytes, not just extension
Only allow PDF files for resumes
Reject files with embedded executables
File Size Limits
Maximum: 5MB per resume
Enforce at multiple layers: Client, API gateway, Backend
Content Scanning
Virus scan with ClamAV or similar (future)
Check for suspicious patterns
Validate PDF structure
Filename Sanitization
Remove special characters
Generate unique server-side filename (UUID)
Never use user-provided filename directly
Secure Storage:

Store files outside web root
Use object storage (S3) with IAM controls
Encrypt at rest (AES-256)
Generate signed URLs for temporary access
Set content-type header correctly
Implement access logging
API Security
Input Validation:

Validate all inputs against strict schemas (Pydantic)
Reject unexpected fields
Sanitize string inputs (SQL injection prevention)
Limit array and string lengths
Validate email, URL formats
SQL Injection Prevention:

Use ORM parameterized queries only (SQLAlchemy)
Never construct SQL from user input
Disable raw SQL execution in production
XSS Prevention:

Escape all user content in responses
Set Content-Security-Policy headers
Use HTTP-only cookies
Validate and sanitize rich text if added
CSRF Protection:

Use SameSite cookie attribute
Validate origin and referer headers
CSRF tokens for state-changing operations (if using cookies)
Rate Limiting:

Per-Endpoint Limits:

Login: 5 requests / 15 minutes per IP
Register: 3 requests / hour per IP
Resume upload: 10 requests / hour per user
Job creation: 20 requests / hour per user
API calls: 100 requests / minute per user
Implementation:

Use Redis for distributed rate limiting
Return 429 Too Many Requests with Retry-After header
Different limits for different roles (admin higher limits)
CORS Configuration:

Whitelist specific origins (frontend domain)
Allow credentials if using cookies
Limit allowed methods (GET, POST, PATCH, DELETE)
Set max age for preflight caching
External API Security
API Key Management:

Development:

Use .env file (gitignored)
Document required keys in .env.example
Never commit real keys
Production:

Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
Rotate keys quarterly
Use separate keys per environment
Monitor for unauthorized usage
Groq API Security:

Store API key in secrets manager
Never log API key
Use HTTPS only
Monitor usage for anomalies
Set spending limits
Data Privacy and Compliance
Data Minimization:

Collect only necessary information
No sensitive data without explicit need
Clear data retention policy
User Rights:

Right to Access
Provide endpoint to export user data
Include all personal information and activity
Return in machine-readable format (JSON)
Right to Deletion
Endpoint to delete account and all data
Cascade delete: resumes, applications, match scores
Anonymize audit logs (replace user_id with "deleted_user")
Retain only what's legally required
Right to Explanation
All match scores come with explanations
Audit log shows decision factors
Users can query why they were/weren't matched
Data Encryption:

At Rest:

Database encryption (Neon provides this)
File storage encryption (S3 with SSE)
Encrypt sensitive fields additionally if needed (PII)
In Transit:

TLS 1.3 for all connections
Certificate validation
No fallback to unencrypted
Audit Logging:

What to Log:

All authentication events (success/failure)
All authorization failures
Resume and job CRUD operations
Application status changes
Admin actions
LLM API calls with inputs/outputs
Match score computations
What NOT to Log:

Passwords (hashed or plain)
API keys or tokens
Full resume content (log reference only)
Sensitive PII unless necessary
Log Retention:

Security logs: 1 year minimum
Audit logs: 3 years (compliance)
Application logs: 90 days
Debug logs: 7 days
Incident Response Plan
Security Incident Types:

Data Breach
Immediately revoke all tokens
Notify affected users within 72 hours
Force password reset
Investigate root cause
Report to authorities if required
API Key Leak
Immediately rotate compromised key
Analyze usage logs for unauthorized access
Notify API provider
Review access controls
Account Takeover
Lock affected account
Notify user via verified channel
Investigate login history
Force password reset
DDoS Attack
Enable rate limiting at edge
Use CDN DDoS protection
Scale infrastructure if needed
Block malicious IPs
Communication Plan:

Internal: Alert dev team immediately
Users: Notify affected users within 72 hours
Public: Transparency report if widespread
Authorities: As required by law
8. Scalability Considerations
Scalability Requirements
Growth Projections:

Phase 1 (Months 1-6): Small Scale

Users: 1,000 candidates, 50 recruiters
Resumes: 1,000 total, ~5-10 per day
Jobs: 100 total, ~2-3 per day
Applications: ~50 per day
Match computations: ~500 per day
Phase 2 (Months 6-12): Medium Scale

Users: 10,000 candidates, 500 recruiters
Resumes: 10,000 total, ~50 per day
Jobs: 1,000 total, ~20 per day
Applications: ~500 per day
Match computations: ~5,000 per day
Phase 3 (Year 2+): Large Scale

Users: 100,000+ candidates, 5,000+ recruiters
Resumes: 100,000+ total, ~500+ per day
Jobs: 10,000+ total, ~200+ per day
Applications: ~5,000+ per day
Match computations: ~50,000+ per day
Horizontal Scaling Strategy
Stateless Components (Easy to Scale):

API Servers:

Run multiple instances behind load balancer
Use platform auto-scaling (Railway, Render)
Scale based on CPU or request count
No shared state (all state in database/cache)
Celery Workers:

Add worker instances as queue depth increases
Each worker pulls from same Redis queue
Scale based on queue length and processing time
Different worker pools for different task types (future)
Frontend:

Served via CDN (Vercel handles this)
Infinite scalability at edge
No scaling concerns
Stateful Components (Harder to Scale):

PostgreSQL Database:

Neon provides automatic scaling
Use read replicas for analytics queries
Partition large tables (match_scores) if needed
Consider sharding by tenant if multi-tenant (future)
Redis Cache/Queue:

Upstash provides scaling
Use Redis Cluster if self-hosted
Separate instances for cache vs. queue (optional)
Database Optimization
Index Strategy:

Essential Indexes (Create Early):

Primary keys on all tables (automatic)
Foreign keys for joins (user_id, job_id, etc.)
Status fields for filtering (resumes.status, jobs.status)
Timestamp fields for sorting (created_at)
Composite index on (job_id, candidate_id) for match lookups
Deferred Indexes (Add When Needed):

Full-text search indexes (when search is slow)
JSONB GIN indexes (when querying nested JSON)
Partial indexes (e.g., only active jobs)
Query Optimization:

Use EXPLAIN ANALYZE for slow queries
Avoid N+1 queries (use joins or eager loading)
Paginate all list endpoints
Use database connection pooling
Set statement timeout to prevent runaway queries
Table Partitioning:

When to Partition:

match_scores table exceeds 10M rows
events table exceeds 100M rows
Query performance degrades despite indexes
Partition Strategy:

match_scores: Partition by created_at (monthly)
events: Partition by created_at (weekly or monthly)
Automatically archive old partitions to cold storage
Caching Strategy
Cache Layers:

Layer 1: Application Cache (Redis)

Match scores (1 hour TTL)
User session data
Rate limiting counters
Job listings (5 minutes TTL)
Layer 2: Database Query Cache

Enabled by Neon automatically
Benefits read-heavy queries
Layer 3: CDN Cache (Frontend)

Static assets (long TTL)
API responses for public data (short TTL)
Cache Invalidation Strategy:

Time-Based (TTL):

Good for: Job listings, match scores
Simple to implement
May serve stale data briefly
Event-Based:

Good for: User profile data, resume data
Invalidate cache when entity updated
More complex but always fresh
Hybrid:

Use TTL as safety net
Invalidate on update events
Best of both worlds
Cache Warming:

Precompute match scores for new jobs
Background task to populate cache
Improves first-view experience
Asynchronous Processing
When to Use Workers:

Resume parsing (always)
Job description analysis (always)
Batch match computation (optional)
Email notifications (when implemented)
Report generation (when implemented)
Data export (when implemented)
Worker Pool Configuration:

Small Scale:

2-4 workers
Single queue
Process all task types
Medium Scale:

8-16 workers
Separate queues by priority
High: parsing, Medium: matching, Low: cleanup
Large Scale:

50+ workers
Separate worker pools by task type
Dedicated pools for parsing, matching, notifications
Auto-scaling based on queue metrics
Queue Management:

Monitor queue depth
Alert if queue depth > 100 for > 10 minutes
Set task timeouts to prevent hanging
Use dead letter queue for failures
Load Balancing
API Load Balancing:

Use platform load balancer (Railway, Render)
Round-robin or least-connections algorithm
Health checks every 30 seconds
Remove unhealthy instances
Database Connection Pooling:

SQLAlchemy pool size: 5-10 per API instance
Max overflow: 10
Pool recycle: 3600 seconds
Connection timeout: 30 seconds
Performance Monitoring
Key Metrics to Track:

Response Time:

API endpoint latency (p50, p95, p99)
Database query time
LLM API call time
Worker task duration
Throughput:

Requests per second
Resumes parsed per hour
Match scores computed per minute
Resource Utilization:

CPU usage per service
Memory usage per service
Database connections in use
Redis memory usage
Business Metrics:

Active users
Daily active candidates/recruiters
Application conversion rate
Average match score
Alerting Thresholds:

API latency p95 > 2 seconds
Error rate > 5%
Worker queue depth > 100
Database CPU > 80%
LLM API error rate > 10%
Cost Optimization
Infrastructure Costs:

Fixed Costs:

Neon database: ~$20-50/month
Upstash Redis: ~$10-30/month
Backend hosting: ~$20-50/month
Frontend (Vercel): Free tier initially
Variable Costs:

Groq API: Pay per token (~$0.10-1.00 per 1M tokens)
File storage: ~$0.02 per GB
Bandwidth: Usually included in platform pricing
Optimization Strategies:

Use efficient prompts to reduce tokens
Compress and cache responses
Archive old data to cheaper storage
Use spot instances for workers (if applicable)
Right-size infrastructure (don't over-provision)
9. Observability Strategy
Logging Architecture
Log Aggregation Flow:

[API Server] → [stdout/stderr] → [Platform Logger] → [Log Service]
[Workers] → [stdout/stderr] → [Platform Logger] → [Log Service]
[Frontend] → [Browser Console] → [Error Tracking Service]
Structured Logging Format (JSON):

{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO",
  "service": "api",
  "request_id": "abc-123",
  "user_id": "uuid",
  "endpoint": "/api/resumes/upload",
  "method": "POST",
  "status_code": 201,
  "duration_ms": 150,
  "message": "Resume uploaded successfully",
  "metadata": {
    "resume_id": "uuid",
    "file_size": 1048576
  }
}
Log Levels Usage:

DEBUG:

Detailed variable values
Function entry/exit
Development debugging
Not enabled in production
INFO:

User actions (login, upload, apply)
Task start/complete
Normal operation events
Main production log level
WARNING:

Deprecated API usage
Slow query detected
Cache miss on important data
Approaching rate limits
ERROR:

Failed API calls
Database errors
LLM parsing failures
Validation errors
Requires investigation
CRITICAL:

Service cannot start
Database unreachable
Complete system failure
Immediate action required
Metrics Collection
Metrics to Collect:

Request Metrics:

http_requests_total (counter): Total requests by endpoint, method, status
http_request_duration_seconds (histogram): Request latency distribution
http_requests_in_flight (gauge): Active concurrent requests
Database Metrics:

db_queries_total (counter): Total queries by table, operation
db_query_duration_seconds (histogram): Query execution time
db_connections_active (gauge): Active database connections
db_connections_idle (gauge): Idle connections in pool
Worker Metrics:

celery_tasks_total (counter): Tasks by name, status (success/failure)
celery_task_duration_seconds (histogram): Task execution time
celery_queue_length (gauge): Number of tasks waiting
celery_workers_active (gauge): Number of active workers
Business Metrics:

resumes_uploaded_total (counter): Total resumes uploaded
resumes_parsed_total (counter): Successfully parsed resumes
jobs_created_total (counter): Jobs posted
applications_submitted_total (counter): Applications
match_scores_computed_total (counter): Match computations
LLM Metrics:

llm_api_calls_total (counter): Calls by provider (groq/ollama), status
llm_tokens_used_total (counter): Tokens consumed
llm_cost_usd_total (counter): Estimated cost
llm_api_duration_seconds (histogram): API call latency
Distributed Tracing
Trace Spans:

Request Trace Example:

HTTP Request [200ms total]
├─ Authentication [10ms]
├─ Database Query [30ms]
│  └─ Connection Acquire [5ms]
├─ Celery Task Enqueue [5ms]
└─ Response Serialization [5ms]
Worker Task Trace Example:

Resume Parse Task [25s total]
├─ File Download [2s]
├─ PDF Text Extraction [3s]
├─ LLM API Call [15s]
│  ├─ Prompt Construction [0.5s]
│  ├─ Network Request [14s]
│  └─ Response Parsing [0.5s]
├─ Skill Normalization [2s]
└─ Database Update [3s]
Implementation:

Use OpenTelemetry for instrumentation
Automatic tracing for HTTP and database
Manual spans for business logic
Export to Jaeger or similar
Dashboard Design
Dashboard 1: System Health

Purpose: Real-time system status

Panels:

Request rate (requests/second)
Error rate (% of requests)
Response time percentiles (p50, p95, p99)
Active users
Worker queue depth
Database connections
Memory and CPU usage
Refresh: 30 seconds

Dashboard 2: Business Metrics

Purpose: Product usage and trends

Panels:

Daily active users (candidates vs. recruiters)
Resumes uploaded (per hour, per day)
Jobs posted (per day)
Applications submitted (per day)
Match score distribution
Top skills in demand
Conversion funnel (view → apply)
Refresh: 5 minutes

Dashboard 3: Worker Performance

Purpose: Async task monitoring

Panels:

Queue length by priority
Task success/failure rate
Task duration by type
Worker pool utilization
Retry count distribution
Dead letter queue depth
Refresh: 1 minute

Dashboard 4: LLM Usage

Purpose: AI cost and quality tracking

Panels:

API calls per hour (by provider)
Token usage (input vs. output)
Estimated cost (daily, monthly)
API error rate
Average response time
Fallback usage rate (Groq → Ollama)
Refresh: 5 minutes

Error Tracking
Error Capture:

Use Sentry or similar service
Capture uncaught exceptions
Group errors by fingerprint
Include context: user_id, request_id, stack trace
Attach breadcrumbs (recent logs)
Error Severity:

Fatal: System cannot continue
Error: Operation failed but system continues
Warning: Unexpected condition
Info: Contextual information
Error Notifications:

Critical errors: Immediate alert
High-volume errors: Alert if > 10/minute
New error types: Notify on first occurrence
Error trends: Alert if error rate increases 2x
Alerting Rules
Critical Alerts (Immediate Action):

Service Down
Condition: Health check fails for 2 minutes
Action: Page on-call engineer
Channels: PagerDuty, SMS
Database Unreachable
Condition: Cannot connect for 1 minute
Action: Page on-call engineer
Channels: PagerDuty, SMS
Error Rate Spike
Condition: Error rate > 25% for 5 minutes
Action: Alert team
Channels: Slack, Email
Warning Alerts (Investigate Soon):

High Latency
Condition: p95 latency > 2s for 10 minutes
Action: Investigate performance
Channels: Slack
Queue Backup
Condition: Queue depth > 100 for 10 minutes
Action: Check worker health, consider scaling
Channels: Slack
LLM Budget Alert
Condition: 80% of monthly budget consumed
Action: Review usage, consider optimizations
Channels: Email
Info Alerts (Awareness):

Deployment Complete
Condition: New version deployed
Action: Monitor for errors
Channels: Slack
Daily Summary
Condition: Daily at 9 AM
Action: Review metrics
Channels: Email
10. Deployment Architecture
Environment Strategy
Three Environments:

Development (Local):

Purpose: Developer testing
Database: Local PostgreSQL in Docker
Redis: Local Redis in Docker
LLM: Ollama only (no Groq)
Deployment: Manual, run locally
Staging:

Purpose: Integration testing, demo
Database: Neon (separate instance)
Redis: Upstash (separate instance)
LLM: Groq with lower quotas
Deployment: Auto-deploy from develop branch
URL: staging.hiringplatform.com
Production:

Purpose: Live users
Database: Neon (production instance)
Redis: Upstash (production instance)
LLM: Groq with full quotas
Deployment: Auto-deploy from main branch after approval
URL: app.hiringplatform.com
Deployment Pipeline
CI/CD Workflow:

On Pull Request:

Run linters (Black, ESLint, Prettier)
Run type checks (mypy, TypeScript)
Run unit tests
Run integration tests
Build Docker images (verify builds)
Comment results on PR
On Merge to develop:

All PR checks pass
Build and tag images (develop-{sha})
Deploy to staging environment
Run smoke tests
Notify team in Slack
On Merge to main:

Require approval from maintainer
Build and tag images (v{version} and latest)
Run database migrations
Deploy backend (rolling update)
Deploy workers (graceful restart)
Deploy frontend (instant via CDN)
Run smoke tests
Monitor error rates for 15 minutes
Rollback if error rate > 5%
Notify team of success/failure
Database Migrations
Migration Strategy:

Development:

Auto-generate migrations: alembic revision --autogenerate
Review and edit generated SQL
Test migration: alembic upgrade head
Test rollback: alembic downgrade -1
Commit migration file
Staging/Production:

Run migrations before deploying code
Automated in CI/CD pipeline
Create database backup before migration
Test rollback plan
Backwards Compatibility:

Additive changes safe (new tables, columns)
Removals require two-phase deploy:
Phase 1: Deploy code that doesn't use old column
Phase 2: Drop column in next release
Renames require alias period
Migration Checklist:

 Migration tested locally
 Rollback tested locally
 Backwards compatible or two-phase planned
 Indexes created concurrently (for large tables)
 Migration runs in < 1 minute (or scheduled maintenance)
 Backup verified before production run
Container Configuration
Backend Dockerfile:

Base image: Python 3.11 slim
Copy requirements.txt
Install dependencies
Copy application code
Expose port 8000
Health check endpoint: /health
Command: uvicorn app.main:app --host 0.0.0.0
Worker Dockerfile:

Base image: Python 3.11 slim
Same dependencies as backend
Copy application code
Command: celery -A app.tasks worker --loglevel info
Frontend Dockerfile (optional):

Build stage: Node 18, run npm build
Serve stage: nginx or serve static files
Copy build artifacts
Expose port 3000
Monitoring Deployment Health
Health Check Endpoints:

Backend: GET /health

{
  "status": "healthy",
  "version": "1.2.3",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "workers": "ok"
  }
}
Frontend: GET /health

{
  "status": "healthy",
  "version": "1.2.3"
}
Smoke Tests (Post-Deploy):

Health endpoint returns 200
Login endpoint accepts valid credentials
Job list endpoint returns data
Resume upload returns 201 (with test file)
Database connection successful
Redis connection successful
Rollback Strategy
Automated Rollback Triggers:

Error rate > 10% for 5 minutes
Health check fails
Smoke tests fail
Manual Rollback:

Command: Revert to previous deployment
Database: Rollback migration if needed
Verification: Run smoke tests
Duration: < 5 minutes
Rollback Checklist:

 Identify issue (logs, errors, metrics)
 Decide to rollback or hotfix
 Trigger rollback via platform or script
 Verify rollback successful (health checks)
 Communicate to team and users
 Post-mortem scheduled
11. Open Questions and Decisions
Before Implementation
1. Skill Taxonomy

Question: How many sample resumes and job descriptions are available for building the initial skill mapping?

Considerations:

Need minimum 100-200 resumes to identify common skills
Different domains have different skill sets (SWE vs. Data Science)
Synonyms need real-world examples
Decision Needed:

Start with curated list (e.g., 100 software engineering skills)?
Crowdsource from early users?
Use existing taxonomy (O*NET, LinkedIn skills)?
2. Resume Parsing Requirements

Question: Which fields must be required in resume JSON for scoring to run?

Options:

Strict: Require name, email, at least 1 skill, education
Lenient: Only require at least 1 skill
Flexible: Accept partial data, score what's available
Implications:

Strict: Higher quality, but more parse failures
Lenient: Lower quality matches, confusing scores
Flexible: Best UX, but complex scoring logic
Recommendation: Flexible approach with clear score disclaimers

3. File Upload Constraints

Question: What are allowed file size and accepted formats for resume upload?

Proposed:

File size: 5MB maximum (generous for PDFs)
Formats: PDF only (for MVP)
Future: DOCX, TXT support
Validation:

Check magic bytes for PDF
Reject corrupted files
Warn if file > 2MB (might have images)
4. Skill Normalization

Question: How strict should skill normalization be when synonyms conflict?

Example Conflict:

"React" and "React Native" both map to "React"?
"Python" and "Python 3" should they be separate?
Options:

Conservative: Keep separate if any ambiguity
Aggressive: Merge aggressively (React Native → React)
Context-aware: Use LLM to disambiguate
Recommendation: Conservative initially, refine based on feedback

5. Admin Dashboard Metrics

Question: Which metrics should be visible in admin dashboard for launch?

Must-Have:

Total users (candidates, recruiters)
Resumes uploaded, parsed, failed
Jobs posted, active
Applications submitted
Parse success rate
Worker queue depth
Error rate
Nice-to-Have:

Top skills in demand
Average match scores
Application conversion rate
LLM cost tracking
Recommendation: Start with must-haves, add nice-to-haves iteratively

During Development
6. Match Score Caching Strategy

Question: Should match scores be computed on-demand or precomputed?

On-Demand:

Pros: Always fresh, saves computation
Cons: Slow first page load
Precomputed:

Pros: Fast UX, can rank all candidates
Cons: Expensive, may be stale
Hybrid:

Compute on first view, cache for 1 hour
Background job to precompute for active candidates
Best of both worlds
Recommendation: Hybrid approach

7. Explanation Generation

Question: Use LLM for all explanations or template-based for cost?

LLM-Generated:

Pros: Natural, personalized
Cons: Costs $0.001-0.01 per explanation
Template-Based:

Pros: Free, fast, consistent
Cons: Robotic, less engaging
Hybrid:

Templates for low scores (< 50)
LLM for medium/high scores (50+)
Reduces cost, maintains quality where it matters
Recommendation: Start with LLM, fall back to templates if budget tight

8. Real-Time Updates

Question: Should candidates see parse progress in real-time?

Options:

Polling: Frontend polls every 2-5 seconds
WebSockets: Real-time bidirectional connection
Email: Notify when complete
Recommendation: Polling for MVP (simple), WebSockets later (better UX)

Post-Launch
9. Feedback Loop

Question: How to collect user feedback on match quality?

Ideas:

Thumbs up/down on match explanations
"Report incorrect match" button
Survey after 10 applications
Track which matches lead to applications
Recommendation: Implicit tracking (application rate by score) + explicit feedback option

10. Feature Prioritization

Question: What features to build after MVP?

Candidate Requests:

Resume editing after parse
Skill endorsements
Application tracking dashboard
Interview scheduling
Recruiter Requests:

Bulk job posting
Team collaboration
Custom screening questions
Integration with ATS
Platform Improvements:

Mobile app
Better analytics
AI-powered job recommendations
Salary insights
Recommendation: Prioritize based on user feedback and usage data

Conclusion
This architecture document provides a comprehensive blueprint for implementing the Hiring Intelligence Platform. It covers:

✅ Component architecture with clear responsibilities

✅ Data models with detailed schemas and relationships

✅ Sequence flows for all major user journeys

✅ Matching algorithm with transparent, explainable logic

✅ LLM integration with prompts, validation, and cost management

✅ Security measures at every layer

✅ Scalability planning from small to large scale

✅ Observability with logging, metrics, and alerting

✅ Deployment strategy with CI/CD and rollback plans

✅ Open questions to guide decision-making

Next Steps:

Review and validate assumptions with stakeholders
Answer open questions to finalize requirements
Set up infrastructure (Neon, Upstash, Groq accounts)
Create project structure and initial boilerplate
Build MVP focusing on core flows first
Test with real users and iterate based on feedback
Scale gradually following the patterns outlined here
This is a living document—update it as the system evolves and new patterns emerge.