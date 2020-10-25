import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Snake",
    options={"build_exe": {"packages":["Buttons"]}},
    executables = executables

    )