from pydantic import BaseModel, Field

class ReportJob(BaseModel):
    task_id: str = Field(alias='taskId', min_length=1, max_length=64)
    topic: str = Field(alias='msg', min_length=3, max_length=2000)
    language: str = 'español'
    audience: str = 'público general interesado en el tema'
    length: str = 'unas 1200 palabras'
    start_date: str = ''
    end_date: str = ''
    model_config = {'populate_by_name': True}

class Section(BaseModel):
    heading: str
    body: str
    bullets: list[str] = Field(default_factory=list)

class Report(BaseModel):
    title: str
    subtitle: str
    executive_summary: str
    sections: list[Section] = Field(min_length=3, max_length=8)
    conclusion: str
    sources: list[str] = Field(default_factory=list)

INSTRUCTIONS = """Redactas reportes claros e informativos en {language} para {audience}.
Adapta el enfoque al tema solicitado: puede pertenecer a cualquier área, como ciencia,
tecnología, salud, educación, historia, cultura, sociedad, medio ambiente o negocios.
No fuerces un enfoque comercial ni incluyas métricas, recomendaciones empresariales o
lenguaje de negocio, salvo que sean pertinentes al tema.

Organiza el contenido como un informe general: presenta una síntesis inicial, desarrolla
los aspectos más relevantes y termina con una conclusión adecuada al tema. Usa las
secciones y viñetas cuando ayuden a la claridad; no inventes un formato de negocio.
Extensión: {length}. Markdown plano en los campos, sin HTML ni bloques de código.
Distingue hechos, estimaciones e interpretaciones. Sustenta las afirmaciones relevantes;
si no tienes certeza o información actualizada, indícalo. No inventes cifras, citas ni fuentes."""