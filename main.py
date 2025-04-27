import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, AsyncOpenAI
import os
from dotenv import load_dotenv, find_dotenv
# env Api key finder
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Provider
gemini_provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# Agent
greeting_agent = Agent(
    name="Greeting Agent",
    instructions="A simple agent that greets the user.",
    model = OpenAIChatCompletionsModel(
        model = "gemini-2.0-flash", openai_client = gemini_provider),
)
# Agent Loop
@cl.on_message
async def main(message: cl.Message):
    ai_response = await Runner.run(starting_agent = greeting_agent, input = message.content)
    await cl.Message(
        content = ai_response.final_output,
        ).send()