import pandas as pd

generales = pd.DataFrame([{
    "estudiante": "aaaaaaaaaaaaaa",
    "institucion": "aaaaaaaaaaaaaaaaa",
    "area": "AIP",
    "periodo": "aaaaaaaaaaaaaa",
    "monitor": "aaaaaaaaaaaaa",
}])

actividades = pd.DataFrame([
    {"fecha": "24 de agosto de 2026", "titulo": "Inducción e indicaciones de trabajo",
     "notas": "inducción inicial, indicaciones sobre el área y funciones"},
    {"fecha": "25 de agosto de 2026", "titulo": "Familiarización con la plataforma estudiantil",
     "notas": "exploré Moodle, sus funciones, usuarios, cursos y recursos"},
    {"fecha": "28 de agosto de 2026", "titulo": "Administración y depuración de la plataforma",
     "notas": "creé cuentas de administrador, revisé la base de datos, eliminé duplicados, corregí datos"},
    {"fecha": "1 de septiembre de 2026", "titulo": "Monitoreo y verificación de cursos",
     "notas": "monitoreo , apoyo a docentes en , verifiqué cursos activos"},
])

with pd.ExcelWriter("informe_datos.xlsx") as writer:
    generales.to_excel(writer, sheet_name="generales", index=False)
    actividades.to_excel(writer, sheet_name="actividades", index=False)

print("informe_datos.xlsx creado")