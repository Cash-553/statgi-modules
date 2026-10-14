# -*- coding: utf-8 -*-
"""把"模块源"和"配置源"收录进 index.json。

用法（双击或 python 跑都行）：
    模块源\  <模块名>\module.py …     ← 一个模块一个文件夹（会自动打成 zip 放进 modules/）
    配置源\  xxx.sgmod.json           ← 纯配置（只有"到点干什么"）
             xxx.sgmodpack.zip        ← 配置 + 附带的模块文件（分享出来的包）

收录结果写进 index.json 的两个列表：
    "modules": [...]   纯模块
    "configs": [...]   配置
"""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD_SRC = HERE / "模块源"
CFG_SRC = HERE / "配置源"
MODS = HERE / "modules"
CFGS = HERE / "configs"
INDEX = HERE / "index.json"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _old(key, kind):
    try:
        d = json.loads(INDEX.read_text(encoding="utf-8-sig"))
        for m in d.get(kind) or []:
            if m.get("key") == key:
                return m
    except Exception:
        pass
    return None


def do_modules():
    """模块源/ 里每个子文件夹 = 一个模块 → 打成 zip 放进 modules/"""
    MOD_SRC.mkdir(exist_ok=True)
    MODS.mkdir(exist_ok=True)
    out = []
    for d in sorted(MOD_SRC.iterdir()):
        if not d.is_dir() or not (d / "module.py").is_file():
            continue
        name = d.name
        ver = ""
        key = name
        try:
            import re as _re
            m = _re.search(r'^\s*KEY\s*=\s*["\']([^"\']+)["\']',
                           (d / "module.py").read_text(encoding="utf-8"), _re.M)
            if m:
                key = m.group(1).strip() or name
        except Exception:
            pass
        try:
            import re
            m = re.search(r'^\s*VERSION\s*=\s*["\']([^"\']+)["\']',
                          (d / "module.py").read_text(encoding="utf-8"), re.M)
            ver = m.group(1) if m else ""
        except Exception:
            pass
        dst = MODS / (key + ".zip")
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, str(f.relative_to(d.parent)).replace("\\", "/"))
        blob = dst.read_bytes()
        item = {"key": key, "kind": "module", "name": name,
                "desc": "", "author": "", "version": ver,
                "file": "modules/" + dst.name, "size": len(blob),
                "sha256": _sha(blob)}
        # 作者/说明可以写在模块文件夹的 module.json 里（可选）
        meta = d / "module.json"
        if meta.is_file():
            try:
                j = json.loads(meta.read_text(encoding="utf-8-sig"))
                for k in ("name", "desc", "author", "version", "category", "changelog"):
                    if j.get(k):
                        item[k] = j[k]
            except Exception:
                pass
        item["updated"] = __import__("datetime").date.today().isoformat()
        out.append(item)
        print("已收录模块：", name, "->", dst.name, f"({len(blob)} 字节)")
    return out


def do_configs():
    """配置源/ 里的 .sgmod.json 或 .sgmodpack.zip → 放进 configs/"""
    CFG_SRC.mkdir(exist_ok=True)
    CFGS.mkdir(exist_ok=True)
    out = []
    for f in sorted(list(CFG_SRC.glob("*.sgmod.json")) + list(CFG_SRC.glob("*.zip"))):
        if f.suffix.lower() == ".zip":
            dst = CFGS / f.name
            shutil.copy2(f, dst)
            blob = dst.read_bytes()
            key = f.stem.replace(".sgmodpack", "")
            name, desc, author, ver, cat, chg = key, "", "", "", "", ""
            try:
                with zipfile.ZipFile(dst) as z:
                    for n in z.namelist():
                        if n.endswith("module.sgmod.json"):
                            j = json.loads(z.read(n).decode("utf-8-sig"))
                            key = j.get("key") or key
                            name = j.get("name") or name
                            desc, author = j.get("desc", ""), j.get("author", "")
                            ver, cat = str(j.get("version", "")), j.get("category", "")
                            chg = j.get("changelog", "")
                            break
            except Exception as e:
                print("跳过（包读不了）：", f.name, e)
                continue
            item = {"key": key, "kind": "config", "name": name, "desc": desc,
                    "author": author or "匿名", "version": ver or "1.0",
                    "file": "configs/" + dst.name, "size": len(blob),
                    "sha256": _sha(blob), "has_modules": True}
        else:
            try:
                j = json.loads(f.read_text(encoding="utf-8-sig"))
            except Exception as e:
                print("跳过（不是合法 JSON）：", f.name, e)
                continue
            acts = j.get("actions") or []
            bad = [a for a in acts if (a or {}).get("type") not in ("exe", "url")]
            if not acts or bad:
                print("跳过（动作只能是 exe / url）：", f.name, bad)
                continue
            _k = str(j.get("key") or f.stem)
            dst = CFGS / (_k + ".sgmod.json")
            dst.write_bytes(f.read_bytes())
            blob = dst.read_bytes()
            item = {"key": _k, "kind": "config",
                    "name": j.get("name") or f.stem, "desc": j.get("desc", ""),
                    "author": j.get("author", "匿名"),
                    "version": str(j.get("version", "1.0")),
                    "file": "configs/" + dst.name, "size": len(blob),
                    "sha256": _sha(blob), "has_modules": False}
        for k in ("category", "changelog"):
            v = str((j if f.suffix.lower() != ".zip" else {}).get(k) or "").strip() \
                if False else ""
        item["updated"] = __import__("datetime").date.today().isoformat()
        out.append(item)
        print("已收录配置：", item["key"], "->", dst.name, f"({len(blob)} 字节)")
    return out


def main():
    mods = do_modules()
    cfgs = do_configs()
    if not mods and not cfgs:
        print("什么都没收录："
              "模块放 模块源/<名字>/module.py；配置放 配置源/xxx.sgmod.json")
        return 1
    data = {"updated": __import__("datetime").date.today().isoformat(),
            "note": "StatGI 仓库清单：modules = 纯模块；configs = 配置（声明式，不含代码）",
            "modules": mods, "configs": cfgs}
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"index.json 已更新：模块 {len(mods)} 个、配置 {len(cfgs)} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
