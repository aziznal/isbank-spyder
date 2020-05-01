import os
import json


# region creating project_settings.json

abs_path = os.getcwd()

project_settings = {
    'abs_path': abs_path,
    'results_path': abs_path + "\\results\\",
    'graphing_results_path': abs_path + "\\graphing_results\\"
}

check_list = [os.path.isdir(project_settings['abs_path']),
              os.path.isdir(project_settings['results_path']),
              os.path.isdir(project_settings['graphing_results_path'])]

if all(check_list):
    print("All folders were found, proceeding...")
else:
    raise FileNotFoundError("re-check your structure or re-clone the repo")

with open("project_settings.json", "w") as project_settings_file:
    json.dump(project_settings, project_settings_file, indent=4)

# endregion

# region creating exec.bat

command_instructions = [
    f'cd "{abs_path}"',
    'python main_script.py'
]

with open('exec.bat', 'w') as exec_file:
    [exec_file.write(line + "\n") for line in command_instructions]

# endregion
