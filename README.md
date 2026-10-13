# StatGI 模块仓库

这里放的是 **StatGI 的模块**（定时启动页里那些"到点干什么"的小配置）。

## 怎么用（普通用户）

不用手动下载 —— 打开 StatGI → 「定时启动」页 → 页尾点 **「模块仓库」** →
在列表里挑你想要的 → 点「下载」即可（程序会自动校验并放进 `data/modules/`）。

## 怎么投稿（作者）

1. 写一个 `.sgmod.json`（格式见下），放进 `modules/` 目录
2. 执行本仓库的 `发布工具.py`（会重算大小与校验值并更新 `index.json`）
3. 提交 Pull Request / 直接提 issue 把文件发过来

## `.sgmod.json` 格式

```json
{
  "key": "auto_door",
  "name": "自动开门",
  "desc": "到点启动 BetterGI 并执行「开门」配置组",
  "author": "你的名字",
  "version": "1.0",
  "actions": [
    { "type": "exe", "path": "D:\\BetterGI\\BetterGI.exe",
      "args": ["--startGroups", "开门"] },
    { "type": "url", "url": "https://live.bilibili.com/123456" }
  ]
}
```

* `actions` 只支持两种：`exe`（启动程序）和 `url`（打开网址）
* **不接受任何可执行代码 / 脚本** —— 这是为了所有用户的安全
* `key` 全仓库唯一，建议用英文小写下划线

## 索引

程序读的是 `index.json`（Gitee 优先，拉不到自动试 GitHub）。

* Gitee ：https://gitee.com/Cash553/statgi-modules
* GitHub：https://github.com/Cash-553/statgi-modules
