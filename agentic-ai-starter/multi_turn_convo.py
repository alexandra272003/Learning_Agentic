import os
from pathlib import Path
from dotenv import load_dotenv
import json
from groq import Groq

# Load .env from the directory containing this Python file
load_dotenv(Path(__file__).resolve().parent / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"

tasks = [
    {"title": "Buy groceries", "completed": False},
    {"title": "Finish the project report", "completed": False},
    {"title": "Call the plumber", "completed": False},
    {"title": "Schedule a dentist appointment", "completed": False},
]

# Limit destructive operations during a single user turn.
turn_state = {"deletions": 0}


# ---------- Python tools ----------

def add_task(task: str) -> str:
    """Add one new task to the todo list."""
    task = task.strip()

    if not task:
        return "Task title cannot be empty."

    if any(t["title"].casefold() == task.casefold() for t in tasks):
        return f"Task already exists: {task}"

    tasks.append({"title": task, "completed": False})
    return f"Added task: {task}"


def delete_task(task: str) -> str:
    """Delete one uniquely matched task. Never delete the entire list."""
    if turn_state["deletions"] >= 1:
        return "Only one task can be deleted per request. Ask the user to make another request."

    if task.strip().casefold() in {
        "all", "all tasks", "everything", "*"
    }:
        return "Bulk deletion is disabled. Ask the user to select individual tasks."

    matches = [
        t for t in tasks
        if task.strip().casefold() in t["title"].casefold()
    ]

    if not matches:
        return f"No matching task found for: {task}"

    if len(matches) > 1:
        return "Multiple matches: " + ", ".join(
            t["title"] for t in matches
        ) + ". Ask the user which task to delete."

    deleted = matches[0]["title"]
    tasks.remove(matches[0])
    turn_state["deletions"] += 1

    return f"Deleted exactly one task: {deleted}"


def complete_task(task: str) -> str:
    """Mark one uniquely matched task as completed."""
    matches = [
        t for t in tasks
        if task.strip().casefold() in t["title"].casefold()
    ]

    if not matches:
        return f"No matching task found for: {task}"

    if len(matches) > 1:
        return "Multiple matches: " + ", ".join(
            t["title"] for t in matches
        ) + ". Ask the user which task to complete."

    matches[0]["completed"] = True
    return f"Completed: {matches[0]['title']}"


def get_tasks() -> str:
    """Retrieve the current todo list and completion status."""
    if not tasks:
        return "No tasks in the list."

    return "\n".join(
        f"- {t['title']} "
        f"[{'Completed' if t['completed'] else 'Pending'}]"
        for t in tasks
    )


# ---------- Tool definitions for Groq ----------

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task requested by the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task title to add."
                    }
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete one existing task requested by the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "A description of the task to delete."
                    }
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark one existing task as completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "A description of the task to complete."
                    }
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Retrieve the actual current todo list.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

available_functions = {
    "add_task": add_task,
    "delete_task": delete_task,
    "complete_task": complete_task,
    "get_tasks": get_tasks,
}


# ---------- Agent configuration ----------

system_instruction = """
You are a personal AI todo assistant.

Manage the user's todo list using the available tools.

Rules:
- Use tools to make actual changes to tasks.
- Never claim an operation succeeded unless its tool confirms it.
- Do not invent tasks or tool results.
- For ambiguous tasks, ask a clarification question.
- Never attempt to delete the entire list.
- Respect tool restrictions and results.
- If asked to list tasks, retrieve the actual current list.
- Help with prioritization when requested.
- Stay focused on todo management; do not provide unrelated
  sexual instructions or other out-of-scope advice.
- Never provide sexual guidance involving a child.
- Be concise, clear, and friendly.
"""

messages = [
    {"role": "system", "content": system_instruction}
]


# ---------- Agent loop ----------

print("Groq AI Todo Buddy")
print("Try: Add milk, delete the plumber task, mark report done.")
print("Type 'exit' to stop.")

while True:
    user_message = input("\nYou: ").strip()

    if user_message.casefold() in {"exit", "quit"}:
        print("Goodbye!")
        break

    if not user_message:
        continue

    turn_state["deletions"] = 0
    messages.append({"role": "user", "content": user_message})

    try:
        for _ in range(5):  # Prevent an endless tool-call loop
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=1024,
            )

            assistant_message = response.choices[0].message

            # Preserve the assistant's tool-call message in history.
            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            if not assistant_message.tool_calls:
                print(
                    "\nAssistant:",
                    assistant_message.content or "No response generated."
                )
                break

            for tool_call in assistant_message.tool_calls:
                name = tool_call.function.name

                try:
                    args = json.loads(tool_call.function.arguments)
                    function = available_functions.get(name)

                    if function is None:
                        result = f"Unknown tool: {name}"
                    else:
                        result = function(**args)

                except (ValueError, TypeError, json.JSONDecodeError):
                    result = "Invalid tool arguments. No operation performed."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": str(result),
                })

        else:
            print("\nAssistant: I reached the tool-call limit. Please try again.")

    except Exception as error:
        # Remove the failed user turn and any incomplete tool-call messages
        # so the next request does not inherit a broken conversation.
        messages = messages[:1] + [
            m for m in messages[1:]
            if m.get("role") not in {"assistant", "tool"}
        ]

        # Keep the application running after API errors.
        print(f"\nAPI error: {error}")
        print("Your local todo list remains available.")
