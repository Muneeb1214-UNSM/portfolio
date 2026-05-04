import os
import subprocess
import sys
import asyncio

# --- AUTO-INSTALLER (Agar Streamlit Cloud fail ho jaye) ---
def install_libraries():
    try:
        import browser_use
        import langchain_openai
    except ImportError:
        # Agar libraries nahi milti, to hum manual install karenge lekin error handle karke
        subprocess.run([sys.executable, "-m", "pip", "install", "browser-use", "langchain-openai>=0.2.5", "playwright", "python-dotenv"])

# Install libraries before anything else
install_libraries()

import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# --- PLAYWRIGHT SETUP ---
@st.cache_resource
def setup_playwright():
    # Chromium aur uski dependencies install karna
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    # System dependencies ko skip karenge kyunki packages.txt handle karega

setup_playwright()

# Ab imports karein (Jab confirm ho jaye ke install ho gayi hain)
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()

# UI Setup
st.set_page_config(page_title="AI Browser Agent", page_icon="🤖")
st.title("🤖 Vision AI Web Agent")
st.info("Built for Hackathon | Stable Version 3.11")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Hukum karein?", placeholder="e.g. Open Google and search for latest AI news.")

async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    browser = Browser(config=BrowserConfig(headless=True))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    return result

if st.button("Run Agent 🚀"):
    if not api_key:
        st.error("Sidebar mein OpenAI API Key dalein!")
    elif not user_task:
        st.warning("Task likhein!")
    else:
        try:
            with st.status("AI Agent kaam kar raha hai (Video record ho rahi hai)...", expanded=True) as status:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                
                status.update(label="✅ Task Complete!", state="complete")
                st.success("Result:")
                st.write(final_result)
        except Exception as e:
            st.error(f"Error: {str(e)}")
