from pathlib import Path
import subprocess
import argparse


def create_folder_structure(num_folders: int) -> None:
    package_name = "some_other_repo"
    src_path = Path(package_name)
    src_path.mkdir(exist_ok=True)
    (src_path / "__init__.py").touch()

    # code that will go in src_path/main.py
    main_text_lines: list[str] = []

    # import all packages
    for i in range(1, num_folders + 1):
        main_text_lines.append(
            f"from {package_name}.pkg_{i}.hello import say_hello as say_hello_{i}"
        )

    # run all functions
    for i in range(1, num_folders + 1):
        main_text_lines.append(f"say_hello_{i}()")

    # Create src_path/main.py
    (src_path / "main.py").write_text("\n".join(main_text_lines))

    # code that will go in pyproject.toml
    pyproject_text_lines: list[str] = []

    pyproject_text_lines.append(
        f"""[tool.poetry]
name = "{package_name}"
version = "0.1.0"
description = ""
authors = ["Jonathan Rayner <jonathan.j.rayner@gmail.com>"]
packages = [{{ include = "{package_name}"}}]

[tool.poetry.dependencies]
python = "^3.10 <3.13"
"""
    )

    # add all dependencies
    for i in range(1, num_folders + 1):
        pyproject_text_lines.append(
            f'pkg_{i} = {{git = "git@github.com:JonathanRayner/some_monorepo.git", subdirectory = "pkg_{i}"}}'
        )

    # last lines of pyproject.toml
    pyproject_text_lines.append(
        """
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )

    # Create pyproject.toml
    Path("pyproject.toml").write_text("\n".join(pyproject_text_lines))


def run_poetry_lock() -> None:
    print("Running 'poetry lock'")
    try:
        subprocess.run(["poetry", "lock"], check=True)
        print("Successfully ran 'poetry lock'")
    except subprocess.CalledProcessError as e:
        print(f"Error running 'poetry lock': {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Create folder structure and run poetry lock"
    )
    parser.add_argument(
        "-n", "--num_folders", type=int, help="Number of folders to create"
    )
    args = parser.parse_args()

    num_folders = args.num_folders

    create_folder_structure(num_folders)
    print(f"Folder structure created successfully for {num_folders} folders.")
    run_poetry_lock()
    print("Finished running 'poetry lock' for all packages.")


if __name__ == "__main__":
    main()
