import streamlit as st
import pandas as pd
import datetime as dt
import sqlite3

# Create a connection to the database
conn = sqlite3.connect('todo.db')

# Create a table for the to-do items if it doesn't exist
conn.execute('''CREATE TABLE IF NOT EXISTS todos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              task TEXT,
              due_date DATE,
              status TEXT)''')

# Define a function to insert a new task into the database
def add_task(task, due_date):
    conn.execute("INSERT INTO todos (task, due_date, status) VALUES (?, ?, ?)", (task, due_date, "Incomplete"))
    conn.commit()

# Define a function to retrieve all the tasks from the database
def get_tasks():
    df = pd.read_sql_query("SELECT * from todos", conn)
    return df

# Define a function to update a task's status
def update_status(id, status):
    conn.execute("UPDATE todos SET status = ? WHERE id = ?", (status, id))
    conn.commit()

# Define a function to delete a task from the database
def delete_task(id):
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()

# Define the Streamlit app
def app():
    st.set_page_config(page_title="To-Do List App")
    st.title("To-Do List App")

    # Create a form for adding a new task
    with st.form(key="add_task"):
        st.write("Add a new task:")
        task = st.text_input("Task")
        due_date = st.date_input("Due date", value=dt.date.today())
        submitted = st.form_submit_button("Add task")

        if submitted:
            add_task(task, due_date)
            st.success("Task added!")

    st.write("## Current Tasks")

    # Display the list of tasks
    tasks_df = get_tasks()
    if len(tasks_df) == 0:
        st.write("No tasks found.")
    else:
        for index, task in tasks_df.iterrows():
            st.write(f"{task['task']} (due {task['due_date']})")
            status = task['status']
            if status == "Incomplete":
                new_status = "Complete"
            else:
                new_status = "Incomplete"
            update_button = st.button(f"Mark as {new_status}", key=f"update_{task['id']}")
            if update_button:
                update_status(task['id'], new_status)
                st.success(f"Task '{task['task']}' marked as {new_status}.")
            delete_button = st.button("Delete", key=f"delete_{task['id']}")
            if delete_button:
                delete_task(task['id'])


# Run the Streamlit app
if __name__ == '__main__':
    app()
