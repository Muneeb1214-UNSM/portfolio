import os
import asyncio
import subprocess
import streamlit as st

# --- PLAYWRIGHT SETUP ---
@st.cache_resource
def setup_browser():
    # Sirf browser download karein (libraries requirements.txt se aayengi)
    subprocess.run(["playwright", "install", "chromium"])

setup_browser()

# Imports
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

load_dotenv()

# UI
st.set_page_config(page_title="AI Agent", page_icon="🤖")
st.title("🤖 Vision AI Web Agent")

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Hukum karein?", placeholder="e.g. Search for latest news on Google")

async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    browser = Browser(config=BrowserConfig(headless=True))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    return result

if st.button("Run Agent 🚀"):
    if not api_key:
        st.error("API Key bhool gaye aap!")
    elif not user_task:
        st.warning("Task to likhein!")
    else:
        try:
            with st.status("Agent kaam kar raha hai..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                st.success("Done!")
                st.write(final_result)
        except Exception as e:
            st.error(f"Masla aa gaya: {str(e)}")
