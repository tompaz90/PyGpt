import os
from openai import OpenAI
import typer
from rich import print
from rich.table import Table


def main():
    # Leemos el token personal en un fichero passkey.txt
    with open("passkey.txt", "r") as file:
        passkey = file.read()
        file.close()

    # Le damos la clave personal a chatgpt
    client = OpenAI(
        api_key=passkey
    )

    # Creamos una tabla mostrando las diferentes funciones
    print("[bold green]Asistente con ChatGPT[/bold green]")
    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la app")
    table.add_row("new", "Crear nueva conversación")
    print(table)

    # Si quieres usar chatgpt en un ambito concreto este seria el lugar para colocar el contexto
    context = [{"role": "system",
                "content": "Eres un asistente de programacion"}]
    messages = context

    while True:
        prompt = _prompt()

        # Si el prompt es "new" se borra toda la conversacion y se crea una nueva
        if prompt == "new":
            print("[green]Nueva conversación creada[/green]")
            messages = context
            prompt = _prompt()

        # en messages role y content son los 2 parametros obligatorios
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=messages)

        response_txt = response.choices[0].message.content

        # Guardamos la respuesta en la conversacion para seguir interactuando
        messages.append({"role": "assistant", "content": response_txt})
        print(f'[bold green]{response_txt}[/bold green]')


def _prompt() -> str:
    prompt = typer.prompt("Lanza tu pregunta")
    if prompt == "exit":
        _exit = typer.confirm("¿Estás seguro?")
        if _exit:
            raise typer.Abort()
    return prompt


if __name__ == "__main__":
    typer.run(main)
