import os
import asyncio
import subprocess
import streamlit as st

# --- Playwright Browser Download ---
@st.cache_resource
def setup_browser():
    try:
        # Browser install karne ki koshish
        subprocess.run(["playwright", "install", "chromium"], check=True)
        subprocess.run(["playwright", "install-deps"], check=True)
    except Exception as e:
        st.warning(f"Note: Browser setup issues: {e}")

setup_browser()

# Imports (Requirements install hone ke baad)
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Web Agent", page_icon="🌐")
st.title("🌐 AI Browser Agent")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

user_task = st.text_area("Aap kya karwana chahte hain?", placeholder="e.g. Open Wikipedia and search for Einstein.")

async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    # Headless mode is required for Streamlit Cloud
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
            with st.status("Agent kaam kar raha hai...", expanded=True) as status:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                
                status.update(label="✅ Task Complete!", state="complete")
                st.success("Result niche dekhein:")
                st.write(final_result)
                
                # Check for video recording
                video_dir = "./videos"
                if os.path.exists(video_dir):
                    videos = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
                    if videos:
                        latest_video = max([os.path.join(video_dir, f) for f in videos], key=os.path.getctime)
                        st.video(latest_video)
        except Exception as e:
            st.error(f"Error: {str(e)}")
