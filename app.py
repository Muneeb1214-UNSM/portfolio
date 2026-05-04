import os
import subprocess
import sys
import asyncio

# --- AUTO-INSTALLER (Agar requirements.txt fail ho jaye) ---
def install_package(package):
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", package])

# Zaroori libraries install karein
install_package("browser-use")
install_package("langchain-openai")
install_package("playwright")

import streamlit as st

# --- PLAYWRIGHT BROWSER INSTALL ---
@st.cache_resource
def setup_browser():
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    subprocess.run([sys.executable, "-m", "playwright", "install-deps"])

setup_browser()

# Ab imports karein
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Web Agent", page_icon="🌐")
st.title("🌐 AI Browser Agent")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Aap kya karwana chahte hain?", placeholder="e.g. Open Google and search for latest news.")

async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    # Headless mode is MUST for cloud
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
