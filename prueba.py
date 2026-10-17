import ollama

respuesta = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": "Responde en una frase: ¿qué es Python?"}]
)
print(respuesta["message"]["content"])