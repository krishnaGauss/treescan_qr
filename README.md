# QR Code Generator for Bark-Code PDFs

This project scans a folder of numbered PDF files and generates a QR code image for each one. Each QR code encodes a direct URL to its corresponding PDF hosted on a web server. The generated images are saved back into the same folder alongside the PDFs.

---

## How it works

The script looks inside a folder called `public/` for files named with numbers, such as `1.pdf`, `42.pdf`, `200.pdf`, and so on. For each PDF it finds, it builds a URL like:

```
YOUR_DOMAIN_GOES_HERE/1.pdf
```

It then creates a QR code image that encodes that URL and saves it as `1.png` (or `1.jpg`) in the same `public/` folder. When someone scans the QR code with a phone, their browser opens the PDF directly.

---

## Default configuration

| Setting                | Default value                                    |
| ---------------------- | ------------------------------------------------ |
| Base URL               | `YOUR_DOMAIN_GOES_HERE`                          |
| Public directory       | `public/` (relative to where you run the script) |
| Output image format    | PNG                                              |
| QR box size            | 10 pixels per box                                |
| QR border (quiet zone) | 4 boxes                                          |
| Error correction       | H (highest — recovers up to 30% damage)          |

The base URL and all other settings can be changed at runtime via command-line flags. See the "Running the script" section below.

---

## Where to put your PDFs

Before running the script, place your PDFs inside the `public/` directory at the root of this project. Any file ending in `.pdf` (case-insensitive) will be picked up — the name can be a number, a word, or anything else.

Examples:

```
public/1.pdf
public/42.pdf
public/report.pdf
public/tree-scan-site-A.pdf
```

The script will skip any file that does not have a `.pdf` extension. It will also skip generating a QR code if the output image already exists, so you can safely run the script multiple times without re-generating files.

The generated QR code images are saved in the same `public/` directory, using the same base name as the PDF:

```
public/1.pdf              ->   public/1.png
public/report.pdf         ->   public/report.png
public/tree-scan-site-A.pdf  ->  public/tree-scan-site-A.png
```

If your web application serves files from a `public/` directory (for example a Next.js or Express app), placing both the PDFs and the generated QR code images there means they are immediately accessible at:

```
https://your-domain.com/1.pdf
https://your-domain.com/report.pdf
https://your-domain.com/1.png
```

---

## Project structure

```
treescan_script/
    main.py              Entry point. Parses command-line arguments and starts the script.
    requirements.txt     Python package dependencies.
    public/              Folder where PDFs live and QR images are saved.
    src/
        __init__.py      Exposes Config and run() to main.py.
        config.py        Holds all configurable settings in one place.
        scanner.py       Finds all valid numbered PDFs inside the public directory.
        generator.py     Creates and saves a single QR code image for a given URL.
        runner.py        Orchestrates the full scan-then-generate loop.
```

### What each file does in detail

**`main.py`**

This is the file you run. It reads any flags you pass on the command line (like `--base-url` or `--format`), builds a `Config` object from them, then calls `run()` to do the actual work. If you run it with no flags at all, it uses the defaults from the table above.

**`src/config.py`**

Defines the `Config` dataclass, which is a simple container for all the settings the script needs. It also has two helper methods: `pdf_url(stem)` builds the full URL for a given PDF number, and `qr_output_path(stem)` returns the file path where the QR image will be saved.

**`src/scanner.py`**

Contains one function, `scan_pdfs(cfg)`. It looks inside `cfg.public_dir`, collects every file with a `.pdf` extension regardless of its name, and returns those names sorted alphabetically.

**`src/generator.py`**

Contains one function, `generate_qr(url, dest, cfg)`. It uses the `qrcode` library to create a QR code for the given URL, applies the box size and border settings from `cfg`, and saves the resulting image to `dest`. If you chose JPEG output, it converts the image to RGB first (JPEG does not support transparency).

**`src/runner.py`**

Contains one function, `run(cfg)`. It calls `scan_pdfs` to get the list of PDFs, then loops over them. For each one it checks whether the output image already exists (and skips it if so), constructs the URL, calls `generate_qr`, and prints a progress line. At the end it prints a summary of how many QR codes were generated and how many were skipped.

---

## Prerequisites

- Python 3.10 or newer. You can check your version by running:

  ```
  python3 --version
  ```

  If you see something like `Python 3.10.x` or higher, you are good. If not, download Python from https://www.python.org/downloads/ and install it first.

---

## Step 1 — Set up a Python virtual environment

A virtual environment is an isolated copy of Python that keeps the packages you install for this project separate from everything else on your computer. This prevents version conflicts and keeps your system Python clean.

Open a terminal, navigate to the project folder, and run:

```bash
cd /path/to/treescan_script
python3 -m venv myenv
```

This creates a folder called `myenv/` inside the project. You only need to do this once.

Now activate the virtual environment:

On macOS or Linux:

```bash
source myenv/bin/activate
```

On Windows (Command Prompt):

```bash
myenv\Scripts\activate.bat
```

On Windows (PowerShell):

```bash
myenv\Scripts\Activate.ps1
```

Once activated, your terminal prompt will change to show `(myenv)` at the beginning. This tells you the virtual environment is active and any packages you install will go into it.

You need to activate the virtual environment every time you open a new terminal before running the script.

To deactivate it when you are done, run:

```bash
deactivate
```

---

## Step 2 — Install dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

This installs two packages:

- `qrcode[pil]` — the library that generates QR code images
- `Pillow` — the image processing library used to save the QR codes as PNG or JPEG files

You only need to run this once per virtual environment. If `requirements.txt` changes in the future, run it again to pick up new packages.

---

## Step 3 — Add your PDFs

Place your numbered PDF files inside the `public/` directory:

```
public/1.pdf
public/2.pdf
public/3.pdf
...
```

If the `public/` directory does not exist yet, create it:

```bash
mkdir public
```

---

## Step 4 — Run the script

With the virtual environment active and your PDFs in place, run:

```bash
python main.py
```

The script will print progress as it works:

```
Found 3 PDFs — generating QR codes...

  [ok]    1.png  ->  YOUR_DOMAIN_GOES_HERE/1.pdf
  [ok]    2.png  ->  YOUR_DOMAIN_GOES_HERE/2.pdf
  [ok]    3.png  ->  YOUR_DOMAIN_GOES_HERE/3.pdf

Done.  generated=3  skipped=0
```

If you run it a second time without adding new PDFs, all files will be skipped because the images already exist:

```
Found 3 PDFs — generating QR codes...

  [skip]  1.png  (already exists)
  [skip]  2.png  (already exists)
  [skip]  3.png  (already exists)

Done.  generated=0  skipped=3
```

---

## Optional — Customising the run with flags

You can override any default value by passing flags when you run the script. All flags are optional.

### Use a different base URL

If your PDFs are hosted somewhere other than `YOUR_DOMAIN_GOES_HERE`, pass your URL:

```bash
python main.py --base-url https://your-domain.com
```

The generated QR codes will then point to `https://your-domain.com/1.pdf`, `https://your-domain.com/2.pdf`, and so on.

### Use a different public directory

If your PDFs are not in a folder called `public/`, specify the folder:

```bash
python main.py --public-dir ./my-files
```

### Save as JPEG instead of PNG

```bash
python main.py --format jpeg
```

This saves QR codes as `.jpg` files instead of `.png`. JPEG files are slightly smaller but are lossy, which can sometimes make QR codes harder to scan. PNG is recommended for QR codes.

### Change the QR code size

`--box-size` controls how many pixels wide each individual square in the QR code is. A larger value produces a bigger image.

```bash
python main.py --box-size 20
```

### Change the quiet-zone border

The quiet zone is the blank white margin around the QR code that helps scanners detect its edges. The default is 4 boxes wide. You can reduce it if space is tight, but most scanners need at least 1 box.

```bash
python main.py --border 2
```

### Combine multiple flags

You can pass any combination of flags at once:

```bash
python main.py --base-url https://your-domain.com --format jpeg --box-size 15 --border 2
```

---

## Troubleshooting

**"No numeric PDFs found in 'public'."**

The script found no files matching the expected pattern. Check that:

- The `public/` folder exists and contains files.
- The files are named with plain numbers, like `1.pdf`, not `document.pdf`.
- You are running the script from the root of the project folder, not from inside `src/`.

**"ModuleNotFoundError: No module named 'qrcode'"**

The dependencies are not installed, or the virtual environment is not active. Make sure you have run `source myenv/bin/activate` (macOS/Linux) or the equivalent for Windows, and then run `pip install -r requirements.txt`.

**QR code image exists but points to the wrong URL**

Delete the existing `.png` or `.jpg` file from `public/` and re-run the script with the correct `--base-url`. The script skips files that already exist, so you must delete the old ones to regenerate them.
