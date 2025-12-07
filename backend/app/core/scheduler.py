from datetime import date, timedelta

def schedule_tasks(tasks):
    current = date.today()
    for t in tasks:
        t["start_date"] = current
        current += timedelta(days=t["estimated_days"])
        t["end_date"] = current
    return tasks
