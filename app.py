import os
import asyncio
import subprocess
import streamlit as st
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv

# API Key load karein
load_dotenv()

# --- STEP 1: PLAYWRIGHT BROWSER DOWNLOAD ---
# Ye sirf browser dhoondta hai, install nahi karta library ko
@st.cache_resource
def setup_playwright():
    try:
        # Check if already installed to save time
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Browser Setup Error: {e}")

# Run setup
setup_playwright()

# --- STEP 2: UI SETUP ---
st.set_page_config(page_title="AI Web Agent", page_icon="🤖")
st.title("🤖 Vision AI Browser Agent")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])
    st.info("Task khatam hone par video record ho kar niche aa jayegi.")

user_task = st.text_area("Aap kya karwana chahte hain?", placeholder="e.g. Open Google and search for latest AI news.")

# --- STEP 3: AGENT LOGIC ---
async def run_agent(task, key, model):
    llm = ChatOpenAI(model=model, api_key=key)
    # Cloud ke liye headless=True hona lazmi hai
    browser = Browser(config=BrowserConfig(headless=True))
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    return result

# --- STEP 4: EXECUTION ---
if st.button("Run Agent 🚀"):
    if not api_key:
        st.error("Pehle OpenAI API Key sidebar mein dalein!")
    elif not user_task:
        st.warning("Kuch command to likhein!")
    else:
        try:
            with st.status("Agent kaam kar raha hai (Video record ho rahi hai)...", expanded=True) as status:
                # Video folder ensure karein
                if not os.path.exists("./videos"):
                    os.makedirs("./videos")
                
                # Async loop handle karna
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_result = loop.run_until_complete(run_agent(user_task, api_key, model_name))
                
                status.update(label="✅ Task Complete!", state="complete")
                st.success("Result:")
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
st.caption("Hackathon Project | Powered by browser-use")
