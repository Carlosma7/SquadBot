from invoke import task, run

# File cleaning task
@task 
def clean(c):
	print("Cleaning python caché.")
	run("find . -maxdepth 4 -type d -name  .pytest_cache -exec rm -r {} +")
	run("find . -maxdepth 4 -type d -name __pycache__ -exec rm -r {} +")

# Testing execution task
@task
def test(c):
	print("Tests execution from SquadBot")
	run("pytest -v -s --disable-pytest-warnings src/test/*")

# Run execution task
@task
def execute(c):
	print("SquadBot running!")
	run("python3 src/core/bot.py")