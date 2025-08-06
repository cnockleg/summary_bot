import os
import asyncio

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv('conf.env')
AI_TOKEN = os.getenv("API_TOKEN") 

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)

async def query(prompt: str):
  completion = await client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ]
  )
  # print(completion)
  print(completion.choices[0].message.content)
  return completion.choices[0].message.content

# await query(prompt=input())
asyncio.run(query(prompt='Привет'))
