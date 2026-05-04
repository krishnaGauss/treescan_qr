from .config import Config
from .scanner import scan_pdfs
from .generator import generate_qr


def run(cfg: Config | None = None) -> None:
    if cfg is None:
        cfg = Config()

    stems = scan_pdfs(cfg)
    if not stems:
        print(f"No numeric PDFs found in '{cfg.public_dir}'.")
        return

    print(f"Found {len(stems)} PDFs — generating QR codes...\n")

    ok = skipped = 0
    for stem in stems:
        dest = cfg.qr_output_path(stem)
        if dest.exists():
            print(f"  [skip]  {dest.name}  (already exists)")
            skipped += 1
            continue

        url = cfg.pdf_url(stem)
        generate_qr(url, dest, cfg)
        print(f"  [ok]    {dest.name}  →  {url}")
        ok += 1

    print(f"\nDone.  generated={ok}  skipped={skipped}")
