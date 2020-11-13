from src.gui.gui import GUI, run_event_loop
from src.program_handler.program_handler import ProgramHandler
import os.path

root_dir = os.getcwd()
print('root: ', root_dir)

# Initialize the GUI object
program_gui = GUI()

# Initialize the ProgramHandler object
program_handler = ProgramHandler(root_dir)

# Run the event loop
while True:
    exit_condition = run_event_loop(gui=program_gui, handler=program_handler)
    if exit_condition:
        break
