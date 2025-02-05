import subprocess
import sys

print("Tentative d'exécution de game.py...")
process = subprocess.Popen(
    [sys.executable, "C:/Users/raph6/Documents/ServOMorph/IO_Genesis/developpement/scripts_et_code/game.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
print("Process lancé, attente de réponse...")
stdout, stderr = process.communicate()
print("STDOUT:", stdout)
print("STDERR:", stderr)
