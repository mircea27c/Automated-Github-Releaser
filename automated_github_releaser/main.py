import json
import os.path
import shutil
import git
from abc import abstractmethod
import subprocess

from git import GitCommandError
from github import Github

def is_single_word(string: str):
    return not ' ' in string

class Command:
    result = ""

    @abstractmethod
    def execute(self, repo_path):
        pass

class Command_Git(Command):

    def __init__(self, command):
        self.command_id = command
        self.repo = None

    @abstractmethod
    def execute(self, repo_path):
        if self.command_id.startswith("add "):
            add_output = self.repo.git.add(self.command_id.split()[1])
            if "Changes to be committed" not in add_output:
                self.result = "Error adding changes to the index. Output:\n" + add_output
        elif self.command_id.startswith("commit "):
            try:
                commit_output = self.repo.git.commit(self.command_id.split()[1], ' '.join(self.command_id.split()[2:]))
                if "nothing to commit" in commit_output:
                    self.result = "No changes to commit. Output:\n" + commit_output
            except GitCommandError as e:
                self.result = "Error committing changes:" + str(e)
        elif self.command_id == "push":
            push_output = self.repo.git.push()
            if "Everything up-to-date" not in push_output:
                self.result = "Error pushing changes. Output:\n" + push_output
        else:
            self.result = "COMMAND GIT DOES NOT EXIST: " + self.command_id

class Command_Console(Command):

    def __init__(self, command):
        self.command = command

    @abstractmethod
    def execute(self, repo_path):
        cmd_result = subprocess.run(self.command, shell=True, capture_output=True, text=True, cwd=os.path.abspath(repo_path))
        if cmd_result.stderr != "":
            self.result = "Console command failed: " + cmd_result.stderr
        else:
            if cmd_result.stdout != "":
                self.result = cmd_result.stdout
            else:
                self.result = "Console command: Success!"
        pass

class Command_OS(Command):
    @abstractmethod
    def execute(self, repo_path):
        pass

class Command_OSMove(Command_OS):

    def __init__(self, from_path, to_path):
        self.from_path = from_path
        self.to_path = to_path

    @abstractmethod
    def execute(self, repo_path):
        from_path_abs = os.path.abspath(self.from_path)
        to_path_abs = os.path.abspath(self.to_path)

        if not os.path.exists(from_path_abs):
            self.result = f"Move command failed: 'from path' does not exist {from_path_abs}"
            return
        if not os.path.exists(to_path_abs):
            self.result = f"Move command failed: 'to path' does not exist {to_path_abs}"
            return

        shutil.move(from_path_abs, to_path_abs)
        self.result = "Move command: Success!"

class Command_OSDelete(Command_OS):
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.result = ""

    @abstractmethod
    def execute(self, repo_path):
        if len(self.file_paths) > 1:

            file_paths_abs = [os.path.abspath(file) for file in self.file_paths]

            for file in file_paths_abs:
                if os.path.exists(file):
                    os.remove(file)
                else:
                    self.result += f"Delete file failed: file {file} does not exist \n"
        else:
            file_path_abs = os.path.abspath(self.file_paths)
            if os.path.exists(file_path_abs):
                os.remove(file_path_abs)
            else:
                self.result += f"Delete file failed: file {file_path_abs} does not exist \n"
        if self.result == "":
            self.result = "File deletion: Success!"

class ReleaseCommandsPack:

    tag = ""
    name = ""
    description = ""
    draft = False
    prerelease = False
    branch = ""
    repo_dir = ""

    github_token = ""
    repo_path = "mircea27c/Unity-Useful"

    repo = None

    commands_sequence = []

    def __init__(self):
        self.commands_sequence = []

    def run(self):

        print_result = False

        repo = git.Repo(self.repo_dir)

        for command in self.commands_sequence:
            if isinstance(command, Command_Git):
                command.repo = repo

        for command in self.commands_sequence:
            command.execute(self.repo_dir)
            if print_result:
                print(command.result)
        pass

    def publish(self):
        print(f"publish release with tag {self.tag} \n name {self.name} \n description {self.description} \n draft {self.draft} \n prerelease {self.prerelease}")

        g = Github(self.github_token)
        release_repo = g.get_repo(self.repo_path)

        release = release_repo.create_git_release(
            tag=self.tag,
            name=self.name,
            message=self.description,
            draft=self.draft,
            prerelease=self.prerelease
        )
        print(f"Release {release.tag_name} created successfully!")

        pass

def add_release_detail_to_pack(pack: ReleaseCommandsPack, detail: tuple):
    field = detail[0]
    value = detail[1]

    if field == "release_tag":
        pack.tag = value
    elif field == "release_name":
        pack.name = value
    elif field == "release_description":
        pack.description = value
    elif field == "prerelease":
        pack.prerelease = value
    elif field == "draft":
        pack.draft = value
    elif field == "branch":
        pack.branch = value
    elif field == "auth_token":
        pack.github_token = value
    elif field == "repo_dir_path":
        pack.repo_dir = value

    return

def run_automated_release(json_data: str):
    json_file = open(json_data)

    config = json.load(json_file)

    release_pack = ReleaseCommandsPack()

    for key, value in config.items():
        if key == "details":
            for detail in value.items():
                add_release_detail_to_pack(release_pack, detail)
        elif key == "run_commands":
            for command in value["commands"]:
                console_cmd = Command_Console(command)
                release_pack.commands_sequence.append(console_cmd)
        elif key == "git_commands":
            for command in value["commands"]:
                git_cmd = Command_Git(command)
                release_pack.commands_sequence.append(git_cmd)
        elif key == "move_files":
            for move_action in value:
                move_cmd = Command_OSMove(move_action["from"], move_action["to"])

                release_pack.commands_sequence.append(move_cmd)
        elif key == "delete_files":
            delete_cmd = Command_OSDelete(value)
            release_pack.commands_sequence.append(delete_cmd)

    release_pack.run()

    release_pack.publish()

    json_file.close()

def main():
    run_automated_release("config_example.json")


if __name__ == "__main__":
    main()
