# 本机 Codex Skills 安装工具

本工具面向 Windows 上的本机 Codex（VS Code Codex 扩展或 Codex CLI）。
它不会改变 ChatGPT 网页对话，也不修改正在支持调查中的云环境配置。

## Windows 双击安装

在 GitHub 仓库首页选择 Code → Download ZIP，解压后打开 `local-skills-kit`，双击 `Install-Skills.cmd`。需要本机已安装 Git for Windows 与 Python 3.9 或更新版。脚本不会要求管理员权限，也不会自动替换不同内容的同名技能。

安装后双击 `Verify-Skills.cmd` 检查文件，重新打开本机 Codex 会话确认实际加载。云端助手不能替代这一步本机执行。

## 安装

1. 安装 Git for Windows、Python 3.9 或更新版，并重启 VS Code。
2. 在 VS Code 中打开本文件所在文件夹。
3. 打开终端，运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install-Skills.ps1
```

ExecutionPolicy Bypass 只用于这次进程，不永久修改系统执行策略。
安装程序从十一个原始 GitHub 仓库拉取固定提交，并保留完整源目录和 AERS 子模块。
网络较慢时需要等待较大的仓库下载。失败后保留日志；不要循环重试不明错误。

4. 安装成功后关闭原来的本机 Codex 会话，重新打开 VS Code/Codex 或开始新的本机会话。
5. 在新的本机 Codex 会话中输入：

> 请检查用户级 .agents/skills 目录，列出当前会话实际识别的 research-paper-writing、peer-review、nature-citation 等技能，分别报告文件存在和运行时加载结果。不要仅通过读取文件就宣称自动加载。

## 路径与验证

完整源文件：`%USERPROFILE%\.codex\skill-bundles\`

Codex 用户级入口：`%USERPROFILE%\.agents\skills\<调用名>\SKILL.md`

入口引导读取完整原始 SKILL.md，所有相对路径相对原文件目录解析。
合集内部技能不批量重复注册，可按需读取。

仅验证已安装文件：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install-Skills.ps1 -Verify
```

已有不同内容的同名入口或旧 `.codex/skills` 目录时，默认终止，不覆盖。
确实决定先备份再替换这些冲突时，才使用 `-BackupExisting`。
备份位于 `%USERPROFILE%\skill-backups`，复制及 SHA-256 核验通过后才移出原入口。

## 运行条件

这些是技能指令与资源的安装，不安装全部科学库、GPU 环境或 API 凭据。
Weizhena 深度调研所需的命名代理和网页搜索应按源仓库 README 在本机另行配置；本工具不自动修改模型和代理设置。
PaperSpine 的 Linux 运行时不能跨平台迁移。本工具登记阅读入口，完整运行仍需在 Windows 采用其官方 install.ps1；不要将源文件存在视为 Web 工作台就绪。
Zotero 不属于十套安装清单，本机 Zotero 连接也需单独检查。

## 验证范围

已在云端隔离测试目录验证：334 个入口的 YAML 元数据、原文件哈希、重复执行和冲突保护。
没有在用户 Windows 上执行，没有声称新本机 Codex 会话已加载这些入口。

## 后续新技能

新增技能需要同时加入 skills-manifest.json，并验证同名冲突和来源版本；重新运行安装器。
不能仅把新文件写到某一个聊天工作区，就视为所有对话可用。

## 十一套清单

- Norman-bury/research-writing-skill：17 个入口，版本 `6f7959554b4614d879d79cb4ece9ed04a7c8a88c`
- zLanqing/codex-claude-academic-skills：1 个入口，版本 `7ed6377f0efb6a38951b48ef03b19d996e454b1f`
- Yuan1z0825/nature-skills：21 个入口，版本 `7d5f160ebfe8033375b4afef7c5911aa4203c983`
- HKUSTDial/Supervisor-Skills：12 个入口，版本 `207bc6f7a1aa107e544099c2c7cc86816fba9628`
- K-Dense-AI/scientific-agent-skills：177 个入口，版本 `92ace75ac21efe19a620434e0ca4e356081fe807`
- brycewang-stanford/Auto-Empirical-Research-Skills：1 个入口，版本 `9fa87d86e34d6c9a1c7cdb0db755c83c780537a0`
- Master-cai/Research-Paper-Writing-Skills：1 个入口，版本 `77e7c2c1ba06f7d71844873147665437a03aac1b`
- Orchestra-Research/AI-Research-SKILLs：97 个入口，版本 `773a52944ba4747a18bd4ae9ade53fff041adcbc`
- Weizhena/Deep-Research-skills：5 个入口，版本 `6ce38f60e3f8b22502c29873f96503a4e0c5addb`
- WUBING2023/PaperSpine：1 个入口，版本 `f7e3dabaf499b2aef1eabdd1cd5d64f173d7dcc3`

## Windows 换行兼容

Git for Windows 可能将 LF 转换为 CRLF。安装器保持原校验值，通过 Git 原始对象核验并仅接受换行差异；内容改动仍然拒绝。新下载的仓库关闭本仓库的 autocrlf 转换，不修改全局 Git 设置。


## 单独添加 PPT Master

已有333个入口的用户，下载最新版工具包并解压后，双击 `Install-PPT-Master.cmd`。
只添加 `ppt-master`，保留已安装的333个入口，不重新拉取全部仓库。

源仓库：hugohe3/ppt-master，固定提交 `8070d3df1f6f54b5fb60a9ae66e79c664f050212`。
其完整源文件、模板、工作流与脚本保留在用户 `.codex/skill-bundles`。
其依赖安装在用户 `.codex/skill-runtimes/ppt-master` 独立虚拟环境中。
安装入口会向 Codex 提供该虚拟环境的 Python 绝对路径。
需要 Python 3.10+；API密钥和可选的图像生成、旁白服务应按具体任务另行配置。

PowerShell方式：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install-Skills.ps1 -Only ppt-master
```

首次安装完成后，重开本机 Codex 会话，检查 `ppt-master` 是否在 Available skills 清单中。
