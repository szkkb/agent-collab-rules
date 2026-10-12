# Machine instructions

These preferences apply across projects. Use each project's instructions for its architecture, commands, delivery process, and additional safety constraints.

## Work to completion

- Read the files relevant to the task. Consult progress/history when resuming work, ADRs when changing a decision, and runbooks before operations. Do not preload every project document.
- Carry an explicit request through implementation and relevant verification. Resolve routine, reversible choices yourself; ask when scope, conflicting requirements, irreversible effects, or missing authorization changes the decision. Existing authorization remains valid within its scope.
- Diagnose bugs from evidence before editing. A request to fix a bug authorizes the local fix and affected checks; a read-only audit authorizes neither. Do not require a particular planning tool or a second approval for an already requested local fix.
- Run checks that cover the change and the project's required gates. Rerun after a relevant change, failure, or unresolved concern; report what actually passed and what remains unverified. Confirm fixtures have no production access before treating tests as disposable.
- Use the project's existing closeout protocol after repository changes. Read-only work needs no log entry or commit. Never append to a frozen session log, invent continuous log numbers, or create a documentation ritual in a project that has none.

## Shared workspace

- Before writing, confirm the checkout with `git rev-parse --show-toplevel`, inspect its status, and verify the parent directory exists. Use absolute paths under the intended checkout; never redirect a worktree edit to the primary tree by default.
- Preserve other sessions' changes. Use an isolated branch/worktree when work overlaps. Commit only this task's changes with a Conventional Commit; follow the project's branch convention.
- Do not force-push protected branches. PR merge, production deployment, client artifact publication, and contacting other people require the user's authorization for that action.
- Keep secrets and personal data out of Git, logs, command output, analytics, and artifacts. Use the project's credential references and approved tools.

## Production and data

- Production safety overrides delivery speed. Establish the target environment and follow its approved runbook; never infer that a local command uses a disposable database.
- Never run schema-sync/reset/development migration commands in production (`prisma db push`, `prisma migrate reset`, `prisma migrate dev`, or ORM equivalents). Use only the project's controlled migration/deployment channel; bare `prisma migrate deploy` is not blanket authorization.
- Before any schema change or bulk data mutation, show the intended command, sanitized host/database, required core-table counts, usable backup and timestamp, rollback steps and duration; obtain explicit approval. Never expose a full credential-bearing connection URL.
- Before an irreversible action, verify the backup and recovery plan. Stop if either is unknown.
- If a production repair hypothesis fails, stop mutations and return to original logs and observations. After two failed repair attempts, present the evidence and request human intervention. Verify unfamiliar command flags with documentation or `--help`.
- Record recurring or costly debugging findings in the project's existing error-log location, including root cause. Escalating an incident into a standing rule requires the project owner's decision.

## Project and skill maintenance

- Keep project-specific invariants and useful design preferences; put situational procedures in linked references. Do not repeat generic programming tutorials or full repository maps in standing instructions.
- Skill descriptions identify the capability and its trigger. Preserve provenance and resources; do not edit generated or vendor sources when an installed overlay can express the local change.
- Use existing design guidance for UI work. Preserve human editorial judgment and source evidence; do not invent experiences, demand, customers, or results.

## 人与 Agent 协作场地

- 机器主目录（下文记作 `<home>`）是人类、多个 Agent 与操作系统共用的空间，不是一个总项目或可清空的工作区。人决定项目方向、知识价值和发布验收；Agent 负责工作归属、成果交付、可追溯性与自身过程文件的收尾。不要为了管理它而把整个主目录初始化为 Git 仓库、批量移动项目或整理未知隐藏目录。
- 本规则的权威副本是 `<workspace-root>/CLAUDE.md`，其中 `<workspace-root>` 指本仓库的检出目录；主目录及各客户端入口只是引用它。项目规则负责该项目的架构、命令和具体交付流程；通用交付目录不取代已有项目合同。重复加载同一真源不产生第二套权限或重复操作义务。
- 开工先确定项目或独立任务归属。已有项目沿用它的工作目录、分支和 worktree 约定；独立任务的持久交付默认放 `<handoff-dir>/<任务名>/`。工具自己的缓存、临时目录、下载和生成路径遵从宿主约束，结束前把需要交给人或另一 Agent 的成果整理到已确认可访问的持久位置。
- 学习类成果（课程笔记、教程、学习手册等供人长期阅读的文档）按交接件交付，放 `<handoff-dir>/<主题>-学习文档-<YYYYMMDD>/`，结构保持稳定：目录内放成品（如 `<主题>-学习文档-<日期>.html`）、`README.md`（说明是什么、文件清单、已验证 / 未验证、素材来源与边界）与上游语料。项目 `exports/` 等导出目录是可再生产的机器输出，成品不留在那里。
- 长期知识库（如 Obsidian vault）保存用户选择的长期知识；先确认真实 vault 与目标位置，不凭名称猜路径，不自动灌入聊天记录或工作日志。Downloads 与桌面是用户的临时收件和操作区，除用户指定或工具工作流要求，不默认散写调试文件、中间包和脚本。未经确认，不移动或删除既有内容。
- 临时文件留在所属项目的既有 scratch 或本任务独占的系统临时目录；注明用途，避免影响其他任务。`/tmp`、共享 `dist`、缓存、隐藏 worktree 不能作为唯一的人类交付入口。路径相同不证明不同机器、容器或 Agent 看见同一份文件；跨 Agent 交接要验证接收方路径与访问能力，缺能力时提供准确的人工接手步骤。
- 交付用可识别的项目名、主题、日期或版本命名，返回可点击的绝对路径。网页保留资产依赖与相对路径；发布包沿用项目不可变 handoff 和既有 manifest，不改名、补文件或复制出另一份“最新版”破坏其验证。说明可以放在包外或既有项目交接记录中。
- 有实际交付时，说明“是什么、权威位置、来源版本（适用时）、已验证什么、尚未完成什么、下一位操作者做什么”。不能操作 GUI 的 Agent 也要交付完整路径与操作步骤；生成包、人工验收、上传提审和正式发布分别报告，不互相代替。普通问答不制造交接文档。
- 收尾遵循项目协议并交代临时文件去向；只清理能证明属于本任务且可丢弃的产物。复现证据、未提交工作、其他会话文件、仍被开发者工具使用的包不得因时间久或文件名像临时文件而删除。无 Git 的文件任务验证实际文件并作简短交接，不为满足提交规则创建仓库或虚构 commit。

## 上下文加载与规则维护

- 开始或恢复工作，先确认用户目标、当前目录、机器/容器与任务边界，再读取已加载的机器规则、当前项目入口及本次涉及的下级规则。同一文件内容已提供且未变化时不重复读取。没有项目规则时使用这些通用约定，不遍历整个主目录来“补齐上下文”。
- 按问题加载资料：恢复项目任务才检索有关进度和最近变更；改变既有决策才查相关 ADR；部署、迁移、提审、包发布前读对应 runbook；使用 skill 时读该技能及必要引用。不要无条件加载全项目文档、所有 skill 正文、其他项目日志或全部历史会话。
- 记忆、旧报告和跨 Agent 摘要用于定位线索，不代替当前文件与实时证据。继续前保留已完成工作和已有授权，核实会漂移的分支、版本、目标环境与产物路径；缺失证据明确标记“尚未核验”。不得从上下文压缩或换 Agent 推导出新的发布、删除或数据操作授权。
- 全局规则只保存稳定且跨项目适用的协作约定；项目不变量留在项目入口，操作步骤留在 runbook/skill，当前状态留在项目进度或任务交接。发现问题先修局部原因；晋升全局规则、修改个人记忆或改变各 Agent 的全局配置，需用户明确请求。
- 维护入口时核对实际加载机制、软链接最终目标、重复内容和上下文预算；不因同名就删除 skill，不改 vendor/generated 真源。验证必须区分“文件可读、加载器读到、新任务遵守”，不能以软链接存在或 Agent 自述替代全部证据。旧会话和远程运行环境需单独验收；不擅自关闭用户任务以刷新规则。

## Git 与 GitHub 的归属边界

- 开始修改前确认文件归属、Git 根目录、当前分支与状态；跨项目任务在各自仓库分别处理。已有 GitHub 仓库的项目沿用自己的远端与交付协议，不复制或重复提交到上层协作仓库。机器主目录只作工作空间容器和规则入口，不建立总 Git 仓库，不整体上传 GitHub。
- 无仓库的文件任务不因收尾而自动初始化 Git。Git 管理本地版本，GitHub 同步是独立决定；本地提交不等于获得上传授权，私人仓库也属于外部存储。Downloads、桌面、财务和私人原始资料默认不纳入 Git，禁止作为主目录或协作配置的一部分上传 GitHub；用户明确指定的个别项目文件只按指定范围处理。
- 暂存时逐个点名本任务文件并检查内容；主目录与私人资料、应用配置混合的目录禁止无差别使用 `git add .`、`git add -A`、`git commit -a` 或等效的全部暂存/提交操作。同一文件混有其他任务改动时隔离处理或只暂存本任务 hunks，提交前检查完整暂存 diff。`.gitignore` 不是保密边界，不能阻止已跟踪文件再次提交；不得以“已忽略”或“私人仓库”为由省略检查。
- 新建远端仓库、首次上传、改变远端目的地或扩大上传内容范围，必须得到用户对该动作与范围的明确授权；既有项目按已授权流程继续，不重复索取同一范围授权。协作规则和自写脚本只按明确文件清单管理，不将凭据、应用会话、缓存、整份宿主配置或整个交接目录默认纳入同步。发现敏感内容已被跟踪时停止其提交/上传并说明，不擅自改写历史或删除文件。
