# Workspace Integration

Nerve Center is portable: clone it once next to a project workspace and run one PowerShell command. The script creates its own `.venv`, installs the package and development tools from `pyproject.toml`, and can start the local API.

## First Run

From the Nerve Center directory, run:

```powershell
.\setup.ps1 -Start
```

The command requires Python 3.11 or later. It prefers the Windows Python launcher for Python 3.12 or 3.11, then falls back to `python`. It is safe to run repeatedly: the existing `.venv` is reused and dependencies are updated.

Keep this terminal running while an agent works. Verify the service with:

```powershell
Invoke-RestMethod http://127.0.0.1:8088/healthz
```

## New Project Workflow

1. Clone Nerve Center outside the new project, or add its repository as a workspace folder.
2. Copy [PLAN_PRACY.md](../templates/PLAN_PRACY.md) into the new project's root and replace `<SCIEZKA_DO_NERVE_CENTER>` with the actual absolute path.
3. Put the project's requirements and implementation order under `## Wytyczne projektu`.
4. Make the agent read `PLAN_PRACY.md` first. The plan instructs it to start and verify Nerve Center before reading [SKILL.md](../SKILL.md) and beginning implementation.

The virtual environment remains local to Nerve Center and is excluded from Git. Do not copy `.venv` between machines; run `setup.ps1` after cloning instead.