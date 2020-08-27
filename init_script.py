import os
import platform
import json
import stat
import warnings


def check_virtual_env(current_os):
    print("Checking for virtual environments..")

    if os.path.isdir("./venv"):
        print("Virtual Environment found")

        if current_os == "Linux":
            if not os.path.isfile("./venv/bin/geckodriver"):
                msg = "Warning! geckodriver wasn't found in venv/bin/\nMake sure to include in path before starting the script."
                warnings.warn(msg)

    else:
        msg = "No virtual envrionment was found. \
            Please create one and install all dependencies from requirements.txt"
        raise FileNotFoundError(msg)


def create_project_settings_file(current_os, abs_path):

    slash = ""
    if current_os == "Linux":
        slash = "/"

    elif current_os == "Windows":
        slash = "\\"

    else:
        raise OSError("Unsupported OS. How did you even make it this far?")

    project_settings = {
        'abs_path': abs_path,
        'results_path': abs_path + f"{slash}results{slash}results.csv",
        'graphing_results_path': abs_path + f"{slash}graphing_results"
    }

    print("Creating project_settings.json")

    with open("project_settings.json", "w") as project_settings_file:
        json.dump(project_settings, project_settings_file, indent=4)


def add_execute_permissions(filename):

    if platform.system() != 'Linux':
        raise OSError("This method should only be used on Linux")

    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def write_to_exec_file(current_os, instructions):
    if current_os == 'Linux':
        with open('exec.sh', 'w') as exec_file:
            [exec_file.write(line + "\n") for line in instructions]

        # Must add permission to execute for linux:
        add_execute_permissions("exec.sh")

    elif current_os == 'Windows':
        with open('exec.bat', 'w') as exec_file:
            [exec_file.write(line + "\n") for line in instructions]

    else:
        msg = "I don't know how you made it this far but your OS (%s) is not supported" % current_os
        raise OSError(msg)


def init_linux():

    check_virtual_env("Linux")

    abs_path = os.getcwd()

    create_project_settings_file("Linux", abs_path)

    command_instructions = [
        f'cd "{abs_path}"',
        'source venv/bin/activate',
        'python main_script.py'
    ]

    return command_instructions


def init_windows():
    check_virtual_env('Windows')

    abs_path = os.getcwd()

    create_project_settings_file("Windows", abs_path)

    command_instructions = [
        f'cd {abs_path}',
        f'call venv/Scripts/activate',
        'python main_script.py',
        'PAUSE'
    ]

    return command_instructions


def main():
    current_os = platform.system()

    instructions = []

    if current_os == 'Linux':
        instructions = init_linux()

    elif current_os == 'Windows':
        instructions = init_windows()

    else:
        raise OSError("Unsupported Platform: %s" % current_os)

    write_to_exec_file(current_os, instructions)


if __name__ == "__main__":
    main()
    input("Press Enter to exit")
