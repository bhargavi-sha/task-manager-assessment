Task Manager System
Overview

This is a small full-stack task management system built using:

Backend: Python + Flask

Frontend: React

Database: SQLite (relational via SQLAlchemy)

The system enforces controlled state transitions and validates business rules to prevent invalid states.

Architecture

The backend follows a layered architecture:

models/      → Database schema
services/    → Business rules and validation
routes/      → HTTP API layer
tests/       → Automated verification
ai_guidance/ → AI constraints and governance

Design Principle

Business rules are isolated in the service layer.
Routes do not directly modify database state.

This ensures:

Predictable behavior

Safer modifications

Clear separation of responsibilities

Task State Machine

Tasks follow a strict state progression:

PENDING → IN_PROGRESS

IN_PROGRESS → COMPLETED

Invalid transitions are rejected with explicit errors.

Example:

Cannot move from IN_PROGRESS to PENDING


This prevents invalid system states.

Correctness & Interface Safety

The system enforces:

Enum-based task status

Controlled state transitions

Validation of due dates

Structured JSON error responses

No direct database manipulation from routes

Verification

Automated tests verify:

Task creation

Valid state transitions

Invalid state transitions

Tests run using an in-memory SQLite database to ensure isolation.

Command:

pytest

Observability

Failures return explicit structured JSON responses.

Example:

{
  "error": "Cannot move from IN_PROGRESS to PENDING"
}


This makes errors diagnosable and visible.

AI Usage

AI tools were used to:

Scaffold initial project structure

Generate boilerplate code

Suggest testing patterns

All AI-generated code was manually reviewed and verified using automated tests.

AI behavior was constrained using guidance files located in:

backend/ai_guidance/


These files define:

Architectural boundaries

Coding standards

System constraints

Tradeoffs

SQLite chosen for simplicity.

No authentication implemented.

Minimal UI (focus was correctness, not polish).

Extension Approach

Future improvements could include:

User authentication

Task ownership

Pagination

Soft delete support

Database migrations

Logging and monitoring

Because business logic is isolated in services, new features can be added without impacting the entire system.
How to Run
Backend
cd backend
pip install -r requirements.txt
python app.py

Frontend
cd frontend
npm install
npm start