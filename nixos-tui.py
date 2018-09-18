import json
import subprocess

import urwid


class InstallerTUI():
    """NixOS installer terminal UI
    """

    def __init__(self):
        pass


CHOICES = {
    "format": "Format Disk for a NixOS install",
    "nix": "Install Nix package manager",
    "create-iso": "Create ISO from current system",
    "bootmedium": "NixOS ISO to USB",
    "nixos": "NixOS manage",
}


def menu(title="NixOS Installer v2018-09", subtitle=None, choices=None):
    title = title
    body = [urwid.Text(title), urwid.Divider()]
    if subtitle:
        body.extend([urwid.Text(subtitle), urwid.Divider()])
    if choices:
        for c in choices.values():
            button = urwid.Button(c)
            urwid.connect_signal(button, "click", item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(button, choice):
    response = urwid.Text([f"You chose {choice}", u"\n"])

    choice_key = list(CHOICES.keys())[list(CHOICES.values()).index(choice)]
    done = urwid.Button(u"Ok")
    urwid.connect_signal(done, "click", exit_program)
    if choice_key == "format":
        output = urwid.BoxAdapter(device_selector(), 10)
    elif choice_key == "nix":
        output = urwid.BoxAdapter(
            menu(
                "Install Nix",
                choices={
                    "curl": "curl https://nixos.org/nix/install | sh",
                    "website": "https://nixos.org/nix/",
                },
            ),
            5,
        )
    elif choice_key == "nixos":
        output = urwid.Text(
            "sudo nix-channel --add https://nixos.org/https://github.com/krebs/nixos-generatorschannels/nixos-18.09 nixos"
        )
    elif choice_key == "create-iso":
        output = urwid.Text("https://github.com/krebs/nixos-generators")
    else:
        output = urwid.Text("no output")
    main.original_widget = urwid.Filler(
        urwid.Pile([response, output, urwid.AttrMap(done, None, focus_map="reversed")])
    )


def get_device_choices():
    choices = {}
    for device in json.loads(subprocess.getoutput("lsblk -J"))["blockdevices"]:
        name = device["name"]
        if name.startswith("loop"):
            continue

        size = device["size"]
        children = device.get("children", "")
        if children:
            c_list = [f"{c['name']} ({c['size']})" for c in children]
            c_string = ": " + ", ".join(c_list)
        else:
            c_string = ""
        choices[name] = f"{name} {size} {c_string}"
    return choices


def device_selector():
    return menu(
        "Choose a disk",
        subtitle="http://cgit.lassul.us/disko/tree/example/config.nix",
        choices=get_device_choices(),
    )


def exit_program(button):
    raise urwid.ExitMainLoop()


def exit_on_q(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()


main = urwid.Padding(menu(choices=CHOICES), left=2, right=2)
tui = urwid.MainLoop(
    main, palette=[("reversed", "standout", "")], unhandled_input=exit_on_q
)
tui.run()

#  def main():
#      return InstallerTUI().main()


# if "__main__" == __name__:
#    global tui
#    tui = main()
