<div align=center>

# Automatic GitHub Releases Manager
*Project proposed by Continental Iasi*

A handy tool for automating the process of creating a github release. Manages various tasks such as running commands, moving files, deleting files, and executing Git commands to streamline your release process. This tool is designed to work with a configuration file in JSON format, allowing you to specify release details and define a sequence of commands to execute.

</div>

## Features

- **Release Details**: Specify release details such as name, tag, description, draft status, prerelease status, GitHub authentication token, and the path to your local repository.

- **Run Commands**: Execute console commands during the release process. Customize the sequence of commands to suit your project's needs.

- **Move Files**: Move files from one location to another as part of the release process.

- **Delete Files**: Remove unwanted files from your repository during the release.

- **Git Commands**: Execute Git commands like add, commit, and push to automate version control.

## Getting Started

### Prerequisites

Make sure you have the following prerequisites installed:

- [Python](https://www.python.org/) (3.x recommended)
- [Git](https://git-scm.com/)

### Clone the Repository

```bash
git clone https://github.com/mircea27c/Automated-Github-Releaser.git
```

### Install the dependencies

```bash
pip install gitpython PyGithub
```

## Configuration

This tool works with a .json configuration file. In the repo you will find attached an example .json config file looking like this:

```json
{
  "details": {
    "release_name": "Release 1.0.1",
    "release_tag": "v1.0.1",
    "release_description": "This is a test for version 1.0.1",
    "prerelease": false,
    "draft": true,
    "auth_token": "secret_token_xxxxxxxxxxxxxxxxxx",
    "repo_dir_path": "path/to/repo/dir"
  },
  "run_commands": {
    "commands": [
      "mkdir NewContainer"
    ]
  },
  "move_files": [
    {
      "from": "source",
      "to": "destination"
    }
  ],
  "delete_files": [
    "trash1.txt",
    "trash2.txt"
  ],
  "git_commands": {
    "commands": [
      "add .",
      "commit -m 'automatic commit'",
      "push"
    ]
  }
}
```

## Available Commands

| Command                             | Description                                                 | Parameters / Arguments                                           | Usage                                                                      |
|-------------------------------------|-------------------------------------------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------|
| `mkdir`                             | Create a new directory.                                    | `<directory_name>`                                               | `mkdir NewContainer`                                                      |
| `move_files`                        | Move files from one location to another.                    | `{ "from": "<source_path>", "to": "<destination_path>" }`      | Specify source and destination paths in the JSON configuration. Example: `"from": "source", "to": "destination"`                      |
| `delete_files`                      | Delete specified files.                                    | `["<file_path_1>", "<file_path_2>", ...]`                       | Specify files to delete in the JSON configuration. Example: `"delete_files": ["trash1.txt", "trash2.txt"]`                           |
| `git_commands`                      | Execute Git commands: `add .`, `commit -m 'automatic commit'`, and `push`. | ` "commands": ["<command 1>", "<command 2>", "..."] `                                                    | Include Git commands in the JSON configuration. Example: `"commands": ["add .", "commit -m 'automatic commit'", "push"]`           |

### Release Details

The following details can be configured in the JSON file:

| Detail                 | Description                                   | Example                                   |
|------------------------|-----------------------------------------------|-------------------------------------------|
| `release_name`         | Name of the release.                          | `"release 1.0.1"`                         |
| `release_tag`          | Tag for the release.                          | `"v1.0.1"`                                |
| `release_description`  | Description of the release.                   | `"this is a test for 1.0.1"`              |
| `prerelease`           | Boolean indicating if the release is a prerelease. | `false`                                 |
| `draft`                | Boolean indicating if the release is a draft.  | `true`                                  |
| `auth_token`           | GitHub authentication token.                  | `"secret_token_xxxxxxxxxxxxxxxxxx"`       |
| `repo_dir_path`        | Path to the local repository.                 | `"path/to/repo/dir"`                     |
