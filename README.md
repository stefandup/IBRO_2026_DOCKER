# Docker Images with VS Code Dev Containers

This small repo is a starter project for learning how to create and work with Docker images directly from Visual Studio Code.

The goal is to make the Docker workflow more transparent than only using Docker Desktop. Docker Desktop is still required, but VS Code, WSL, and Dev Containers let you see and control more of what is happening.

## Dependencies

Install these tools before getting started:

- Windows 10 or Windows 11
- WSL 2
- Ubuntu or another Linux distribution installed through WSL
- Visual Studio Code
- Docker Desktop
- VS Code Dev Containers extension
- VS Code WSL extension
- Git

## Install WSL

Open PowerShell as Administrator and install WSL:

```powershell
wsl --install
```

Restart your computer if Windows asks you to.

After restarting, open Ubuntu from the Start menu and complete the first-time setup.

Update Ubuntu:

```sh
sudo apt update
sudo apt upgrade
```

Install Git:

```sh
sudo apt install git
```

## Install Docker Desktop

Download and install Docker Desktop from:

```text
https://www.docker.com/products/docker-desktop/
```

During setup, make sure Docker Desktop is configured to use the WSL 2 backend.

After installation:

1. Open Docker Desktop.
2. Go to Settings.
3. Open Resources.
4. Open WSL Integration.
5. Enable integration for your WSL distribution, for example Ubuntu.

## Install Visual Studio Code

Download and install VS Code from:

```text
https://code.visualstudio.com/
```

Install these VS Code extensions:

- WSL
- Dev Containers by Microsoft

## Open This Repo in WSL

From Ubuntu or your WSL terminal, clone or open the repo location.

Then start VS Code from the repo folder:

```sh
code .
```

This opens the project in VS Code using the WSL environment.

## Getting Started with Dev Containers

Open the VS Code Command Palette:

```text
Ctrl + Shift + P
```

Then use these Dev Containers commands:

```text
Dev Containers: Add Dev Container Configuration Files...
Dev Containers: Reopen in Container
Dev Containers: Rebuild and Reopen in Container
```

### What the Commands Do

`Dev Containers: Add Dev Container Configuration Files...`

Creates the `.devcontainer` setup files used by VS Code to describe the development container.

`Dev Containers: Reopen in Container`

Reopens the current project inside the configured Docker container.

`Dev Containers: Rebuild and Reopen in Container`

Rebuilds the container image and then reopens the project inside it. Use this after changing the Dockerfile or devcontainer configuration.

## Why Use This Workflow?

Docker Desktop gives you a visual interface, but Dev Containers make the build and development process easier to inspect:

- The Dockerfile shows how the image is built.
- The devcontainer configuration shows how VS Code connects to the container.
- The terminal runs inside the container, so you can test the environment directly.
- Rebuilding the container helps confirm that your setup is reproducible.

This repo is intentionally small so you can focus on the Docker and VS Code workflow first.

## Run Singularity with an External Output Folder

Singularity usually starts in your current workspace. To test a folder that is outside this repo, create a separate output directory and bind it into the container.

The point of running these scripts through Singularity is that the software dependencies live inside the `.sif` image instead of being installed on the host machine. This is especially useful on HPC systems, where Singularity is commonly available and users usually do not have root access to install system packages.

In these examples, replace `<username>` with your Linux username.

Note: some newer systems use the `apptainer` command instead of `singularity`. The command shape is the same.

Create an output folder outside the workspace:

```sh
mkdir -p /home/<username>/example_output
```

Open an interactive shell inside the image and mount that folder as `/output_dir`:

```sh
singularity shell -B /home/<username>/example_output:/output_dir build/LittleUbuntu.sif
```

Inside the Singularity shell, create a test file in the mounted output folder:

```sh
printf 'container output test\n' > /output_dir/test-output.txt
```

List the mounted output folder from inside the container:

```sh
ls -l /output_dir
```

Run the test script from inside the container:

```sh
python scripts/my_test_script.py
```

Then inspect the example NIfTI file:

```sh
python scripts/inspect_nifti.py
```

Exit the container shell:

```sh
exit
```

Back on the host, the same file should exist outside the workspace:

```sh
ls -l /home/<username>/example_output
```

You can also run the same scripts from outside the container with `singularity exec`. Run these commands from the repo root on the host:

```sh
singularity exec build/LittleUbuntu.sif python scripts/my_test_script.py
singularity exec build/LittleUbuntu.sif python scripts/inspect_nifti.py
```

These scripts do not need the external output folder bind. The earlier bind example is there to show how the host filesystem can be mounted into the container. These commands still use the Python environment and installed packages from inside `build/LittleUbuntu.sif`; they just avoid opening an interactive shell first.
