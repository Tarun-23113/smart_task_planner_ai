from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.database import get_db
from app.schemas import PlanRequest
from app.model import Plan, TaskModel
from app.core.llm import generate_task_plan
from app.core.scheduler import schedule_tasks
from reportlab.pdfgen import canvas

plan_router = APIRouter(prefix="/plan", tags=["Planning"])

@plan_router.post("/")
def create_plan(request: PlanRequest, session: Session = Depends(get_db)):
    raw_tasks = generate_task_plan(request.goal)
    tasks = schedule_tasks(raw_tasks)

    plan = Plan(goal=request.goal)
    session.add(plan)
    session.commit()
    session.refresh(plan)

    for idx, t in enumerate(tasks, start=1):
        task = TaskModel(
            task_code=f"T{idx}",
            name=t["name"],
            description=t["description"],
            depends_on=",".join(t.get("depends_on", [])) if t.get("depends_on") else None,
            estimated_days=t["estimated_days"],
            start_date=t["start_date"],
            end_date=t["end_date"],
            plan_id=plan.id
        )
        session.add(task)

    session.commit()

    return {"message": "Plan created", "plan_id": plan.id, "goal": request.goal}


@plan_router.get("/all")
def get_all(session: Session = Depends(get_db)):
    plans = session.query(Plan).all()
    result = []

    for p in plans:
        tasks = session.query(TaskModel).filter(TaskModel.plan_id == p.id).all()
        result.append({
            "plan_id": p.id,
            "goal": p.goal,
            "tasks": [
                {
                    "task_db_id": t.id,
                    "id": t.task_code,
                    "name": t.name,
                    "description": t.description,
                    "depends_on": t.depends_on.split(",") if t.depends_on else [],
                    "estimated_days": t.estimated_days,
                    "start_date": t.start_date.isoformat(),
                    "end_date": t.end_date.isoformat(),
                    "status": t.status
                } for t in tasks
            ],
        })

    return result


@plan_router.patch("/task/{task_id}/status")
def update_status(task_id: int, status: str, session: Session = Depends(get_db)):
    task = session.get(TaskModel, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    session.commit()
    return {"message": "Status updated"}


@plan_router.delete("/clear")
def clear_all(session: Session = Depends(get_db)):
    session.query(TaskModel).delete()
    session.query(Plan).delete()
    session.commit()
    return {"message": "All plans cleared"}


@plan_router.get("/export/pdf/{plan_id}")
def export_pdf(plan_id: int, session: Session = Depends(get_db)):
    plan = session.get(Plan, plan_id)
    tasks = session.query(TaskModel).filter(TaskModel.plan_id == plan_id).all()

    filename = f"plan_{plan_id}.pdf"
    pdf = canvas.Canvas(filename)
    y = 800
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, f"Plan #{plan_id}: {plan.goal}")
    y -= 30

    pdf.setFont("Helvetica", 12)
    for t in tasks:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"{t.task_code} — {t.name}  [{t.status}]")
        y -= 20

        pdf.setFont("Helvetica", 10)
        pdf.drawString(60, y, f"Description: {t.description}")
        y -= 15

        pdf.drawString(60, y, f"Depends On: {t.depends_on if t.depends_on else 'None'}")
        y -= 15

        pdf.drawString(60, y, f"Estimated Days: {t.estimated_days}")
        y -= 15

        pdf.drawString(60, y, f"Start: {t.start_date}   End: {t.end_date}")
        y -= 25

        if y < 60:  # Move to new page if reaching bottom
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 800

    pdf.save()

    return FileResponse(filename, media_type="application/pdf", filename=filename)

@plan_router.delete("/{plan_id}")
def delete_plan(plan_id: int, session: Session = Depends(get_db)):
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    session.delete(plan)
    session.commit()
    return {"message": f"Plan {plan_id} deleted"}
