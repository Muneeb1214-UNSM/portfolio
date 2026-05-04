import os
import asyncio
import subprocess
import streamlit as st

# --- Playwright Browser Download ---
@st.cache_resource
def setup_playwright():
    try:
        # Chromium install karein
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Browser installation failed: {e}")

setup_playwright()

# Ab imports (Jab libraries requirements.txt se install ho jayengi)
try:
    from browser_use import Agent, Browser, BrowserConfig
    from langchain_openai import ChatOpenAI
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    st.error(f"Library Import Error: {e}. Please check requirements.txt.")

# --- UI Setup ---
st.set_page_config(page_title="AI Web Agent", page_icon="🤖")
st.title("🤖 Vision AI Browser Agent")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Aap kya karwana chahte hain?", placeholder="e.g. Open Google and search for AI news.")

async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    browser = Browser(config=BrowserConfig(headless=True))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    return result

if st.button("Run Agent 🚀"):
    if not api_key:
        st.error("API Key dalein!")
    elif not user_task:
        st.warning("Task likhein!")
    else:
        try:
            with st.status("Agent kaam kar raha hai...", expanded=True):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                st.success("Task Complete!")
                st.write(final_result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
