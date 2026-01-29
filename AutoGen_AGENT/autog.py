import warnings
warnings.filterwarnings("ignore")

import os
import autogen
import gradio as gr
from openai import OpenAI  
from dotenv import load_dotenv
from IPython.display import display, Markdown
import random  
import google.generativeai as genai  

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")  

print("Setup Complete: Libraries installed and API keys loaded.")

def print_markdown(text):
    display(Markdown(text))

config_list_openai = [
    {
        "model": "gpt-4o-mini",
        "api_key": openai_api_key,
    }
]

llm_config_openai = {
    "config_list": config_list_openai,
    "temperature": 0.7,  
    "timeout": 120,
}

cmo_prompt = """You are the Chief Marketing Officer (CMO) of a new shoe brand (sustainable).
Provide high-level strategy, define target audiences, and guide the Marketer. Focus on the big picture. Be concise."""

brand_marketer_prompt = """You are the Brand Marketer for the shoe brand. Brainstorm creative, specific campaign ideas (digital, content, experiences).
Focus on tactics and details. Suggest KPIs for your ideas."""

cmo_agent_openai = autogen.ConversableAgent(
    name = "Chief_Marketing_Officer_OpenAI",
    system_message = cmo_prompt,
    llm_config = llm_config_openai,  
    human_input_mode = "NEVER")

print(f"Agent '{cmo_agent_openai.name}' created (using OpenAI).")

brand_marketer_agent_openai = autogen.ConversableAgent(
    name = "Brand_Marketer_OpenAI",
    system_message = brand_marketer_prompt,
    llm_config = llm_config_openai,  
    human_input_mode = "NEVER")

print(f"Agent '{brand_marketer_agent_openai.name}' created (using OpenAI).")

initial_task_message = """
Context: We're launching a new sustainable shoe line and need campaign ideas
Instruction: Brainstorm a campaign concept with specific elements
Input: Our sustainable, futuristic shoe brand needs marketing direction
Output: A concise campaign concept with the following structure:
Brand Marketer, let's brainstorm initial campaign ideas for our new sustainable shoe line.
Give me a distinct campaign concept. Outline: core idea, target audience, primary channels, and 1-2 KPIs. Keep it concise. Try to arrive at a final answer in 2-3 turns.
"""

print("--- Starting Agent Conversation (OpenAI Only) ---")
print("Chief Marketing Officer (OpenAI) initiating chat with Brand Marketer (OpenAI). Max Turns = 4")
print("--------------------------------------------------")

chat_result_openai_only = cmo_agent_openai.initiate_chat(
    recipient = brand_marketer_agent_openai, message = initial_task_message, max_turns = 4
)

print("--------------------------------------------------")
print("--- Conversation Ended (OpenAI Only) ---")

def print_chat_history(chat_result):
    for i in chat_result.chat_history:  
        print_markdown(i['name'])
        print("_"*100)
        print_markdown(i['content'])
        print("_"*100)

print_chat_history(chat_result_openai_only)

config_list_gemini = [
    {
        "model": "gemini-2.0-flash",  
        "api_key": google_api_key,
        "api_type": "google",  
    }
]

llm_config_gemini = {
    "config_list": config_list_gemini,
    "temperature": 0.6,  
    "timeout": 120,
}

cmo_agent_gemini = autogen.ConversableAgent(
    name = "Chief_Marketing_Officer_Gemini",
    system_message = cmo_prompt,
    llm_config = llm_config_gemini,  
    human_input_mode = "NEVER")

brand_marketer_agent_openai_mixed = autogen.ConversableAgent(
    name = "Brand_Marketer_OpenAI",  
    system_message = brand_marketer_prompt,
    llm_config = llm_config_openai,  
    human_input_mode = "NEVER")

print(f"Agent '{cmo_agent_gemini.name}' created (using Google Gemini).")
print(f"Agent '{brand_marketer_agent_openai_mixed.name}' created (using OpenAI).")

print("--- Starting Agent Conversation (Multi-Model: Gemini + OpenAI) ---")
print("Chief Marketing Officer (Gemini) initiating chat with Brand Marketer (OpenAI). Max Turns = 4")
print("------------------------------------------------------------------")

chat_result_multi_model = cmo_agent_gemini.initiate_chat(
    recipient = brand_marketer_agent_openai_mixed,  
    message = initial_task_message,
    max_turns = 4)

print("------------------------------------------------------------------")
print("--- Conversation Ended (Multi-Model) ---")
print_chat_history(chat_result_multi_model)

user_proxy_agent = autogen.UserProxyAgent(
    name = "Human_User_Proxy",
    human_input_mode = "ALWAYS",  
    max_consecutive_auto_reply = 1,
    is_termination_msg = lambda x: x.get("content", "").rstrip().lower() in ["exit", "quit", "terminate"],
    code_execution_config = False,
    system_message = "You are the human user interacting with a multi-model AI team (Gemini CMO, OpenAI Marketer). Guide the brainstorm. Type 'exit' to end.",
)

print(f"Agent '{user_proxy_agent.name}' created for HIL with multi-model team.")

print("--- Starting Human-in-the-Loop (HIL) Conversation (Multi-Model) ---")
print("You will interact with Gemini CMO and OpenAI Marketer. Type 'exit' to end.")
print("---------------------------------------------------------------------")

cmo_agent_gemini.reset()  
brand_marketer_agent_openai_mixed.reset()  
user_proxy_agent.reset()

from autogen import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents = [user_proxy_agent, cmo_agent_gemini, brand_marketer_agent_openai],  
    messages = [ ],  
    max_round = 20,  
)

group_manager = GroupChatManager(groupchat = groupchat, llm_config = llm_config_openai)  

group_chat_result = group_manager.initiate_chat(
    recipient = user_proxy_agent,  
    message = """Hello team!!""",
)

print("---------------------------------------------------------------------")
print("--- Conversation Ended (Human terminated or Max Turns) ---")