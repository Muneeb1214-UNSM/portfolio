import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

load_dotenv()

# --- AGENT FUNCTION ---
async def run_browser_agent(api_key, task):
    if not api_key or not task:
        return "❌ Please provide both API Key and Task."

    try:
        # API Key set karein
        os.environ["OPENAI_API_KEY"] = api_key
        
        # LLM aur Browser Configuration
        llm = ChatOpenAI(model="gpt-4o")
        
        # Hackathon Demo ke liye: headless=False (taake browser chalta nazar aaye)
        # Agar cloud pe deploy kar rahe hain to True kar dein
        browser = Browser(config=BrowserConfig(headless=True)) 
        
        agent = Agent(task=task, llm=llm, browser=browser)
        
        # Agent ko run karein
        history = await agent.run()
        
        # Result extract karein
        return history.final_result()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Gradio ko async function chalane ke liye wrapper chahiye
def gradio_wrapper(api_key, task):
    return asyncio.run(run_browser_agent(api_key, task))

# --- GRADIO UI DESIGN ---
with gr.Blocks(theme=gr.themes.Soft(), title="AI Browser Agent") as demo:
    gr.Markdown("# 🌐 Omni-Agent: Web Executive")
    gr.Markdown("Aapka apna AI Agent jo browser control karta hai.")
    
    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(
                label="OpenAI API Key", 
                placeholder="sk-...", 
                type="password"
            )
            task_input = gr.Textbox(
                label="Aapka Hukum?", 
                placeholder="e.g. Search for the cheapest flights from London to Paris next week.",
                lines=3
            )
            run_btn = gr.Button("Execute Task 🚀", variant="primary")
        
        with gr.Column():
            output_display = gr.Textbox(
                label="Agent's Final Report", 
                lines=10,
                interactive=False
            )

    # Button Click Logic
    run_btn.click(
        fn=gradio_wrapper, 
        inputs=[api_key_input, task_input], 
        outputs=output_display
    )

    gr.Markdown("---")
    gr.Markdown("💡 **Tip:** Agar aap apne laptop pe demo de rahe hain, to code mein `headless=False` kar dein taake judges ko browser chalta nazar aaye!")

# --- LAUNCH ---
if __name__ == "__main__":
    # share=True karne se aapko ek temporary public link mil jayega
    demo.launch(share=True)
