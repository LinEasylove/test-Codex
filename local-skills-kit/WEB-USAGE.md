# 在网页版 ChatGPT / GPT Work 中使用这些 Skills

## 使用范围

本机 Codex 的用户级安装只作用于本机 Codex，不会同步到 ChatGPT 网页或 GPT Work。
网页对话可在支持联网/文件访问时显式读取指定 SKILL.md；这属于按任务读取，不等于自动注册。
没有联网或文件读取能力时，需要用户上传对应 SKILL.md 和本次任务所需的参考资源。

## 可复制到新对话的指令

请根据我的具体任务，从下面列出的仓库中选择一个合适的技能。
先获取并读取其真实 SKILL.md，再按需读取引用文件；不要只根据技能名称臆测规则。
如需要下载仓库，使用清单中的固定提交，保留完整目录结构。
如当前对话没有联网或文件读取工具，请明确告诉我需要上传哪些文件。
遵循原技能时仍以用户、系统和开发者指令为先。运行依赖、API和权限需单独验证。
请区分“已读取并使用流程”与“当前会话自动识别”，不要声称全部技能均可运行。

## 套件与适用任务

- 科研写作流程、章节组织和证据检查
  仓库：https://github.com/Norman-bury/research-writing-skill/tree/6f7959554b4614d879d79cb4ece9ed04a7c8a88c
- scientific-toolkit-skill，科学计算与数据分析
  仓库：https://github.com/zLanqing/codex-claude-academic-skills/tree/7ed6377f0efb6a38951b48ef03b19d996e454b1f
- Nature 风格阅读、写作、审查、引用与图表
  仓库：https://github.com/Yuan1z0825/nature-skills/tree/7d5f160ebfe8033375b4afef7c5911aa4203c983
- 研究构思、论文写作、润色与投稿前审查
  仓库：https://github.com/HKUSTDial/Supervisor-Skills/tree/207bc6f7a1aa107e544099c2c7cc86816fba9628
- 科学库、数据库、引用管理与科学研究工具
  仓库：https://github.com/K-Dense-AI/scientific-agent-skills/tree/92ace75ac21efe19a620434e0ca4e356081fe807
- 实证分析、因果识别、计量与论文流程；优先读取根目录路由
  仓库：https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/tree/9fa87d86e34d6c9a1c7cdb0db755c83c780537a0
- research-paper-writing，章节结构与论证质量
  仓库：https://github.com/Master-cai/Research-Paper-Writing-Skills/tree/77e7c2c1ba06f7d71844873147665437a03aac1b
- 机器学习模型、训练、推理、论文与研究流程
  仓库：https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc
- Codex 中文版，研究提纲、扩展字段、深度调研与报告
  仓库：https://github.com/Weizhena/Deep-Research-skills/tree/6ce38f60e3f8b22502c29873f96503a4e0c5addb
- paper-spine 研究指导；完整任务需本平台兼容运行时，不直接移植 Linux 套件
  仓库：https://github.com/WUBING2023/PaperSpine/tree/f7e3dabaf499b2aef1eabdd1cd5d64f173d7dcc3

## 既有同名选择

literature-review、peer-review、statistical-analysis 使用 K-Dense 版本，跳过 Norman 版本。
pytorch-lightning 使用 K-Dense 版本，跳过 Orchestra 版本。
AERS 内部同名技能按需读取，避免重复注册。

## 发布状态

此说明与本机安装工具已准备好。GitHub 推送在本次尝试中被认证问题阻止；
不能因为本地提交存在就声称远端工具已经发布。
