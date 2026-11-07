import drawpyo

drawpyo.register_mxlibrary(
    "developer",
    "https://raw.githubusercontent.com/jgraph/drawio-libs/refs/heads/main/libs/integration/developer.xml",
)

file = drawpyo.File()
file.file_path = "docs"
file.file_name = "arquitectura.drawio"
page = drawpyo.Page(file=file)

VERDE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;strokeWidth=3;fontSize=13;fontStyle=1;"
MORADO = "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=3;fontSize=13;fontStyle=1;"
NARANJA = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=3;fontSize=13;fontStyle=1;"
TITULO = "text;html=1;fontSize=34;fontStyle=1;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=3;rounded=1;"

def caja(nombre, texto, estilo, pos, icono=None):
    o = drawpyo.diagram.Object(page=page, value=texto)
    o.apply_style_string(estilo)
    o.position = pos
    if icono:
        drawpyo.diagram.object_from_library(
            page=page, library="developer", obj_name=icono,
            position=(pos[0] + 45, pos[1] - 55))
    return o

titulo = caja("t", "<b>Report Generator — Arquitectura</b>", TITULO, (120, 20))

cliente = caja("c", "Cliente<br/>Navegador", VERDE, (40, 200))
api     = caja("a", "API<br/>Express/TS", VERDE, (280, 200), "App Developing")
cola    = caja("q", "Cola BullMQ<br/>Redis", MORADO, (520, 200))
worker  = caja("w", "Worker<br/>Python", VERDE, (760, 200))
llm     = caja("l", "DeepSeek<br/>LLM", NARANJA, (760, 380))
got     = caja("g", "Gotenberg<br/>HTML→PDF", NARANJA, (520, 380))
s3      = caja("s", "Silo / S3<br/>PDFs", MORADO, (280, 380))

def flecha(a, b, etiqueta, punteada=False):
    e = drawpyo.diagram.Edge(page=page, source=a, target=b, value=etiqueta)
    e.apply_style_string(
        f"endArrow=block;strokeWidth=2;strokeColor=#333333;fontSize=11;"
        f"labelBackgroundColor=#ffffff;{'dashed=1;' if punteada else ''}")
    return e

flecha(cliente, api, "POST /report")
flecha(api, cola, "encola")
flecha(cola, worker, "consume")
flecha(worker, llm, "prompt")
flecha(worker, got, "HTML")
flecha(got, worker, "PDF", punteada=True)
flecha(worker, s3, "put_object")

file.write()
