"""
让所有作业的 ok 完全离线：从每个 *.ok 配置的 protocols 中移除 'followup' 和 'backup'。
- followup: 测试通过后向伯克利服务器追问话题，离线会 DNS 失败崩溃
- backup: 向服务器备份代码（离线用不到，且 --local 外会联网）
移除后 ok 不再尝试任何网络请求，可离线直接 `python ok` 运行。
"""
import os
import json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 脚本位于 scripts/ 下，上溯一级到仓库根目录（.ok 位于各单元目录内）
TO_REMOVE = {"followup", "backup"}
changed = 0
skipped = 0

for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith(".ok") and not f.startswith("ok"):  # 作业的 xxx.ok 配置（排除 ok 本体）
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    cfg = json.load(fh)
                prots = cfg.get("protocols", [])
                new_prots = [p for p in prots if p not in TO_REMOVE]
                if new_prots != prots:
                    cfg["protocols"] = new_prots
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(cfg, fh, indent=4, ensure_ascii=False)
                        fh.write("\n")
                    removed = [p for p in prots if p in TO_REMOVE]
                    changed += 1
                    print(f"  [修改] {os.path.relpath(path, BASE)}  移除: {removed}")
                else:
                    skipped += 1
            except Exception as e:
                print(f"  [跳过] {os.path.relpath(path, BASE)}  错误: {e}")
                skipped += 1

print(f"\n完成: 修改 {changed} 个配置 | 无需修改 {skipped} 个")
