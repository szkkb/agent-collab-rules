# Agent 协作规则（可移植模板）

一套给编码 Agent 用的协作规则与自维护工具。它约束的不是某个项目的架构，而是**人、Agent 与工作区之间的协作方式**：怎么算做完、改动归属谁、什么时候可以上传 GitHub、收尾要留什么证据。

原始版本运行在一台真实机器上，覆盖多个客户端；这里是**去除机器专属内容后的可移植版本**——真实人名、本机路径、私有备份目录、客户端安装拓扑和提交邮箱都不在其中。

## 包含什么

| 文件 | 作用 |
|---|---|
| `CLAUDE.md` | 规则正文，唯一权威副本。分七节：完成度、共享工作区、生产与数据、项目与 skill 维护、协作场地、上下文加载、Git/GitHub 归属边界 |
| `AGENTS.md` | 指针文件。只负责把只认 `AGENTS.md` 的客户端引到 `CLAUDE.md`，不复制正文 |
| `scripts/audit-rules.py` | 只读自检：规则体积预算、必需小节是否存在、清单与 Git 跟踪文件是否一致 |
| `skills/closeout/SKILL.md` | 收尾 skill：按项目现有协议记录成果、更新待办、提交改动 |
| `TRACKED_FILES.txt` | 已审核的跟踪文件清单，配合默认拒绝的 `.gitignore` 使用 |
| `LICENSE` | CC0 1.0 Universal 法律文本 |

## 怎么用

把仓库检出到你想放规则的位置，然后把各客户端的入口指向 `CLAUDE.md`。常见做法是软链接：

```sh
git clone https://github.com/szkkb/agent-collab-rules.git ~/agent-collab-rules

# 按你实际使用的客户端择一或全部
ln -s ~/agent-collab-rules/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/agent-collab-rules/CLAUDE.md ~/.codex/AGENTS.md
ln -s ~/agent-collab-rules/CLAUDE.md ~/.gemini/GEMINI.md
```

自检：

```sh
python3 scripts/audit-rules.py
```

脚本以本仓库根为默认目标，也可显式指定：`python3 scripts/audit-rules.py --root /path/to/rules`。它只做文件和清单一致性检查，**不检查任何客户端的安装情况，也不验证规则是否真的被加载或遵守**。

### 采用前请按自己的情况改写

规则里的多数条目是稳定约定，但有几处需要你替换成自己的值：

- `CLAUDE.md` 的「人与 Agent 协作场地」一节使用 `<home>`、`<workspace-root>`、`<handoff-dir>` 占位符——换成你的真实路径，或保留占位符并在别处定义。
- 「生产与数据」一节提到了 `prisma` 系列命令作为例子。不用 Prisma 就换成你实际的迁移工具，或删掉该条的具体命令名。
- `skills/closeout/SKILL.md` 的协议探测顺序（项目自有版 → changeset → session-log → lite）按你项目的实际惯例调整。
- 整套规则本身是**意见**，不是规范。不同意某条就改，改完跑一次自检。

## 边界与已知限制

- **`AGENTS.md` 是指针，不是副本。** 只维护 `CLAUDE.md`；在 `AGENTS.md` 里复制正文会立刻产生两份会漂移的真源。
- **`.gitignore` 不是保密边界。** 它是默认拒绝清单，用来减少误加；它拦不住强制添加，也拦不住已跟踪文件再次提交。敏感内容只能靠提交前逐项检查 `git diff --cached`。
- **自检脚本不是权限拦截器。** 它验证的是文件状态，不是运行行为。「文件可读」「加载器读到」「新会话遵守」是三层不同的证据，下一层不能由上一层推出。
- **软链接在部分环境下不可用**（例如 Windows 需要开发者模式或管理员权限，某些工具不跟随符号链接）。这种情况下改为复制文件，并自己承担同步责任。
- **本模板未在多种客户端上做过新会话行为验收。** 文件级检查通过不等于规则实际生效。

## 来源与许可

规则来自一套实际使用中的个人协作约定，公开前已做去个人化处理。

以 [CC0 1.0 Universal](LICENSE) 发布：在法律允许的最大范围内，作者已放弃本作品的全部著作权及相关权利。你可以自由复制、修改、再发布，**无需署名、无需保留本说明**。

需要留意的两点：

- CC0 第 4(a) 条明确**不放弃商标权和专利权**。本仓库是文档与脚本，不涉及专利授权；若你要把其中的代码用于专利敏感的场景，请自行评估。
- CC0 放弃的是著作权，不构成对使用者的担保；规则文本按「现状」提供。

## 维护

只改 `CLAUDE.md` 正文。新增文件时同时更新 `TRACKED_FILES.txt` 和 `.gitignore`，再逐个暂存并运行自检：

```sh
git status --short
git add -- CLAUDE.md
python3 scripts/audit-rules.py
git diff --cached
git diff --cached --check
git commit -m "docs: refine collaboration rules"
```

不要用 `git add .` / `git add -A` 在混合目录里无差别暂存。
