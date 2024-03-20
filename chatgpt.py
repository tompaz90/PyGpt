from openai import OpenAI
import typer
from rich import print
from rich.table import Table


def main():
    # Read the token from the file passkey.txt and give it to chatgpt
    with open("passkey.txt", "r") as file:
        passkey = file.read()
        file.close()
        client = OpenAI(
            api_key=passkey
        )

    # Create a table showing different functions
    print("[bold green]ChatGPT Assistant[/bold green]")
    table = Table("Command", "Description")
    table.add_row("exit", "Kill the app")
    table.add_row("new", "Start new chat")
    print(table)

    # Content gives a first context to chatgpt
    context = [{"role": "system",
                "content": "You are a assistant of programming"}]
    messages = context

    while True:
        prompt = _prompt()

        # If prompt is "new" deletes all messages and starts a new conversation
        if prompt == "new":
            print("[green]New conversation created[/green]")
            messages = context
            prompt = _prompt()

        # In messages "Role" and "Content" are mandatory
        messages.append({"role": "user", "content": prompt})

        # Generates a response from chatgpt
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=messages)

        response_txt = response.choices[0].message.content

        # Saves response and keeps talking
        messages.append({"role": "assistant", "content": response_txt})
        print(f'[bold green]{response_txt}[/bold green]')


def _prompt() -> str:
    prompt = typer.prompt("Ask your question")
    if prompt == "exit":
        _exit = typer.confirm("¿Are you sure?")
        if _exit:
            raise typer.Abort()
    return prompt


if __name__ == "__main__":
    typer.run(main)
