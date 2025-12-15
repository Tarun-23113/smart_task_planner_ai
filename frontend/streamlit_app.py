import streamlit as st
import requests

BACKEND_URL = "http://localhost:8001"

st.set_page_config(page_title="Smart Task Planner", layout="wide")
st.title("🧠 Smart Task Planner")

if "initialized" not in st.session_state:
    resp = requests.get(f"{BACKEND_URL}/plan/all")
    st.session_state["plans"] = resp.json() if resp.status_code == 200 else []
    st.session_state["current_plan"] = None
    st.session_state["initialized"] = True

st.header("Create a New Plan")
goal = st.text_area("Enter your goal", height=100)

if st.button("Generate Plan"):
    response = requests.post(f"{BACKEND_URL}/plan/", json={"goal": goal})
    if response.status_code == 200:
        st.success("🎯 Plan generated successfully!")

        refreshed = requests.get(f"{BACKEND_URL}/plan/all").json()
        st.session_state["plans"] = refreshed
        st.session_state["current_plan"] = refreshed[-1] if len(
            refreshed) else None
    else:
        st.error("Failed to generate plan")

st.header("📦 View Plans")

if len(st.session_state["plans"]) > 0:
    plan_names = ["— Select —"] + [
        f"Plan {p['plan_id']} — {p['goal']}" for p in st.session_state["plans"]
    ]

    if st.session_state["current_plan"]:
        current_name = f"Plan {st.session_state['current_plan']['plan_id']} — {st.session_state['current_plan']['goal']}"
        default_index = plan_names.index(
            current_name) if current_name in plan_names else 0
    else:
        default_index = 0

    selected = st.selectbox(
        "Select a plan to view",
        plan_names,
        index=default_index
    )

    if selected != "— Select —":
        selected_plan = next(
            p for p in st.session_state["plans"]
            if f"Plan {p['plan_id']} — {p['goal']}" == selected
        )

        st.subheader(f"📝 {selected_plan['goal']}")

        pdf_url = f"{BACKEND_URL}/plan/export/pdf/{selected_plan['plan_id']}"
        if st.button("📄 Export PDF", key=f"pdf-{selected_plan['plan_id']}"):
            st.write(pdf_url)

        for task in selected_plan["tasks"]:
            with st.container(border=True):
                st.markdown(f"""
                **{task['id']} — {task['name']}**

                📄 *{task['description']}*

                ⏳ **Estimated Days:** `{task['estimated_days']}`
                🗓 **Start:** `{task['start_date']}`
                🏁 **End:** `{task['end_date']}`
                """)

                status = st.selectbox(
                    "Status",
                    ["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress",
                           "Completed"].index(task["status"]),
                    key=f"status-{task['task_db_id']}"
                )

                if st.button("Update Status", key=f"update-{task['task_db_id']}"):
                    update = requests.patch(
                        f"{BACKEND_URL}/plan/task/{task['task_db_id']}/status",
                        params={"status": status}
                    )
                    if update.status_code == 200:
                        st.success("Updated!")
                        refreshed = requests.get(
                            f"{BACKEND_URL}/plan/all").json()
                        st.session_state["plans"] = refreshed
                    else:
                        st.error("Failed to update")
else:
    st.info("No plans yet. Create one above.")

st.header("🗑 Delete Plan")

if len(st.session_state["plans"]) > 0:
    delete_options = [
        f"Plan {p['plan_id']} — {p['goal']}" for p in st.session_state["plans"]]

    delete_selected = st.selectbox(
        "Select a plan to delete", delete_options, key="delete_dropdown")

    if st.button("Delete Selected Plan"):
        delete_id = int(delete_selected.split(" ")[1])

        resp = requests.delete(f"{BACKEND_URL}/plan/{delete_id}")

        if resp.status_code == 200:
            st.success(f"Plan {delete_id} deleted!")

            refreshed = requests.get(f"{BACKEND_URL}/plan/all").json()
            st.session_state["plans"] = refreshed
            st.session_state["current_plan"] = refreshed[-1] if len(
                refreshed) else None
        else:
            st.error("Failed to delete plan")
else:
    st.info("No plans available to delete.")
