import json
from pathlib import Path

import ollama
import pandas as pd

CARPETA = Path(__file__).parent
MODELO = "llama3.2:3b"

# ---------- Redacción de cada día (con ejemplo de estilo) ----------
INSTR_DIA = (
    "Eres un asistente que redacta informes de prácticas preprofesionales en español. "
    "Recibes un título y notas breves de un día de trabajo y las conviertes en 2 o 3 "
    "párrafos formales, en voz impersonal y tiempo pasado (Se realizó..., Asimismo, se..., "
    "Posteriormente, se...). "
    "REGLAS ESTRICTAS: usa únicamente la información de las notas. "
    "No agregues resultados, beneficios, mejoras ni consecuencias que no estén en las notas. "
    "No repitas la misma idea en párrafos distintos. "
    "Cuida la concordancia gramatical (por ejemplo: Se corrigieron y actualizaron los datos). "
    'Responde únicamente con JSON: {"parrafos": ["...", "..."]}'
)
EJ_ENTRADA = (
    "Título: Familiarización con la plataforma estudiantil\n"
    "Notas: exploré Moodle: funciones, herramientas, usuarios, cursos y recursos"
)
EJ_SALIDA = json.dumps({"parrafos": [
    "Se realizó un proceso de familiarización con la plataforma estudiantil basada en Moodle, "
    "explorando sus principales funciones, herramientas y opciones disponibles.",
    "Esta actividad permitió conocer la estructura de la plataforma y comprender los "
    "procedimientos relacionados con la administración de usuarios, cursos, actividades y "
    "demás recursos utilizados por la institución.",
]}, ensure_ascii=False)


def redactar_dia(titulo, notas, intentos=3):
    for _ in range(intentos):
        try:
            r = ollama.chat(
                model=MODELO,
                messages=[
                    {"role": "system", "content": INSTR_DIA},
                    {"role": "user", "content": EJ_ENTRADA},
                    {"role": "assistant", "content": EJ_SALIDA},
                    {"role": "user", "content": f"Título: {titulo}\nNotas: {notas}"},
                ],
                format="json",
                options={"temperature": 0.1},
            )
            parrafos = json.loads(r["message"]["content"])["parrafos"]
            if parrafos and all(isinstance(p, str) for p in parrafos):
                return [p.strip() for p in parrafos]
        except (json.JSONDecodeError, KeyError):
            pass
    raise RuntimeError(f"No se pudo redactar el día: {titulo}")


# ---------- Redacción de las secciones generales ----------
REGLAS = (
    "Redactas secciones de un informe de prácticas preprofesionales en español formal, "
    "en voz impersonal. Usa únicamente la información de los DATOS. "
    "No inventes actividades, resultados, beneficios ni mejoras que no estén en los datos. "
    "No repitas ideas. Cuida la concordancia gramatical. "
    'Responde únicamente con JSON: {"items": ["...", "..."]}'
)


def pedir(instruccion, contexto, intentos=3):
    for _ in range(intentos):
        try:
            r = ollama.chat(
                model=MODELO,
                messages=[
                    {"role": "system", "content": REGLAS},
                    {"role": "user", "content": f"{instruccion}\n\nDATOS:\n{contexto}"},
                ],
                format="json",
                options={"temperature": 0.2},
            )
            items = json.loads(r["message"]["content"])["items"]
            if items and all(isinstance(x, str) for x in items):
                return [x.strip() for x in items]
        except (json.JSONDecodeError, KeyError):
            pass
    raise RuntimeError(f"No se pudo generar: {instruccion[:40]}...")


SECCIONES = {
    "INTRODUCCION": "Redacta la introducción del informe en 3 párrafos: finalidad del informe y área de trabajo, resumen de las actividades realizadas, y cierre sobre la experiencia práctica.",
    "OBJETIVO_GENERAL": "Redacta el objetivo general en UN solo párrafo, que empiece con un verbo en infinitivo (Desarrollar, Fortalecer...).",
    "OBJETIVOS_ESPECIFICOS": "Redacta una lista de 8 a 10 objetivos específicos, uno por actividad principal, cada uno en una oración que empiece con un verbo en infinitivo.",
    "RESULTADOS": "Redacta una lista de 8 a 12 resultados obtenidos, cada uno en una oración que empiece con 'Se' (Se creó..., Se verificó...), basada solo en las actividades realizadas.",
    "CONCLUSIONES": "Redacta las conclusiones en 4 párrafos: aprendizajes técnicos, experiencia con la plataforma Moodle, trabajo en el área AIP y comunicación con docentes, y una conclusión final.",
    "RECOMENDACIONES": "Redacta una lista de 6 a 8 recomendaciones para la institución, cada una en una oración que empiece con un verbo en infinitivo, relacionadas con las actividades realizadas.",
}


def main():
    generales = pd.read_excel(CARPETA / "informe_datos.xlsx", sheet_name="generales").iloc[0].to_dict()
    actividades = pd.read_excel(CARPETA / "informe_datos.xlsx", sheet_name="actividades")

    contenido = {"generales": generales, "actividades": [], "secciones": {}}

    print("Redactando actividades por día...")
    for _, fila in actividades.iterrows():
        print(f"  - {fila['fecha']}")
        contenido["actividades"].append({
            "titulo": f"{fila['fecha']} – {fila['titulo']}",
            "parrafos": redactar_dia(fila["titulo"], fila["notas"]),
        })

    resumen = (
        f"Área: {generales['area']} de {generales['institucion']}\n"
        f"Periodo: {generales['periodo']}\n"
        "Actividades:\n"
        + "\n".join(f"- {f['titulo']}: {f['notas']}" for _, f in actividades.iterrows())
    )

    print("Redactando secciones generales...")
    for clave, instruccion in SECCIONES.items():
        print(f"  - {clave}")
        contenido["secciones"][clave] = pedir(instruccion, resumen)

    salida = CARPETA / "contenido.json"
    salida.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Listo: {salida}")


if __name__ == "__main__":
    main()