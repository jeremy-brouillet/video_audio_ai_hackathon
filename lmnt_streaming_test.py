import asyncio
from lmnt.api import Speech
from openai import AsyncOpenAI
import os

RESUME = open('resume/sam_altman.txt').read()

# VOICE_ID = '26b0c713-0d5b-476f-af0a-1eeb3278b362'  # Sam Altman
# VOICE_ID = 'b8fb49dc-623d-427a-a6db-8840babccca7'  # Sam Altman
os.environ['LMNT_API_KEY'] = '2b4e75c1e1b34aa287a78152394e316e'
os.environ['OPENAI_API_KEY'] = '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'


async def process_single_input(speech, system_prompt, resume, output_file_path, voice_id):
    """Process a single input tuple using the speech connection."""
    connection = await speech.synthesize_streaming(voice_id)
    t1 = asyncio.create_task(reader_task(connection, output_file_path))
    t2 = asyncio.create_task(writer_task(connection, system_prompt, resume))
    await asyncio.gather(t1, t2)

async def main(input_tuples):
    """
    Process multiple input tuples concurrently.
    input_tuples: list of tuples, each containing (system_prompt, resume, output_file_path)
    """
    async with Speech() as speech:
        tasks = [
            process_single_input(speech, system_prompt, resume, output_file_path, voice_id)
            for system_prompt, resume, output_file_path, voice_id in input_tuples
        ]
        await asyncio.gather(*tasks)


async def reader_task(connection, output_file_path):
  """Streams audio data from LMNT and writes it to `output.mp3`."""
  with open(output_file_path, 'wb') as f:
    async for message in connection:
      f.write(message['audio'])
    #   print('wrote audio', end='', flush=True)


async def writer_task(connection, system_prompt, resume):
    """Streams text from ChatGPT to LMNT."""
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ['OPENAI_API_KEY'],
    )
    response = await client.chat.completions.create(
        model='openai/gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': resume}
        ],
        stream=True)
    output_text = ''
    async for chunk in response:
        if (not chunk.choices[0] or
            not chunk.choices[0].delta or
            not chunk.choices[0].delta.content):
          continue
        content = chunk.choices[0].delta.content
        await connection.append_text(content)
        output_text += content

    print(output_text)

    # After `finish` is called, the server will close the connection
    # when it has finished synthesizing.
    await connection.finish()


input_tuples = [
    # prompt, resume, output_file_path, voice_id
    (
        open('system_prompts/nervous_2_style.txt').read(),
        RESUME,
        'output/4-12-pm-output-nervous.mp3',
        '26b0c713-0d5b-476f-af0a-1eeb3278b362' # Sam Altman Voice Clone
    ),
    (
        open('system_prompts/jargon_style.txt').read(),
        RESUME,
        'output/4-12-pm-output-jargon.mp3',
        'ava'
    ),
]

asyncio.run(main(input_tuples))
