import asyncio
from lmnt.api import Speech
from openai import AsyncOpenAI
import os

SYSTEM_PROMPT = open('system_prompts/nervous_style.txt').read()
RESUME = open('resume/sam_altman.txt').read()

# VOICE_ID = '26b0c713-0d5b-476f-af0a-1eeb3278b362'  # Sam Altman
# VOICE_ID = 'b8fb49dc-623d-427a-a6db-8840babccca7'  # Sam Altman
VOICE_ID = 'ava'
os.environ['LMNT_API_KEY'] = '2b4e75c1e1b34aa287a78152394e316e'
os.environ['OPENAI_API_KEY'] = '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'

async def main():
  async with Speech() as speech:
    connection = await speech.synthesize_streaming(VOICE_ID)
    t1 = asyncio.create_task(reader_task(connection))
    t2 = asyncio.create_task(writer_task(connection))
    await asyncio.gather(t1, t2)


async def reader_task(connection):
  """Streams audio data from LMNT and writes it to `output.mp3`."""
  with open('output.mp3', 'wb') as f:
    async for message in connection:
      f.write(message['audio'])
    #   print('wrote audio', end='', flush=True)


async def writer_task(connection):
    """Streams text from ChatGPT to LMNT."""
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ['OPENAI_API_KEY'],
    )
    response = await client.chat.completions.create(
        model='openai/gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': RESUME}
        ],
        stream=True)

    async for chunk in response:
        if (not chunk.choices[0] or
            not chunk.choices[0].delta or
            not chunk.choices[0].delta.content):
          continue
        content = chunk.choices[0].delta.content
        await connection.append_text(content)
        print(content, end='', flush=True)

    # After `finish` is called, the server will close the connection
    # when it has finished synthesizing.
    await connection.finish()


asyncio.run(main())
