"""Prepara esta pasta num computador novo (Mac ou Windows).

Uso, a partir da raiz da pasta Maranne:
    Mac:      python3 .agents/configurar.py
    Windows:  py .agents/configurar.py

Pode rodar quantas vezes quiser: só faz o que estiver faltando.
1. Cria o atalho .claude/skills -> .agents/skills (symlink no Mac, junction no Windows,
   que não precisa de administrador).
2. Cria o .venv e instala as dependências de todas as skills (requirements.txt).
"""

import os
import subprocess
import sys
import venv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / ".agents" / "skills"
ATALHO = RAIZ / ".claude" / "skills"
VENV = RAIZ / ".venv"
WINDOWS = os.name == "nt"


def python_do_venv():
    return VENV / ("Scripts/python.exe" if WINDOWS else "bin/python")


def criar_atalho():
    if ATALHO.exists():
        print(f"ok  atalho já existe: {ATALHO}")
        return
    if ATALHO.is_symlink():  # atalho quebrado
        ATALHO.unlink()
    ATALHO.parent.mkdir(parents=True, exist_ok=True)
    if WINDOWS:
        subprocess.run(["cmd", "/c", "mklink", "/J", str(ATALHO), str(SKILLS)], check=True)
    else:
        ATALHO.symlink_to(Path("..") / ".agents" / "skills", target_is_directory=True)
    print(f"ok  atalho criado: {ATALHO} -> {SKILLS}")


def preparar_venv():
    if not python_do_venv().exists():
        print("..  criando .venv")
        venv.create(VENV, with_pip=True)
    for req in sorted(SKILLS.glob("*/scripts/requirements.txt")):
        print(f"..  instalando {req.relative_to(RAIZ)}")
        subprocess.run([str(python_do_venv()), "-m", "pip", "install", "-q", "-r", str(req)], check=True)
    print(f"ok  python das skills: {python_do_venv().relative_to(RAIZ)}")


if __name__ == "__main__":
    criar_atalho()
    preparar_venv()
