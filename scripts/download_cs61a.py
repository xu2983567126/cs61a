"""
CS61A Summer 2026 — 下载并解压所有 Lab / Discussion / Homework / Project 到单元目录。

最终布局（脚本直接产出，无需额外 extract/flatten 步骤）:
    <repo>/
        labs/lab00/{lab00.html, sol-lab00.html, <解压代码>}
        discs/disc00/{disc00.html, sol-disc00.html}
        hws/hw01/{hw01.html, sol-hw01.html, <解压代码>}
        projs/hog/{hog.html, <解压代码>}

规则（与 cs61a.org 实际资源对应）:
    - lab / hw : 下载题目页 + 解答页 + 题目 zip（解压进单元目录后删 zip）；不下载解答 zip。
    - disc     : 仅下载题目页 + 解答页；disc 无 zip（资源不存在）。
    - proj     : 下载题目页 + 题目 zip（解压进单元目录后删 zip）；proj 无解答页、无解答 zip。

幂等：已存在的非空文件直接跳过；404 友好跳过不中断。
"""
import os
import sys
import zipfile
import shutil
import urllib.request
import urllib.error

BASE_URL = "https://cs61a.org"
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 脚本位于 scripts/ 下，上溯一级到仓库根目录

# 每个单元: name(目录名/页面基名), page(题目页 URL 路径), sol(解答页 URL 或 None), zip(题目 zip URL 或 None)
UNITS = {
    "labs": [
        {"name": f"lab{i:02d}", "page": f"lab/lab{i:02d}/",
         "sol": f"lab/sol-lab{i:02d}/", "zip": f"lab/lab{i:02d}/lab{i:02d}.zip"}
        for i in range(13)
    ],
    "discs": [
        {"name": f"disc{i:02d}", "page": f"disc/disc{i:02d}/",
         "sol": f"disc/sol-disc{i:02d}/", "zip": None}
        for i in range(13)
    ],
    "hws": [
        {"name": f"hw{i:02d}", "page": f"hw/hw{i:02d}/",
         "sol": f"hw/sol-hw{i:02d}/", "zip": f"hw/hw{i:02d}/hw{i:02d}.zip"}
        for i in range(1, 8)
    ],
    "projs": [
        {"name": "hog",   "page": "proj/hog/",   "sol": None, "zip": "proj/hog/hog.zip"},
        {"name": "cats",  "page": "proj/cats/",  "sol": None, "zip": "proj/cats/cats.zip"},
        {"name": "ants",  "page": "proj/ants/",  "sol": None, "zip": "proj/ants/ants.zip"},
        {"name": "scheme","page": "proj/scheme/","sol": None, "zip": "proj/scheme/scheme.zip"},
    ],
}

stats = {"success": 0, "skipped": 0, "failed": 0, "failed_urls": []}


def fetch_url(url, save_path, desc=""):
    """下载单个 URL 保存；已存在非空文件则跳过。返回 True 表示已下载/存在。"""
    full_url = f"{BASE_URL}/{url}" if not url.startswith("http") else url
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        stats["skipped"] += 1
        print(f"  [SKIP] {desc} (已存在)")
        return False

    try:
        req = urllib.request.Request(
            full_url, headers={"User-Agent": "Mozilla/5.0 (compatible; CS61A-downloader)"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(save_path, "wb") as f:
            f.write(data)
        stats["success"] += 1
        print(f"  [OK]   {desc} ({len(data)/1024:.1f} KB)")
        return True
    except urllib.error.HTTPError as e:
        stats["failed"] += 1
        stats["failed_urls"].append((full_url, str(e)))
        print(f"  [404]  {desc} - {e}")
        return False
    except Exception as e:
        stats["failed"] += 1
        stats["failed_urls"].append((full_url, str(e)))
        print(f"  [ERR]  {desc} - {e}")
        return False


def extract_zip(zip_path, dest_dir):
    """解压 zip 到 dest_dir；若 zip 根仅含一个顶层目录则扁平化上提；随后删除 zip。"""
    tmp = dest_dir + "._extract_tmp"
    os.makedirs(tmp, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)
    items = os.listdir(tmp)
    if len(items) == 1 and os.path.isdir(os.path.join(tmp, items[0])):
        top = os.path.join(tmp, items[0])
        for name in os.listdir(top):
            shutil.move(os.path.join(top, name), os.path.join(dest_dir, name))
        os.rmdir(top)
    else:
        for name in items:
            shutil.move(os.path.join(tmp, name), os.path.join(dest_dir, name))
    os.rmdir(tmp)
    os.remove(zip_path)  # 解压完成，丢弃 zip（本环境回收站不可用时可能保留，属正常）
    print(f"  [UNZIP] {os.path.basename(zip_path)} -> {os.path.relpath(dest_dir, OUTPUT_DIR)}")


def process_unit(cat, u, dry_run):
    unit_dir = os.path.join(OUTPUT_DIR, cat, u["name"])
    page_path = os.path.join(unit_dir, f"{u['name']}.html")
    sol_path = os.path.join(unit_dir, f"sol-{u['name']}.html") if u["sol"] else None
    zip_path = os.path.join(unit_dir, f"{u['name']}.zip") if u["zip"] else None

    if dry_run:
        print(f"  [DRY] unit {cat}/{u['name']}")
        print(f"        page -> {os.path.relpath(page_path, OUTPUT_DIR)}")
        if sol_path:
            print(f"        sol  -> {os.path.relpath(sol_path, OUTPUT_DIR)}")
        if zip_path:
            print(f"        zip  -> {os.path.relpath(zip_path, OUTPUT_DIR)} (下载后解压并删除)")
        return

    os.makedirs(unit_dir, exist_ok=True)
    fetch_url(u["page"], page_path, f"page/{u['name']}")
    if sol_path:
        fetch_url(u["sol"], sol_path, f"sol/{u['name']}")
    if zip_path:
        if fetch_url(u["zip"], zip_path, f"zip/{u['name']}"):
            try:
                extract_zip(zip_path, unit_dir)
            except Exception as e:
                print(f"  [ERR]  解压失败 {u['name']}: {e}")


def main():
    dry_run = "--dry-run" in sys.argv
    print("=" * 60)
    print("CS61A — 下载到单元目录" + (" [DRY-RUN]" if dry_run else ""))
    print(f"输出: {OUTPUT_DIR}")
    print("=" * 60)

    for cat, units in UNITS.items():
        print(f"\n{'='*40}\n📁 {cat.upper()}\n{'='*40}")
        for u in units:
            process_unit(cat, u, dry_run)

    if dry_run:
        print("\n[DRY-RUN] 仅打印计划，未联网/未落盘。")
        return

    print("\n" + "=" * 60)
    print("📊 完成!")
    print(f"  成功: {stats['success']}  跳过(已存在): {stats['skipped']}  失败: {stats['failed']}")
    if stats["failed_urls"]:
        print("  失败列表 (多为不存在的资源，可忽略):")
        for url, err in stats["failed_urls"]:
            print(f"    - {url}  ({err})")
    print("=" * 60)


if __name__ == "__main__":
    main()
