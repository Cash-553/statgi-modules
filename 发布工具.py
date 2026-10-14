# -*- coding: utf-8 -*-
"""把"模块源"里的 .sgmod.json 收进 modules/ 并更新 index.json。

用法：把新的 .sgmod.json 放进 `模块源/`，然后跑这个脚本（双击或 python 跑都行）。
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "模块源"
MODS = HERE / "modules"
INDEX = HERE / "index.json"
REQUIRED = ("key", "name", "actions")


def main():
    MODS.mkdir(exist_ok=True)
    SRC.mkdir(exist_ok=True)
    old = {}
    if INDEX.exists():
        try:
            for m in json.loads(INDEX.read_text(encoding="utf-8")).get("modules", []):
                if m.get("key"):
                    old[m["key"]] = m
        except Exception:
            pass
    items = []
    for f in sorted(SRC.glob("*.sgmod.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8-sig"))
        except Exception as e:
            print("跳过（不是合法 JSON）：", f.name, e)
            continue
        miss = [k for k in REQUIRED if not d.get(k)]
        if miss:
            print("跳过（缺字段", miss, "）：", f.name)
            continue
        acts = d.get("actions") or []
        bad = [a for a in acts if (a or {}).get("type") not in ("exe", "url")]
        if bad:
            print("跳过（只允许 exe / url 动作）：", f.name, bad)
            continue
        key = d["key"]
        dst = MODS / (key + ".sgmod.json")
        shutil.copy2(f, dst)
        blob = dst.read_bytes()
        item = {
            "key": key,
            "name": d.get("name", key),
            "desc": d.get("desc", ""),
            "author": d.get("author", "匿名"),
            "version": str(d.get("version", "1.0")),
            "file": "modules/" + dst.name,
            "size": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
        }
        # 2026-10-15 新增（可选）：分类 / 更新说明 / 更新时间 / 精选
        #   程序里的「模块仓库」靠这几个字段做筛选和"更新了什么"提示
        for k in ("category", "changelog"):
            v = str(d.get(k) or "").strip()
            if v:
                item[k] = v
        v = str(d.get("updated") or "").strip()
        item["updated"] = v or __import__("datetime").date.today().isoformat()
        if d.get("featured"):
            item["featured"] = True
        items.append(item)
        print("已收录：", key, "->", dst.name)
    if not items:
        print("没有可收录的模块（先在 模块源/ 里放 .sgmod.json）")
        return 1
    # 保留 index 里已有但本次没提供的（比如别人提的 PR）
    have = {i["key"] for i in items}
    for k, m in old.items():
        if k not in have:
            items.append(m)
    INDEX.write_text(json.dumps(
        {"updated": __import__("datetime").date.today().isoformat(),
         "note": "StatGI 模块仓库清单（.sgmod.json 声明式模块）",
         "modules": items}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("index.json 已更新，共", len(items), "个模块")
    return 0


if __name__ == "__main__":
    sys.exit(main())
