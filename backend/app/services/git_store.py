from pathlib import Path

from git import Repo

from app.config import settings


def _repo() -> Repo:
    path = Path(settings.backup_dir)
    path.mkdir(parents=True, exist_ok=True)
    if(path/".git").exists():
        return Repo(path)
    repo = Repo.init(path)
    with repo.config_writer() as cw:
        cw.set_value("user", "name", "NetOps Portal")
        cw.set_value("user", "email", "netops@localhost")
    return repo

def save_config(device_name: str, config: str) -> tuple[str, bool]:
    """Write the config and commit it. Returns (commit sha, whether it changed)."""
    repo = _repo()
    filename = f"{device_name}.cfg"
    (Path(repo.working_dir) / filename).write_text(config)
    repo.index.add([filename])
    if repo.head.is_valid() and not repo.index.diff("HEAD"):
        return repo.head.commit.hexsha, False
    commit = repo.index.commit(f"Backup {device_name}")
    return commit.hexsha, True


def read_config(commit: str, device_name: str) -> str:
    return _repo().git.show(f"{commit}:{device_name}.cfg")