import json
from weather_agent.client import get_client_and_model
from weather_agent.prompts import build_system_prompt
from weather_agent.tools.weather import TOOL_FUNCTIONS
from weather_agent.schemas import TOOL_MENU
from weather_agent.config import MAX_TURNS, MAX_TOKENS

def run_agent_turns(messages: list, max_turns: int = MAX_TURNS) -> str:
    client, model, _ = get_client_and_model()
    working = [{"role": "system", "content": build_system_prompt()}, *messages]
    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=model, messages=working, tools=TOOL_MENU,
            tool_choice="auto", max_tokens=MAX_TOKENS, temperature=0.2
        )
        message = response.choices[0].message
        calls = message.tool_calls or []
        if not calls:
            answer = message.content or "I couldn't generate a response."
            messages.append({"role": "assistant", "content": answer})
            return answer
        working.append({
            "role": "assistant", "content": message.content,
            "tool_calls": [{
                "id": c.id, "type": "function",
                "function": {"name": c.function.name, "arguments": c.function.arguments}
            } for c in calls]
        })
        for call in calls:
            try:
                args = json.loads(call.function.arguments or "{}")
                if call.function.name not in TOOL_FUNCTIONS:
                    result = {"error": f"Unknown tool: {call.function.name}"}
                else:
                    result = TOOL_FUNCTIONS[call.function.name](**args)
            except Exception as exc:
                result = {"error": f"Tool failed: {type(exc).__name__}: {exc}"}
            working.append({"role": "tool", "content": json.dumps(result), "tool_call_id": call.id})
    fallback = "Stopped after reaching the maximum number of tool rounds."
    messages.append({"role": "assistant", "content": fallback})
    return fallback
