import asyncio
from lmnt.api import Speech
from openai import AsyncOpenAI
import os

SYSTEM_PROMPT = '''
# Resume to Silicon Valley Monologue Transformer

You are a GPT that takes a user's resume or work experience as input and transforms it into ONE continuous paragraph of over-the-top Silicon Valley style narrative. When a user shares their professional background, you focus on their most recent role/experience and convert it into an exaggerated first-person Silicon Valley story.

## Input Processing
- Focus on the most recent position/experience from the provided resume
- Extract key responsibilities and achievements
- Identify technical skills and tools used
- Note team size and growth metrics if available

## Output Requirements
You MUST generate only ONE continuous paragraph that:
1. Uses first-person perspective throughout
2. Focuses only on the most recent work experience
3. Incorporates all Silicon Valley elements naturally
4. Maintains a single flowing narrative
5. Length should be 200-300 words
6. Start directly with the narrative (no "Real talk" or similar prefaces)

## Required Story Elements (Must All Appear in Single Paragraph)
- 4:30 AM routine reference
- Silicon Valley coffee shop mention (Blue Bottle/Philz)
- At least two tech buzzwords (AI/ML/blockchain/neural networks)
- Growth metrics ("10x" or "exponential")
- Wellness activity (meditation/Peloton/cold plunge)
- Valley phrases ("let me double-click," "sync")
- First principles thinking reference
- Team/product scaling mention

## Response Rules
1. ONLY output the transformed narrative paragraph
2. NO additional explanations or commentary
3. NO bullet points or lists
4. Keep all Silicon Valley elements regardless of original resume content
5. Maintain consistent first-person perspective
6. Ensure narrative flows naturally despite required elements
7. Start paragraph immediately without any preface phrases
8. Don't use "Real talk" or similar opening phrases

Remember: Your ONLY response should be ONE continuous paragraph transforming the user's recent work experience into an exaggerated Silicon Valley narrative.

'''
RESUME = '''
# Samuel H. Altman
## Chief Executive Officer, OpenAI
San Francisco Bay Area, California

---

### Professional Summary
Pioneering technology executive and entrepreneur with extensive experience in artificial intelligence, startup acceleration, and venture capital. Known for transformative leadership in AI development and commitment to ensuring AI benefits humanity.

### Professional Experience

**OpenAI**
*Chief Executive Officer (2019 - Present)*
- Led development and deployment of groundbreaking AI models including GPT-4
- Scaled organization from research lab to multi-billion dollar company
- Established partnerships with Microsoft and other major tech companies
- Advanced responsible AI development practices and safety measures
- Brief departure and return in November 2023 marked significant corporate governance changes

**Y Combinator**
*President (2014 - 2019)*
- Transformed YC into the world's premier startup accelerator
- Grew portfolio value to over $100B
- Mentored and funded over 2,000 startups
- Initiated programs like Startup School and the YC Growth Program
- Expanded YC's international presence and diversity initiatives

**Loopt**
*Co-Founder & CEO (2005 - 2012)*
- Founded location-based social networking company at age 19
- Raised over $30M in venture capital
- Scaled to millions of users
- Successfully sold to Green Dot Corporation for $43.4M

### Board Positions & Advisory Roles
- Microsoft (Board Member, 2023 - Present)
- Reddit (Former Board Member)
- Retro Biosciences (Co-Founder & Investor)
- Helion Energy (Board Member)
- Various technology and biotech companies (Advisor)

### Education
**Stanford University**
- Computer Science (2003 - 2005)
- Left to pursue entrepreneurial ventures

### Investments & Ventures
Notable investments and founding roles in:
- Stripe
- Reddit
- Airbnb
- Pinterest
- Various AI, biotechnology, and clean energy companies

### Publications & Thought Leadership
- Regular speaker at major technology conferences
- Author of numerous articles on AI, startups, and technology
- Frequent contributor to discussions on AI safety and ethics

### Areas of Expertise
- Artificial Intelligence Leadership
- Corporate Strategy
- Startup Development
- Venture Capital
- Technology Innovation
- Corporate Governance
- Public Speaking
- Strategic Partnerships

### Languages
- English (Native)

### Notable Achievements
- Listed in TIME 100 Most Influential People
- Forbes 30 Under 30
- MIT Technology Review's 35 Innovators Under 35
- Successfully navigated OpenAI through significant growth and challenges
- Pioneered responsible AI development frameworks

---
*References available upon request*

'''

VOICE_ID = '26b0c713-0d5b-476f-af0a-1eeb3278b362'
VOICE_ID = 'b8fb49dc-623d-427a-a6db-8840babccca7'
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
