import os
import platform
import subprocess

# directories
CURRENT: str = str(os.getcwd()) + "/"
HOME: str = str(os.path.expanduser("~")) + "/"
WORKDIR: str = CURRENT#HOME + "debian_setup/"
CONFIG: str = HOME + ".config/"
PROJECTS: str = HOME + "Projects/"
DISTROBOX: str = HOME + "distrobox/"
ASSETS: str = WORKDIR + "assets/"

HOME_FILES: list[str] = os.listdir(HOME)
DISTROBOX_HOMES: list[str] | list = os.listdir(DISTROBOX) if ("distrobox" in HOME_FILES) else list()

if (".config" not in HOME_FILES):
    os.system("mkdir ~/.config")


CONFIG_FILES: list[str] = os.listdir(CONFIG)
ASSETS_FILES: list[str] = os.listdir(ASSETS)

# get the list of my favorites packages
with open(f"{WORKDIR}packages.txt", "r") as file:
    PACKAGES: list[str] = file.read().split("\n")

# get the list of already installed packages
def installed() -> list[str]:
    result = subprocess.run(['dpkg', '--get-selections'], stdout=subprocess.PIPE, text=True)
    result = result.stdout.replace("\tinstall\n", "")
    for _ in range(4):
        result = result.replace("\t\t", "\t")
    result = result.split("\t")
    return result

# check if package is already installed
def check_pkg(package: str) -> bool:
    return (package in installed())

def is_debian() -> bool:
    return platform.freedesktop_os_release()["ID"] == "debian"

def install(package: str) -> None:
    os.system(f"sudo apt install {package} -y")
    return

def upgrade() -> None:
    os.system(f"sudo apt update -y && sudo apt upgrade -y")
    return

# add the extra contrib and non-free repositories
def extra_repos() -> None:
    os.system("sudo apt-add-repository contrib -y")
    os.system("sudo apt-add-repository non-free -y")
    if not (check_pkg("brave-browser")):
        os.system("sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg")
        os.system('echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list')
    upgrade()
    return

def new_file(name: str, destiny: str, destiny_files: list[str] | list, hidden: bool = False) -> None:
    hidden_name = "." + name if hidden else name
    if (hidden_name in destiny_files): return
    if (name in ASSETS_FILES):
        os.symlink(ASSETS + name, destiny + hidden_name)
        return
    return

def new_home_file(name: str, hidden: bool = False) -> None:
    return new_file(name, HOME, HOME_FILES, hidden)

def new_config(name: str, hidden: bool = False) -> None:
    return new_file(name, CONFIG, CONFIG_FILES, hidden)

# install oh my zsh
def oh_my_zsh() -> None:
    new_home_file("oh-my-zsh", True)
    new_home_file("zshrc", True)
    return

# install zsh theme
def power_level() -> None:
    new_home_file("powerlevel10k")
    os.system("p10k configure")
    return

def sway() -> None:
    new_config("sway")
    return

def waybar() -> None:
    new_config("waybar")
    return

def wofi() -> None:
    new_config("wofi")
    return

def alacritty() -> None:
    new_config("alacritty")
    return

def redshift() -> None:
    new_config("redshift")
    return

def distrobox() -> None:
    for opS in ["arch", "ubuntu", "fedora"]:
        if (opS in DISTROBOX_HOMES): continue
    return

def set_appearance() -> None:
    # testando algo
    for dir in ["wallpapers", "fonts", "icons", "themes"]:
        new_home_file(dir, True)
    return

def main() -> None:
    if (not is_debian()): return
    upgrade()
    extra_repos()

    for index, pkg in enumerate(PACKAGES):
        
        if (check_pkg(pkg)): continue
        os.system("clear")
        print(f"[{index + 1}/{len(PACKAGES)}] - {pkg}")
        install(pkg)
        continue
    os.system("clear")

    oh_my_zsh()
    power_level()

    alacritty()

    sway()
    waybar()
    wofi()
    redshift()

    distrobox()

    set_appearance()

    return

if __name__ == "__main__":
    main()