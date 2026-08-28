"""Adaptador neutro.

No escribe nada mas alla de `AGENTS.md`, que install.py ya genera.

Existe para dejar explicito que el caso base funciona sin adaptador: cualquier
agente que lea AGENTS.md, o al que se le pueda decir "lee .agent/workflows/X.md
y seguilo", esta cubierto. Incluso pegar el contenido a mano en un chat
funciona.

Para agregar una herramienta nueva, copiar este archivo, ponerle el nombre de
la herramienta y escribir donde espera encontrar sus instrucciones. Son unas
30 lineas; el contenido de rules/ y workflows/ no se toca.
"""

NAME = "generic"


def apply(project_root, agent_dir, log):
    log("adaptador neutro: AGENTS.md alcanza, no hace falta nada mas")
