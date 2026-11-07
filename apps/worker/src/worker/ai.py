import os

from pydantic_ai import Agent, UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIChatModelSettings
from pydantic_ai.providers.deepseek import DeepSeekProvider

from worker.config import settings
from worker.schemas import INSTRUCTIONS, Report, ReportJob

def build_agent(job: ReportJob) -> Agent:
    model = OpenAIChatModel(
        settings.ai_model,
        provider=DeepSeekProvider(api_key=os.environ['DEEPSEEK_API_KEY']),
    )
    return Agent(
        model,
        output_type=Report,
        retries={'output': 2},
        instructions=INSTRUCTIONS.format(
            language=job.language, audience=job.audience, length=job.length),
        # DeepSeek rechaza tool_choice forzado con thinking activo
        model_settings=OpenAIChatModelSettings(thinking=False),
    )

async def generate(job: ReportJob) -> Report:
    prompt = f'Tema del reporte: {job.topic}'
    if job.start_date and job.end_date:
        prompt += f'\nPeriodo a cubrir: {job.start_date} a {job.end_date}'
    agent = build_agent(job)
    async with agent:  # cierra el cliente HTTP del proveedor
        res = await agent.run(prompt, usage_limits=UsageLimits(
            request_limit=4, total_tokens_limit=settings.max_tokens))
    return res.output