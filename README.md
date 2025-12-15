# 🧠 Smart Task Planner  
**AI-assisted Goal-to-Execution Planning System**

---

## 📌 Project Overview

Smart Task Planner is a **backend-driven application** that converts high-level user goals into **structured, actionable task plans** with timelines, status tracking, and persistence.

The project emphasizes **workflow orchestration, backend system design, and state management**, using an LLM only as a **supporting component** for task generation rather than the core logic.

---

## 🎯 Problem Statement

People often know *what* they want to achieve but struggle to:

- Break goals into executable tasks  
- Assign realistic timelines  
- Track progress over time  
- Store and reuse plans  

This project addresses that gap by transforming **unstructured goals into manageable execution plans**, backed by a persistent backend system.

---

## 🏗️ System Architecture
```
┌──────────────────────┐
│   Streamlit Frontend │
│   (Presentation)     │
│──────────────────────│
│ • Goal Input UI      │
│ • Plan Selection     │
│ • Task Status Update│
│ • PDF Export Trigger│
└─────────▲────────────┘
          │ HTTP (REST)
          ▼
┌────────────────────────────┐
│      FastAPI Backend       │
│   (Application Layer)     │
│────────────────────────────│
│ 1. API Layer               │
│    • Request Validation    │
│    • Routing               │
│    • Error Handling        │
│                            │
│ 2. Business Logic Layer    │
│    • Goal → Task Workflow  │
│    • Timeline Scheduling   │
│    • Status Transitions    │
│    • PDF Generation        │
│                            │
│ 3. Integration Layer       │
│    • LLM Client (Groq)     │
│    • Database ORM          │
└─────────▲───────────▲─────┘
          │           │
          │           │
          ▼           ▼
┌────────────────┐   ┌──────────────────────┐
│  MySQL Database│   │   Groq LLM Service   │
│ (Persistence)  │   │  (Task Generation)  │
│────────────────│   │──────────────────────│
│ • Plans        │   │ • Goal → Raw Tasks   │
│ • Tasks        │   │ • No Business Logic  │
│ • Status State │   │ • Stateless Calls   │
└────────────────┘   └──────────────────────┘
```

### Component Responsibilities

- **Frontend (Streamlit)**  
  User interaction, plan selection, task status updates, and exports.

- **Backend (FastAPI)**  
  Business logic, task lifecycle management, scheduling, and persistence.

- **Database (MySQL + SQLAlchemy)**  
  Storage for plans, tasks, and status states.

- **LLM (Groq – LLaMA 3.1)**  
  Generates the *initial task breakdown only*.

---

## 🔑 Core Design Philosophy

> **The AI generates task ideas — the system owns everything else.**

All critical logic such as:
- task scheduling  
- status transitions  
- database persistence  
- updates and deletions  
- PDF export  

is **deterministic and backend-controlled**, not handled by the LLM.

---

## ✨ Key Features

- AI-assisted task generation from user-defined goals  
- Automatic timeline assignment using Python date logic  
- Task lifecycle management  
  *(Not Started → In Progress → Completed)*  
- Persistent storage of plans and tasks using MySQL  
- REST APIs to update, delete, and retrieve plans  
- Export complete plans as downloadable PDFs  
- Clean separation of frontend and backend responsibilities  

---

## 🧠 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MySQL |
| ORM & Validation | SQLAlchemy, Pydantic |
| AI Model | Groq – llama-3.1-8b-instant |
| PDF Export | ReportLab |

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/plan/` | Generate and store a new plan |
| GET | `/plan/all` | Retrieve all saved plans |
| PATCH | `/plan/task/{task_id}/status` | Update task status |
| DELETE | `/plan/{plan_id}` | Delete a plan |
| GET | `/plan/export/pdf/{plan_id}` | Export plan as PDF |

---

## 🔄 Application Flow

1. User submits a goal via the UI  
2. Backend requests an initial task breakdown from the LLM  
3. Tasks are scheduled and structured  
4. Data is persisted in MySQL  
5. Users can update task status, export, or delete plans  

---

## 🧪 Usage

- Enter a goal and generate a plan  
- Select stored plans from the dropdown  
- Update task statuses as work progresses  
- Export plans as PDFs for sharing or offline use  
- Delete plans when no longer needed  

---

## 🚀 Future Enhancements

- User authentication and per-user plan isolation  
- Async task generation for long or complex plans  
- Deployment with role-based access control  

---

## 🧠 What This Project Demonstrates

- Backend API design and data modeling  
- Workflow and state management  
- Practical integration of LLMs into deterministic systems  
- Separation of concerns in full-stack applications  
- Building usable,
