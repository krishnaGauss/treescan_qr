from .config import Config


def scan_pdfs(cfg: Config) -> list[str]:
    """Return stems of all *.pdf files in public_dir, sorted alphabetically."""
    stems = []
    for f in cfg.public_dir.iterdir():
        if f.suffix.lower() == ".pdf":
            stems.append(f.stem)
    return sorted(stems)
