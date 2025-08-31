from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Digits, Footer, Header, Input, Button, Static

class App(App):
    TITLE="Local Vision - v2.0"
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Digits("")

        with Static(classes="input-area"):
            yield Input(placeholder="Type something...")
            yield Button(">")

        yield Footer()

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(0.5, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")

app = App()