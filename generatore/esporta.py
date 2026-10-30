"""Converte le slide Instagram in JPG nella cartella della giornata del repository.
Uso: python3 esporta.py N   -> ../gN/01.jpg ... (e ../gN/tiktok.zip)"""
import sys, glob, os, pathlib, zipfile
from PIL import Image
ROOT = pathlib.Path(__file__).parent
n = sys.argv[1]
dest = ROOT.parent / f"g{n}"; dest.mkdir(exist_ok=True)
for f in sorted(glob.glob(str(ROOT / "out/ig/*.png"))):
    k = os.path.basename(f)[-6:-4]
    Image.open(f).convert("RGB").save(dest / f"{k}.jpg", "JPEG", quality=92, subsampling=0)
with zipfile.ZipFile(dest / "tiktok.zip", "w") as z:
    for f in sorted(glob.glob(str(ROOT / "out/tiktok/*.png"))):
        z.write(f, os.path.basename(f))
print("ok", dest)
