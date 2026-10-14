# StatGI 模块仓库

StatGI「定时启动」页可下载的模块都放在这里。

## 使用

StatGI → 定时启动 → 模块仓库 → 选择模块 → 下载。
程序自动校验完整性，装完即可使用；有新版本时列表会提示更新。

## 投稿

1. 在 `模块源/` 放入 `<名称>.sgmod.json`
2. 运行 `发布工具.py`，自动打包并更新 `index.json`
3. 提交 Pull Request 或 issue

## 模块文件格式

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
| `key` | 是 | 全仓库唯一；建议英文小写下划线 |
| `name` / `desc` | 是 | 名称与一句话说明 |
| `author` / `version` | 是 | 作者与版本号 |
| `actions` | 是 | 仅支持 `exe`（启动程序）与 `url`（打开网址） |
| `category` | 否 | 分类，如 `自动化` / `直播` / `挂机`；程序中显示为分类标签 |
| `changelog` | 否 | 本次更新说明 |
| `featured` | 否 | 填 `true` 表示精选 |

## 安全

本仓库只收声明式模块文件（仅能启动程序或打开网址），不接受任何可执行代码。
