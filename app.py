import os
import subprocess
import sys
import asyncio
import streamlit as st

# --- STEP 1: FORCE INSTALL LIBRARIES (Hackathon Fix) ---
def force_install():
    try:
        import browser_use
        import langchain_openai
    except ImportError:
        with st.spinner("Installing AI Engine... Please wait (This happens only once)."):
            # Hum specifically version conflicts ko bypass karne ke liye install kar rahe hain
            subprocess.run([sys.executable, "-m", "pip", "install", "langchain-openai>=0.2.5", "browser-use"], check=True)
            st.rerun()

# --- STEP 2: PLAYWRIGHT SETUP ---
def setup_playwright():
    if "playwright_ready" not in st.session_state:
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            st.session_state.playwright_ready = True
        except:
            pass

# Pehle installation check karein
force_install()
setup_playwright()

# Ab imports karein (Jab confirm ho jaye ke install ho gayi hain)
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# --- UI SETUP ---
st.set_page_config(page_title="Vision AI Agent", page_icon="🤖")
st.title("🤖 AI Browser Agent")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Aap kya karwana chahte hain?", placeholder="e.g. Open Google and search for latest AI news.")

# --- AGENT EXECUTION ---
async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    browser = Browser(config=BrowserConfig(headless=True))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    return result

if st.button("Run Agent 🚀"):
    if not api_key:
        st.error("API Key sidebar mein dalein!")
    elif not user_task:
        st.warning("Task likhein!")
    else:
        try:
            with st.status("Agent kaam kar raha hai... Video record ho rahi hai.", expanded=True):
                # Video folder ensure karein
                if not os.path.exists("./videos"):
                    os.makedirs("./videos")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                
                st.success("Task Mukammal!")
                st.write(final_result)
                
                # Latest video dhoond kar dikhayein
                if os.path.exists("./videos"):
                    videos = [f for f in os.listdir("./videos") if f.endswith(".mp4")]
                    if videos:
                        latest_video = max([os.path.join("./videos", f) for f in videos], key=os.path.getctime)
                        st.video(latest_video)
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
st.caption("Built for Hackathon | Vision Web Agent")
