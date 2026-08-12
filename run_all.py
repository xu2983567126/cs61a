"""
CS61A 材料流水线 —— 一键运行脚本

下载脚本已自包含（下载页面/解答页 + 解压 zip 进单元目录并删除 zip），
因此流水线只需两步：
    download -> fixok

用法:
    python run_all.py                 # 跑完整流水线（下载 + .ok 离线化）
    python run_all.py --skip-download # 已有单元目录时跳过联网下载
    python run_all.py --only download  # 只跑下载
    python run_all.py --only fixok     # 只跑 .ok 离线化
    python run_all.py --continue-on-error

说明:
    - 使用运行本脚本的同一解释器 (sys.executable) 逐一执行子脚本。
    - 纯标准库，无第三方依赖。
"""
import os
import sys
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

# 流水线步骤（顺序很重要）。每个步骤: (key, 脚本文件名, 描述)
STEPS = [
    ("download", "scripts/download_cs61a.py", "下载并解压到单元目录（联网）"),
    ("fixok",    "scripts/fix_ok_offline.py", "让 .ok 配置离线可用"),
]


def run_step(script_name, desc, stop_on_error=True):
    """运行单个子脚本，实时透传输出，返回 True/False 表示成功与否。"""
    path = os.path.join(BASE_DIR, script_name)
    if not os.path.isfile(path):
        print(f"  [跳过] 找不到 {script_name}")
        return False

    print("\n" + "=" * 64)
    print(f"▶ 步骤: {desc}")
    print(f"  运行: {script_name}")
    print("=" * 64)

    try:
        result = subprocess.run([PY, path], cwd=BASE_DIR)
    except Exception as e:
        print(f"  [异常] 无法启动 {script_name}: {e}")
        return False

    if result.returncode == 0:
        print(f"  [完成] {desc} ✓")
        return True
    else:
        print(f"  [失败] {desc} ✗ (退出码 {result.returncode})")
        if stop_on_error:
            print("\n流水线在错误处中止。可加 --continue-on-error 忽略此步继续，"
                  "或 --only <step> 单独重试。")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CS61A 材料处理流水线 —— 一键运行所有脚本")
    parser.add_argument("--skip-download", action="store_true",
                        help="跳过联网下载（已有单元目录时使用）")
    parser.add_argument("--only", metavar="STEP",
                        choices=[s[0] for s in STEPS],
                        help="只运行指定步骤: " + "/".join([s[0] for s in STEPS]))
    parser.add_argument("--continue-on-error", action="store_true",
                        help="某步失败时仍继续后续步骤")
    args = parser.parse_args()

    print("=" * 64)
    print("CS61A 材料流水线 — 一键运行")
    print(f"工作目录: {BASE_DIR}")
    print("=" * 64)

    stop_on_error = not args.continue_on_error

    # 单独运行模式
    if args.only:
        for key, script, desc in STEPS:
            if key == args.only:
                ok = run_step(script, desc, stop_on_error)
                break
        print("\n" + "=" * 64)
        print("指定步骤结束。" if ok else "指定步骤未成功完成。")
        print("=" * 64)
        return

    # 完整流水线
    steps_to_run = list(STEPS)
    if args.skip_download:
        steps_to_run = [s for s in steps_to_run if s[0] != "download"]
        print("\n[提示] 已跳过下载步骤 (--skip-download)")

    for key, script, desc in steps_to_run:
        ok = run_step(script, desc, stop_on_error)
        if not ok and stop_on_error:
            print("\n流水线已中止。")
            return

    print("\n" + "=" * 64)
    print("🎉 全部步骤完成！")
    print("=" * 64)


if __name__ == "__main__":
    main()
