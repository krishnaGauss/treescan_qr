import qrcode
import qrcode.constants
from pathlib import Path
from .config import Config

_CORRECTION_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


def generate_qr(url: str, dest: Path, cfg: Config) -> None:
    """Render a QR code for *url* and write it to *dest*."""
    qr = qrcode.QRCode(
        error_correction=_CORRECTION_MAP[cfg.qr_error_correction],
        box_size=cfg.qr_box_size,
        border=cfg.qr_border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    dest.parent.mkdir(parents=True, exist_ok=True)

    if cfg.output_format == "JPEG":
        img = img.convert("RGB")
    img.save(dest, format=cfg.output_format)
