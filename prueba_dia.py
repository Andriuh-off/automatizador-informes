import json
import pandas as pd
import ollama
from pathlib import Path

CARPETA = Path(__file__).parent

MODELO = "llama3.2:3b"

INSTRUCCIONES = (
    "Eres un asistente que redacta informes de prácticas preprofesionales en español. "
    "Recibes un título y notas breves de un día de trabajo y las conviertes en 2 o 3 "
    "párrafos formales, en voz impersonal y tiempo pasado (Se realizó..., Asimismo, se..., "
    "Posteriormente, se...). "
    "REGLAS ESTRICTAS: usa únicamente la información de las notas. "
    "No agregues resultados, beneficios, mejoras ni consecuencias que no estén en las notas. "
    "No repitas la misma idea en párrafos distintos. "
    'Responde únicamente con JSON: {"parrafos": ["...", "..."]}'
)

EJEMPLO_ENTRADA = (
    "Título: Familiarización con la plataforma estudiantil\n"
    "Notas: exploré Moodle: funciones, herramientas, usuarios, cursos y recursos"
)
EJEMPLO_SALIDA = json.dumps({"parrafos": [
    "Se realizó un proceso de familiarización con la plataforma estudiantil basada en Moodle, "
    "explorando sus principales funciones, herramientas y opciones disponibles.",
    "Esta actividad permitió conocer la estructura de la plataforma y comprender los "
    "procedimientos relacionados con la administración de usuarios, cursos, actividades y "
    "demás recursos utilizados por la institución.",
]}, ensure_ascii=False)


def redactar_dia(titulo, notas):
    respuesta = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": INSTRUCCIONES},
            {"role": "user", "content": EJEMPLO_ENTRADA},
            {"role": "assistant", "content": EJEMPLO_SALIDA},
            {"role": "user", "content": f"Título: {titulo}\nNotas: {notas}"},
        ],
        format="json",
        options={"temperature": 0.1},
    )
    return json.loads(respuesta["message"]["content"])["parrafos"]


actividades = pd.read_excel(CARPETA / "informe_datos.xlsx", sheet_name="actividades")
fila = actividades.iloc[2]  # 28 de agosto

print(f"{fila['fecha']} – {fila['titulo']}\n")
for parrafo in redactar_dia(fila["titulo"], fila["notas"]):
    print(parrafo, "\n")