import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const API = "http://127.0.0.1:5000/tasks/";



  const fetchTasks = async () => {
    const res = await axios.get(API);
    setTasks(res.data);
  };

  const createTask = async () => {
    if (!title.trim()) return;

    await axios.post(API, {
      title: title,
      description: "",
      due_date: "2026-02-20"
    });

    setTitle("");
    fetchTasks();
  };

  const updateStatus = async (id, status) => {
    await axios.put(`http://127.0.0.1:5000/tasks/${id}/status`, {
      status: status
    });
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ padding: 30 }}>
      <h1>Task Manager</h1>

      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task"
      />
      <button onClick={createTask}>Create</button>

      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title} - {task.status}
            {task.status === "PENDING" && (
              <button onClick={() => updateStatus(task.id, "IN_PROGRESS")}>
                Start
              </button>
            )}
            {task.status === "IN_PROGRESS" && (
              <button onClick={() => updateStatus(task.id, "COMPLETED")}>
                Complete
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
