# StatGI 模块仓库

StatGI「定时启动」页可下载的**模块**与**配置**。

## 目录结构

```
模块源\<名字>\module.py      模块源码（发布工具会自动打包进 modules\<名字>.zip）
配置源\xxx.sgmod.json        纯配置（只有"到点干什么"，几 KB，记事本可改）
        xxx.sgmodpack.zip     配置 + 附带的模块文件（分享出来的包）
```

## 使用

StatGI → 定时启动 → 模块仓库 → 选择模块或配置 → 下载。

* 模块装到程序旁的 `modules\`，重启后生效
* 配置装好后立即可用；包里附带的模块，本地没有才会装
* 程序自动校验完整性；有新版本时列表会提示

## 发布

1. **模块**：在 `模块源\<名字>\` 放 `module.py`（可选再放 `module.json` 写
   `name` / `desc` / `author` / `category` / `changelog`）
   **配置**：在 `配置源\` 放 `.sgmod.json` 或 `.sgmodpack.zip`
2. 运行 `发布工具.py` —— 自动打包并更新 `index.json`
3. 提交 Pull Request 或 issue

## 模块元信息（module.py）

| 字段 | 说明 |
| --- | --- |
| `KEY` | 唯一标识，建议英文小写下划线 |
| `NAME` / `DESC` | 名称与一句话说明 |
| `VERSION` | 版本号；**改动模块就加一**，用户端会提示更新 |
| `BUILTIN` | 是否内置 |
| `ORDER` | 显示顺序 |

## 配置文件格式（.sgmod.json）

```json
{
  "key": "auto_door",
  "name": "自动开门",
  "desc": "到点启动 BetterGI 并执行「开门」配置组",
  "author": "作者名",
  "version": "1.0",
  "category": "自动化",
  "changelog": "首次发布",
  "actions": [
    { "type": "exe", "path": "D:\\BetterGI\\BetterGI.exe",
      "args": ["--startGroups", "开门"] },
    { "type": "url", "url": "https://live.bilibili.com/123456" }
  ]
}
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `key` | 是 | 全仓库唯一 |
| `name` / `desc` | 是 | 名称与一句话说明 |
| `author` / `version` | 是 | 作者与版本号 |
| `actions` | 是 | 仅支持 `exe`（启动程序）与 `url`（打开网址） |
| `category` | 否 | 分类，程序中显示为分类标签 |
| `changelog` | 否 | 本次更新说明 |
| `featured` | 否 | 填 `true` 表示精选 |

## 安全

本仓库只收声明式内容（启动程序 / 打开网址），不接受任何可执行代码。
