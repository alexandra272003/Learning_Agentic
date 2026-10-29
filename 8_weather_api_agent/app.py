import streamlit as st
from weather_agent.agent import run_agent_turns
from weather_agent.client import get_client_and_model
from weather_agent.prompts import build_greeting_prompt, build_system_prompt

st.set_page_config(page_title="Weather Agent", page_icon="🌦️")
with st.sidebar:
    st.header("About this project")
    st.markdown(build_greeting_prompt())
    st.divider()
    st.subheader("Provider")
    try:
        _, model, provider = get_client_and_model()
        st.success(f"Provider: {provider.name} (model: {model})")
    except RuntimeError as exc:
        st.error(str(exc))
    st.divider()
    with st.expander("Preview system prompt"):
        st.code(build_system_prompt(), language="markdown")
    if st.button("Clear chat"):
        st.session_state.chat_log = []
        st.rerun()

st.title("🌦️ Weather Agent")
st.caption("Current weather powered by Open-Meteo and Groq tool calling.")
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
for entry in st.session_state.chat_log:
    if entry.get("content"):
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
prompt = st.chat_input("Weather in Varanasi, London, Tokyo...")
if prompt:
    st.session_state.chat_log.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Checking weather..."):
            try:
                answer = run_agent_turns(st.session_state.chat_log)
            except Exception as exc:
                answer = f"**Error:** `{type(exc).__name__}` — {exc}"
            st.markdown(answer)
