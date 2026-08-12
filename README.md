# CS61A 材料仓库（Summer 2026）

CS61A 课程材料的本地镜像：Lab / Discussion / Homework / Project 的**题目页与解答页**已翻译为中文，并附带可直接运行的解压代码。仓库仅依赖 Python 标准库，无第三方包（环境由 uv 管理）。

## 目录结构

每个任务是一个独立的「单元目录」，归入四个类型目录：

```
cs61a/
├── labs/            # Lab：lab00 ~ lab12
│   └── lab00/
│       ├── lab00.html        # 题目页（已译中）
│       ├── sol-lab00.html    # 解答页（已译中，部分单元无此文件）
│       ├── lab00.py          # 解压出的任务代码
│       ├── tests/            # 测试
│       ├── ok                # ok 测试运行器
│       └── *.ok              # 作业配置（已离线化，见下）
├── discs/           # Discussion：disc00 ~ disc12（仅有页面，无 zip）
├── hws/             # Homework：hw01 ~ hw07
├── projs/           # Project：ants / cats / hog / scheme
├── scripts/         # 流水线脚本（见下）
├── run_all.py       # 一键运行入口（留在仓库根）
├── main.py          # 占位 / 示例文件，非流水线一部分
├── pyproject.toml
├── uv.lock
└── .python-version
```

每个单元目录内直接包含：`题目页.html` + `解答页.html`（若存在）+ 解压代码（`.py`、`tests/`、`ok`、`.ok_*` 等）。

> 说明：`disc` 无 zip 资源；`proj` 无解答页 / 无解答 zip；`lab` / `hw` 不下载解答 zip，只下载并解压题目 zip。

## scripts/ 流水线脚本

- `download_cs61a.py` —— 自包含下载器：为每个单元建目录 → 下载题目页 → 下载解答页(按需) → 下载题目 zip → 解压进单元目录(必要时扁平化) → 删除 zip。脚本内 `OUTPUT_DIR` 用 `dirname(dirname(__file__))` 上溯到仓库根。
- `fix_ok_offline.py` —— 离线化：遍历仓库内所有 `*.ok` 配置，移除 `followup` / `backup` 协议，使 `python ok` 完全离线可运行（避免向伯克利服务器联网）。

## 使用方法

```bash
# 跑完整流水线（下载 + 离线化），使用当前 Python 解释器
python run_all.py

# 已有单元目录、只做离线化（跳过联网下载）
python run_all.py --skip-download

# 只跑某一步
python run_all.py --only download
python run_all.py --only fixok

# 某步失败也继续后续步骤
python run_all.py --continue-on-error
```

`run_all.py` 用 `sys.executable` 依次调用 `scripts/` 下的子脚本，纯标准库实现。

## 下载规则（与 cs61a.org 实际资源对应）

| 类型 | 题目页 | 解答页 | 题目 zip | 解答 zip |
|------|--------|--------|----------|----------|
| lab  | 是     | 是     | 是（解压后删） | 否 |
| disc | 是     | 是     | 无资源     | 否 |
| hw   | 是     | 是     | 是（解压后删） | 否 |
| proj | 是     | 无     | 是（解压后删） | 否 |

幂等：已存在的非空文件直接跳过；404 友好跳过，不中断流程。

## 其他

- `.gitignore` 已忽略 `__pycache__/`、`.venv`、`.workbuddy`、`*.zip` 等。
- `.workbuddy/` 为 WorkBuddy 内部数据，不提交。
- `main.py` 仅为示例 / 占位文件，不参与流水线。
