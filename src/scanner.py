from pathlib import Path
from .config import Config


def scan_pdfs(cfg: Config) -> list[str]:
    """Return numeric stems of all *.pdf files in public_dir, sorted numerically."""
    stems = []
    for f in cfg.public_dir.iterdir():
        if f.suffix.lower() == ".pdf" and f.stem.isdigit():
            stems.append(f.stem)
    return sorted(stems, key=int)
