import os
import asyncio
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()

# Playwright install command (locally ya server par)
import subprocess
import sys

def setup_browser():
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])

setup_browser()

# --- AGENT FUNCTION ---
async def run_omni_agent(api_key, user_goal):
    if not api_key:
        return "Error: Please provide an OpenAI API Key."
    
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Brain: GPT-4o use karenge jo sabse aqalmand hai
    llm = ChatOpenAI(model="gpt-4o")
    
    # Browser: Headless=False taake demo ke waqt judges ko nazar aaye
    # (Agar deployment hai to Headless=True kar dein)
    browser = Browser(config=BrowserConfig(headless=True)) 
    
    agent = Agent(
        task=user_task,
        llm=llm,
        browser=browser
    )

    try:
        # Agent task shuru karega
        result = await agent.run()
        # Final result extraction
        return result.final_result()
    except Exception as e:
        return f"Error: {str(e)}"

# --- GRADIO UI (Professional Look) ---
def start_task(api_key, task):
    return asyncio.run(run_omni_agent(api_key, task))

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌐 Omni-Agent: Autonomous Web Executive")
    gr.Markdown("Complex tasks dain, agent browser khud handle karega.")
    
    with gr.Row():
        with gr.Column():
            key_input = gr.Textbox(label="OpenAI API Key", placeholder="sk-...", type="password")
            task_input = gr.Textbox(label="What do you want the agent to do?", 
                                    placeholder="e.g. Find the best laptop under 1 lakh on different Pak sites and compare.")
            btn = gr.Button("Execute Task 🚀", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(label="Agent's Final Report", lines=10)

    btn.click(fn=start_task, inputs=[key_input, task_input], outputs=output)

if __name__ == "__main__":
    demo.launch()
