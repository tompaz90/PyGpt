from openai import OpenAI
import typer
from rich import print
from rich.table import Table
import requests
from PIL import Image
from io import BytesIO


def main():
    _option()


def _gpt() -> OpenAI:
    # Read the token from the file passkey.txt and give it to chatgpt
    with open("passkey.txt", "r") as file:
        passkey = file.read()
        file.close()
        gpt = OpenAI(
            api_key=passkey
        )
        return gpt


def _option() -> None:
    # Create a table showing different functions
    print("[bold green]ChatGPT Assistant[/bold green]")
    table = Table("Command", "Description")
    table.add_row("exit", "Kill the app")
    table.add_row("chat", "Starts new chat")
    table.add_row("img", "Starts chat of images")
    print(table)
    option = typer.prompt("Choose option")
    if option == "exit":
        _exit()
    elif option == "chat":
        _prompt()
    elif option == "img":
        _img()


def _exit() -> None:
    confirm = typer.confirm("¿Are you sure?")
    if confirm:
        raise typer.Abort()


def _prompt():
    gpt = _gpt()
    # Content gives a first context to chatgpt
    context = [{"role": "system", "content": "You are an assistant of programming"}]
    messages = context

    while True:
        print("[bold green]Write 'new' for a new chat[/bold green]")
        prompt = typer.prompt("Ask your question")

        # If prompt is "new" deletes all messages and starts a new conversation
        if prompt == "new":
            print("[green]New conversation created[/green]")
            _prompt()
        elif prompt == "exit":
            _exit()
        elif prompt == "option":
            _option()

        # In messages "Role" and "Content" are mandatory
        messages.append({"role": "user", "content": prompt})

        # Generates a response from chatgpt
        response = gpt.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        response_txt = response.choices[0].message.content

        # Saves and prints response and keeps talking
        messages.append({"role": "assistant", "content": response_txt})
        print(f'[bold green]{response_txt}[/bold green]')


def _img() -> None:
    gpt = _gpt()

    while True:
        prompt = typer.prompt("What do you want to create?")

        if prompt == "option":
            _option()
        elif prompt == "exit":
            _exit()

        # Generates the model Dall-e-2 and gives him the prompt
        response = gpt.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024",
            n=1
        )

        # Generates a url of Azure
        image_url = response.data[0].url

        # Download the image
        image = requests.get(image_url)
        image_data = BytesIO(image.content)

        # Show the image
        img = Image.open(image_data)
        img.show()


if __name__ == "__main__":
    typer.run(main)
