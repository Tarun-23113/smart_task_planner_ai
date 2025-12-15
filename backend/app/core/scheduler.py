from datetime import date, timedelta


def schedule_tasks(tasks):
    current = date.today()
    for t in tasks:
        t["start_date"] = current
        t["end_date"] = current + timedelta(days=t["estimated_days"] - 1)
        
        # Next task starts the day after
        current = t["end_date"] + timedelta(days=1)
    return tasks
