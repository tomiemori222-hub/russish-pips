import json
import hashlib
import zipfile
import os
import sys

PACKAGES_DIR = "."  # текущая папка
OUTPUT_FILE = "packages.json"

def md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_meta_from_ruwhl(path):
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            if "package.russish.json" in zf.namelist():
                return json.loads(zf.read("package.russish.json"))
            else:
                return None
    except:
        return None

def generate():
    packages = {}
    for fname in os.listdir(PACKAGES_DIR):
        if fname.endswith(".ruwhl"):
            full_path = os.path.join(PACKAGES_DIR, fname)
            meta = get_meta_from_ruwhl(full_path)
            if meta is None:
                print(f"Предупреждение: в {fname} отсутствует package.russish.json, пропускаю.")
                continue
            name = meta.get("name", fname.replace(".ruwhl", ""))
            version = meta.get("version", "0.0")
            description = meta.get("description", "")
            packages[name] = {
                "version": version,
                "file": fname,
                "hash": md5_file(full_path),
                "description": description
            }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(packages, f, ensure_ascii=False, indent=4)
    print(f"Готово! {len(packages)} пакетов записано в {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
