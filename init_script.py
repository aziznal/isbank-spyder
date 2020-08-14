import os
import platform
import json


def init_linux():
    pass


def init_windows():
    pass


def initialize_project():
    current_os = platform.system()

    if current_os == 'Linux':
        init_linux()
    elif current_os == 'Windows':
        init_windows()
    else:
        raise OSError("Unsupported Platform: %s" % current_os)

    abs_path = os.getcwd()

    project_settings = {
        'abs_path': abs_path,
        'results_path': abs_path + "\\results\\",
        'graphing_results_path': abs_path + "\\graphing_results\\"
    }

    check_list = [os.path.isdir(path_) for path_ in project_settings]

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


if __name__ == "__main__":
    initialize_project()
