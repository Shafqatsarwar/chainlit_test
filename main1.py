import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import chainlit as cl
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
# Agent
greeting_agent = Agent(
    name="Greeting Agent",
    instructions="A simple agent that greets the user.",
    model = model
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(
        content="Thinking ...")
    await msg.send()
    print("\n Step 1 : Get History and add User message \n")

    history = cl.user_session.get("history")
    print("\n Step 2 : Add User message to history \n")

    history.append({"role": "user", "content": message.content})
    print("\n Step 3 : Updated History \n")

    agent_response = await Runner.run(greeting_agent, history)
    msg.content = agent_response.final_output
    await msg.update()

    history.append({"role": "assistant", "content": agent_response.final_output})