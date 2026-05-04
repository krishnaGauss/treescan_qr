from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    public_dir: Path = field(default_factory=lambda: Path("public"))
    base_url: str = "YOUR_DOMAIN_GOES_HERE"
    output_format: str = "PNG"       # PNG or JPEG
    qr_box_size: int = 10
    qr_border: int = 4
    qr_error_correction: str = "H"  # L, M, Q, H

    def pdf_url(self, stem: str) -> str:
        return f"{self.base_url}/{stem}.pdf"

    def qr_output_path(self, stem: str) -> Path:
        ext = "jpg" if self.output_format == "JPEG" else "png"
        return self.public_dir / f"{stem}.{ext}"
