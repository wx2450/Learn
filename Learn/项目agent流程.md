# Codex 项目处理标准流程

在使用 Codex 处理一个新项目时，建议先建立 Git 版本管理和 Python 独立环境，再配置项目规则、制定任务计划，最后分步骤执行和检查。

这样可以避免代码无法回退、不同项目依赖冲突，以及 Codex 一次性大范围修改代码。

---

## 一、进入项目目录

进入已有项目：

```bash
cd ~/Learn
```

新建项目时：

```bash
mkdir ~/my_project
cd ~/my_project
```

后续所有 Git、Python 环境和 Codex 操作，都应在该项目目录中进行。

---

## 二、使用 Git 进行版本管理

先检查项目是否已经是 Git 仓库：

```bash
git status
```

如果提示当前目录不是 Git 仓库，执行：

```bash
git init
```

Git 用于记录代码变化、对比修改内容和恢复历史版本。

建议先配置 Git 用户信息：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

查看当前状态：

```bash
git status
```

首次保存项目版本：

```bash
git add .
git commit -m "initial project version"
```

在让 Codex 修改代码前，建议先建立一个可回退版本：

```bash
git status
git add .
git commit -m "backup before codex changes"
```

如果当前存在尚未完成的修改，不要盲目提交，应先确认这些修改是否需要保留。

---

## 三、使用 `.venv` 隔离 Python 环境

Python 项目建议在项目根目录创建独立虚拟环境：

```bash
python3 -m venv .venv
```

激活虚拟环境：

```bash
source .venv/bin/activate
```

激活后，终端前面通常会出现：

```text
(.venv)
```

升级项目环境中的 pip：

```bash
python -m pip install --upgrade pip
```

安装项目需要的依赖：

```bash
python -m pip install numpy
```

或者：

```bash
python -m pip install -r requirements.txt
```

导出当前依赖：

```bash
python -m pip freeze > requirements.txt
```

退出虚拟环境：

```bash
deactivate
```

`.venv` 只负责隔离 Python 和第三方库，不负责代码版本管理。代码版本由 Git 管理。

---


每次进入项目执行：

cd ~/Learn
source .venv/bin/activate
codex




## 四、创建 `.gitignore`

`.venv` 不应该提交到 Git 仓库。

在项目根目录创建：

```bash
nano .gitignore
```

建议写入：

```gitignore
# Python virtual environment
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Environment variables
.env

# Build outputs
build/
dist/

# IDE files
.vscode/
.idea/
```

其中 `.vscode/` 是否忽略，可根据项目是否需要共享 VS Code 配置决定。

保存后检查：

```bash
git status
```

确保 Git 没有准备跟踪 `.venv` 中的大量文件。

如果 `.venv` 已经被 Git 跟踪，需要执行：

```bash
git rm -r --cached .venv
```

然后重新提交：

```bash
git add .gitignore
git commit -m "ignore Python virtual environment"
```

---

## 五、项目推荐结构

一个普通 Python 项目可以采用：

```text
my_project/
├── .git/
├── .venv/
├── .gitignore
├── AGENTS.md
├── requirements.txt
├── README.md
├── src/
├── tests/
└── scripts/
```

各部分作用：

```text
.git/             Git 版本历史
.venv/            当前项目独立的 Python 环境
.gitignore        指定 Git 不需要管理的文件
AGENTS.md         Codex 在该项目中长期遵守的规则
requirements.txt  项目 Python 依赖清单
README.md         项目说明和使用方式
src/              主要源代码
tests/            测试代码
```

---

## 六、配置 Codex 项目权限

创建或修改 Codex 配置：

```bash
mkdir -p ~/.codex
nano ~/.codex/config.toml
```

写入：

```toml
approval_policy = "never"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

这套配置允许 Codex：

* 读取当前项目文件；
* 修改当前项目文件；
* 执行编译和测试；
* 联网下载 Python 依赖；
* 不再频繁询问操作权限。

同时，不会主动允许 Codex 修改项目外的普通文件。

启动 Codex 时必须先进入具体项目目录：

```bash
cd ~/Learn
source .venv/bin/activate
codex
```

不要直接在整个家目录启动：

```bash
cd ~
codex
```

否则 Codex 的工作区范围可能过大。

---

## 七、使用 `/init` 生成 `AGENTS.md`

进入 Codex 后执行：

```text
/init
```

该命令会在当前项目中生成 `AGENTS.md`。

`AGENTS.md` 用于记录 Codex 在当前仓库中长期需要遵守的规则，例如：

* 项目结构；
* 编译和运行方式；
* 测试命令；
* 代码风格；
* 禁止修改的接口；
* 硬件资源限制；
* 修改后的验证要求；
* 什么状态才算任务完成。

生成后，让 Codex 根据真实项目完善它：

```text
请阅读当前项目中的 README、目录结构、构建文件和主要源码，完善 AGENTS.md。

要求补充：
1. 项目结构和主要模块；
2. 正确的编译、运行和测试命令；
3. 当前项目的代码风格；
4. 不允许随意修改的接口、配置和资源；
5. 每次修改后的验证要求。

只修改 AGENTS.md，不要修改其他文件。
不要编造项目中不存在的命令或目录。
```

完成后人工检查 `AGENTS.md`，确认其中的目录、命令和规则符合项目实际情况。

---

## 八、重新启动 Codex

完善 `AGENTS.md` 后，可以退出：

```text
/exit
```

然后重新进入：

```bash
cd ~/Learn
source .venv/bin/activate
codex
```

重新启动后，Codex 会在新会话中重新读取项目里的 `AGENTS.md`。

---

## 九、使用 `/plan` 制定任务计划

进入 Codex 后执行：

```text
/plan
```

然后输入当前需要处理的具体任务，例如：

```text
请先分析当前任务并制定实施计划。

要求：
1. 阅读所有相关文件和调用关系；
2. 明确需要修改哪些文件；
3. 说明每个修改点的原因；
4. 优先采用最小修改方案；
5. 不随意修改已有接口和变量名；
6. 指出可能的兼容性风险；
7. 给出编译和验证方法；
8. 目前只生成计划，不修改任何文件。
```

`/plan` 生成的是当前任务的实施计划，不是长期项目规则。

简单区分：

```text
AGENTS.md：整个项目长期遵守的规则
/plan：当前这个任务的具体实施步骤
Git：保存和回退代码版本
.venv：隔离当前项目的 Python 环境
```

---

## 十、人工审查计划

计划生成后，不要立即开始修改。

重点检查：

* 是否遗漏相关文件；
* 是否改动范围过大；
* 是否改变已有接口；
* 是否存在不必要的重构；
* 是否修改了无关模块；
* 是否给出了编译或测试方法；
* 是否能拆成多个可单独验证的小步骤。

计划不合适时，让 Codex重新修改：

```text
当前计划改动范围太大。

请重新设计：
1. 保留现有接口；
2. 不进行无关重构；
3. 尽量减少修改文件数量；
4. 将计划拆成可以逐步验证的小步骤；
5. 仍然只修改计划，不要写代码。
```

---

## 十一、分步骤执行

计划确认后，输入：

```text
现在按照计划开始实施。

要求：
1. 一次只执行一个步骤；
2. 不提前执行后续步骤；
3. 每完成一步，说明修改了哪些文件；
4. 说明具体修改内容；
5. 执行对应的编译或测试；
6. 汇报验证结果；
7. 当前步骤完成后停止。
```

当前步骤确认无误后，再输入：

```text
继续执行下一步。
```

这种方式可以防止 Codex 一次性修改大量代码。

---

## 十二、每一步都检查 Git 差异

Codex 每完成一步后，应执行：

```bash
git status
git diff --check
git diff
```

各命令作用：

```text
git status
查看哪些文件被修改、新增或删除

git diff --check
检查空白错误和部分格式问题

git diff
查看具体代码变化
```

重点检查：

* 是否修改了无关代码；
* 是否出现大范围格式变化；
* 是否误删已有功能；
* 头文件和源文件是否一致；
* 新增配置是否真正生效；
* 默认行为是否保持兼容；
* 是否意外修改了依赖文件；
* 是否生成了不应提交的临时文件。

---

## 十三、执行编译和测试

根据项目类型执行真实可用的验证命令。

### Python 项目

```bash
source .venv/bin/activate
python -m compileall .
```

有测试时：

```bash
python -m pytest
```

### CMake 项目

```bash
cmake -S . -B build
cmake --build build -j
```

### Make 项目

```bash
make -j
```

只运行当前仓库真实支持的命令，不要编造不存在的测试方式。

如果验证失败，Codex 应说明：

* 执行了什么命令；
* 在哪里失败；
* 是代码问题还是环境问题；
* 当前还有哪些内容没有验证。

---

## 十四、每完成一个稳定阶段就创建 Git 提交

当一个步骤已经修改完成并验证通过，可以创建提交：

```bash
git add .
git commit -m "描述本次修改"
```

例如：

```bash
git commit -m "add inquire mode support"
```

建议一个提交只对应一个明确功能或修复。

不要把完全无关的多个修改混在同一个提交中。

常用提交节奏：

```text
建立初始项目
→ 提交一次

完善 AGENTS.md
→ 提交一次

完成计划第一阶段
→ 验证后提交一次

完成计划第二阶段
→ 验证后提交一次

全部完成
→ 最终审查后提交一次
```

除非明确要求，否则不要让 Codex自动执行：

```bash
git push
git reset --hard
git clean -fd
git rebase
```

---

## 十五、最终代码审查

全部步骤完成后，在 Codex 中执行：

```text
/review
```

要求 Codex重点检查：

* 潜在逻辑错误；
* 行为变化；
* 兼容性问题；
* 遗漏测试；
* 边界条件；
* 未使用变量；
* 错误的配置默认值；
* 意外修改的文件；
* 可能出现的回归问题。

最终再检查：

```bash
git status
git diff --check
git diff
```

确认无误后提交：

```bash
git add .
git commit -m "complete current task"
```

需要上传到远程仓库时，最后由用户决定是否执行：

```bash
git push
```

---

## 十六、其他电脑恢复项目环境

Git 不保存 `.venv`，只保存代码和依赖清单。

在另一台电脑克隆项目后：

```bash
git clone 仓库地址
cd 项目目录
```

重新创建虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

然后启动 Codex：

```bash
codex
```

这样可以恢复项目代码和 Python 依赖环境，同时避免直接复制庞大的 `.venv` 文件夹。

---

# 完整推荐流程

```text
进入项目目录
→ 初始化 Git
→ 创建 .gitignore
→ 创建 .venv
→ 激活 Python 虚拟环境
→ 安装并记录项目依赖
→ 建立初始 Git 提交
→ 配置 Codex 工作区读写和网络权限
→ 启动 Codex
→ 使用 /init 生成 AGENTS.md
→ 根据真实项目完善 AGENTS.md
→ 人工检查并提交 AGENTS.md
→ 退出并重新启动 Codex
→ 使用 /plan 制定当前任务计划
→ 人工审查并调整计划
→ 要求一次只执行一个步骤
→ 每一步执行编译或测试
→ 每一步检查 git diff
→ 稳定阶段分别创建 Git 提交
→ 全部完成后使用 /review
→ 最终检查并提交
→ 根据需要推送到远程仓库
```

---

# 核心原则

```text
Git 管理代码版本
.venv 隔离 Python 环境
requirements.txt 记录 Python 依赖
AGENTS.md 记录项目长期规则
/plan 制定当前任务步骤
Codex 负责分析和修改
用户负责检查计划、差异和最终结果
```

项目处理时应始终坚持：

* 先建立可回退版本；
* 每个项目使用独立 Python 环境；
* 不提交 `.venv`；
* 先制定规则，再制定计划；
* 计划确认后再修改；
* 一次只完成一个步骤；
* 每一步都执行验证；
* 每个稳定阶段都保存 Git 版本；
* 最后统一审查。

TODO:需要放在agent.md中，遵守这个规则
## Python 环境

本项目使用项目根目录中的 `.venv`。

执行 Python、pip 和测试命令前，必须确认使用 `.venv` 中的解释器。优先使用：

- `.venv/bin/python`
- `.venv/bin/python -m pip`
- `.venv/bin/python -m pytest`

不要使用 `sudo pip` 或 `pip install --user`。