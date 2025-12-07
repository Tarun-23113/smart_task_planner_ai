# 🧠 Smart Task Planner

Smart Task Planner converts user goals into structured, actionable tasks with timelines and status tracking.

---

## 🌟 About the Project

The application allows users to submit a goal, and an AI model generates a list of tasks.  
A scheduling algorithm then assigns estimated dates based on duration values.  
Users can generate, view, update, store and export plans easily through an interactive interface.

---

## ✨ Key Features

- AI-generated task breakdown from user goals
- Automatic timeline assignment using Python date logic
- Task status updates: **Not Started → In Progress → Completed**
- Save and load plans from a MySQL database
- Export generated plans to PDF
- Select and delete specific plans
- Simple UI to generate, view, update, store and export plans easily

---

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | MySQL + SQLAlchemy |
| ORM & Schema Validation | SQLAlchemy + Pydantic |
| AI Task Generation | Groq - llama-3.1-8b-instant |
| PDF Export | ReportLab |

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| `POST` | `/plan/` | Generate new task plan |
| `GET` | `/plan/all` | Get all saved plans |
| `PATCH` | `/plan/task/{task_id}/status` | Update a task's status |
| `DELETE` | `/plan/{plan_id}` | Delete a specific plan |
| `GET` | `/plan/export/pdf/{plan_id}` | Export plan as PDF |

---

## 🧪 How to Use

1. Enter a goal and press **Generate Plan**
2. Select a plan from the dropdown to view complete plan and tasks
3. Update status for tasks.
4. Export to PDF to save or share the plan
5. Delete a specific plan if not needed

---

## 📦 Deliverables Included

- Working backend API with database integration
- Streamlit UI for user-friendly interaction
- AI-based task generation using Groq
- Scheduling logic for timelines
- PDF export feature

---

## 🔮 Future Improvements

- Deploy the application and add user authentication so each user can securely save and access their own plans.    

---


My focus was on building a practical and understandable solution.

---

Thank you for reviewing this project.     
Suggestions and improvements are always welcome.

---


## To Clone and Run in your machine

- Create a MySQL Database with name *smart_planner*
- Create a .env file in root folder with GROQ_API_KEY=*your_api_key_here*
- After this in one terminal enter into backend using `cd backend`, then run backend server `uvicorn app.main:app --reload`
- Create a new terminal enter into frontend using `cd frontend`, then run `streamlit run streamlit_main.py`
