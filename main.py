#!/usr/bin/env python3
"""
Entry point — generates QR codes for every numeric PDF in public/.

Usage:
    python main.py                        # defaults
    python main.py --format jpeg          # save as .jpg instead of .png
    python main.py --public-dir ./public  # custom folder
"""

import argparse
from pathlib import Path
from src import Config, run


def parse_args() -> Config:
    p = argparse.ArgumentParser(description="QR code generator for bark-code PDFs")
    p.add_argument(
        "--public-dir",
        default="public",
        metavar="DIR",
        help="Folder that contains the numbered PDFs (default: public)",
    )
    p.add_argument(
        "--base-url",
        default="YOUR_DOMAIN_GOES_HERE",
        metavar="URL",
        help="Base URL prefix for the QR code links",
    )
    p.add_argument(
        "--format",
        choices=["png", "jpeg"],
        default="png",
        dest="fmt",
        help="Output image format (default: png)",
    )
    p.add_argument(
        "--box-size",
        type=int,
        default=10,
        help="Pixel size of each QR box (default: 10)",
    )
    p.add_argument(
        "--border",
        type=int,
        default=4,
        help="Quiet-zone border in boxes (default: 4)",
    )
    args = p.parse_args()

    return Config(
        public_dir=Path(args.public_dir),
        base_url=args.base_url,
        output_format=args.fmt.upper(),
        qr_box_size=args.box_size,
        qr_border=args.border,
    )


if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)
