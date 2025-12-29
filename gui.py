import random

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.keys import Keys



class Menu:
    def run() -> str | None:
        style = Style.from_dict({
            "screen": "bg:#0b0e14 fg:#8fa3bf",
            "border": "fg:#4f5d75",
            "title": "fg:#9bbcff bold",
            "text": "fg:#8fa3bf",
            "glitch": "fg:#6c7a96 italic",
            "input": "fg:#c0c0c0 bold",
        })

        # helper
        command_buffer = ""
        output_lines = [
            "Security System Terminal v0.3",
            "Type '-help' to list available commands.",
            ""
        ]

        MENU_COMMANDS = {
            "start": "Start the program.",
            "continue": "Get back to where you left off.",
            "settings": "Options menu.",
            "quit": "Quit the program."
        }

        # glitch effect
        def glitch_text(text):
            if len(text) == 0:  # empty line
                return text
            if random.randrange(0, 1000) < 5:
                pos = random.randint(0, len(text) - 1)
                return text[:pos] + random.choice("#$%&@?") + text[pos+1:]
            return text

        # displayer
        def get_display_text():
            formatted = []
            for line in output_lines[-20:]:
                formatted.append(("class:text", glitch_text(line)))
                formatted.append(("", "\n"))
            formatted.append(("class:input", f"> {command_buffer}"))
            return formatted

        output_control = FormattedTextControl(get_display_text)
        output_window = Window(content=output_control)

        root_container = HSplit([
            Window(
                height=1,
                content=FormattedTextControl(
                    [("class:title", " SECURITY SYSTEM — ACCESS TERMINAL")]
                ),
                style="class:border"
            ),
            output_window
        ])

        layout = Layout(root_container)

        # key bindings
        kb = KeyBindings()

        @kb.add("c-c")
        @kb.add("c-q")
        def _(event):
            event.app.exit()

        @kb.add("enter")
        def _(event):
            nonlocal command_buffer, output_lines
            cmd = command_buffer.strip().lower()
            output_lines.append(f"> {cmd}")
            command_buffer = ""

            if cmd in ("-help", "help"):

                output_lines.append("")
                output_lines.append("Available commands:")

                for k, v in MENU_COMMANDS.items():
                    output_lines.append(f"  {k:<10} — {v}")

                output_lines.append("")

            elif cmd in MENU_COMMANDS:
                output_lines.append(f"Launching '{cmd}'...")
                result = cmd
                Menu.exit(result=result)

            elif cmd == "":
                pass
            else:
                output_lines.append("Command not recognized by the system.")
                output_lines.append("Type '-help'.")

        @kb.add("backspace")
        def _(event):
            nonlocal command_buffer
            command_buffer = command_buffer[:-1]

        @kb.add(Keys.Any)
        def _(event):
            if event.data.isprintable():
                nonlocal command_buffer
                command_buffer += event.data

        # ======================
        # APPLICATION
        # ======================
        Menu = Application(
            layout=layout,
            key_bindings=kb,
            style=style,
            full_screen=True,
            refresh_interval=0.1
        )
        return Menu.run()

if __name__ == "__main__":
    menu = Menu()
    result = menu.run()
    print(f"Menu exited with result: {result}")