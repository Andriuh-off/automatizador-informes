import sys

import generar_contenido
import llenar_plantilla

#Con --solo-word no se vuelve a llamar a Ollama (usa el contenido.json ya corregido)
if "--solo-word" not in sys.argv:
    generar_contenido.main()
llenar_plantilla.main()