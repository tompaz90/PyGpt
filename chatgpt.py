from openai import OpenAI
import typer
from rich import print
from rich.table import Table


def main():
    # Create a table showing different functions
    print("[bold green]ChatGPT Assistant[/bold green]")
    table = Table("Command", "Description")
    table.add_row("exit", "Kill the app")
    table.add_row("chat", "Start new chat")
    print(table)
    _option()


def _option() -> None:
    option = typer.prompt("Choose option")
    if option == "exit":
        _exit()
    elif option == "chat":
        _prompt()


def _exit() -> None:
    confirm = typer.confirm("¿Are you sure?")
    if confirm:
        raise typer.Abort()


def _prompt():
    # Read the token from the file passkey.txt and give it to chatgpt
    with open("passkey.txt", "r") as file:
        passkey = file.read()
        file.close()
        client = OpenAI(
            api_key=passkey
        )

    # Content gives a first context to chatgpt
    context = [{"role": "system", "content": "You are an assistant of programming"}]
    messages = context

    while True:
        prompt = typer.prompt("Ask your question")

        # If prompt is "new" deletes all messages and starts a new conversation
        if prompt == "new":
            print("[green]New conversation created[/green]")
            _prompt()
        elif prompt == "option":
            _option()

        # In messages "Role" and "Content" are mandatory
        messages.append({"role": "user", "content": prompt})

        # Generates a response from chatgpt
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        response_txt = response.choices[0].message.content

        # Saves response and keeps talking
        messages.append({"role": "assistant", "content": response_txt})
        print(f'[bold green]{response_txt}[/bold green]')


if __name__ == "__main__":
    typer.run(main)
