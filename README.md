# Some Other Repo
Repository used to reproduce https://github.com/python-poetry/poetry/issues/6958

Adapted from https://github.com/JonathanRayner/some_other_repo.
The addition of a Dockerfile made the issue reproducible.

## Reproducing
Running a Docker build:
```bash
docker build .
```
Should result in multiple errors at the `poetry install` step.
