# 10 Tips & Pitfalls

Running log of useful lessons from this learning program. Add one per week — by
Week 10 this becomes the team-facing writeup referenced in the DoD.

Each entry: **title**, one-sentence takeaway, optional code snippet, and the
concrete incident that prompted it.

---

## 01. 不要用 notebook cell 去改写 src/ 里的 .py 文件

**Takeaway:** 改 `src/` 下的 `.py` 文件就直接在编辑器里打开改，notebook 只负责 `import` 和调用；
加 `%load_ext autoreload` + `%autoreload 2` 让改动自动生效。

**Why it matters:** Week 1 我想把一个稳定下来的 helper 从 notebook 搬进 `src/spatial_notebooks/stats.py`，
偷懒用 cell 里的 `%%writefile -a` 和 `open(path, "a").write(code)` 直接往文件尾追加。问题是：
写"含 Python 代码的字符串"时，Jupyter 的 auto-indent 会把三引号内的缩进偷偷改错（`if` 变 8 空格、`return` 变 16 空格），
生成的 `stats.py` 一坏下一次 `import` 就 `IndentationError`。然后我再写一个 cell 去"修复"，
同样的坑再踩一次，循环 4 轮才跳出来。根因是**用 Python 去生成 Python 源码**这件事本身就脆弱。

```python
# ❌ Don't — 在 notebook 里用字符串生成 .py 内容
code = """
def foo():
    if x:
        return y
"""
open("mymodule.py", "a").write(code)  # 缩进随时被 auto-indent 弄坏

# ✅ Do — 编辑器改文件，notebook 只 import
# (notebook 顶部一次)
%load_ext autoreload
%autoreload 2
from mymodule import foo
```

## 02. 你的包写了类型不等于"类型化"——必须有 `py.typed`

**Takeaway:** 在包根放一个空的 `py.typed` 文件（PEP 561），并确保打包配置会把它包进 wheel；
没有它，mypy 会直接跳过分析你的包，即使你的每个函数都写了完美的 type hint。

**Why it matters:** Week 2 打开 `strict = true` 后，`uv run nbqa mypy notebooks/` 报了
`module is installed, but missing library stubs or py.typed marker [import-untyped]`。
代码的类型标注从 Week 1 就是完整的，mypy 检查 `src/` 时没问题——因为它直接读源码。
但从 notebook import 时走的是安装路径（`.venv/lib/…`），mypy 需要看到 `py.typed` 才肯信任。
**类型标注是给人写的，`py.typed` 是给工具看的**——两者缺一不可。

```
src/spatial_notebooks/
├── __init__.py
├── py.typed          ← 空文件，存在即声明"我是类型化的"
├── stats.py
└── cli.py
```

打包配置也要跟上（否则只在源码里有，别人 pip install 后没有）：

```toml
# pyproject.toml
[tool.hatch.build.targets.wheel.force-include]
"src/spatial_notebooks/py.typed" = "spatial_notebooks/py.typed"
```

## 03. Notebook 的可复现性要验给「重置后的自己」看，不是给「已经跑过的自己」看

**Takeaway:** 开发中可以随便乱序执行 cell、反复试错；但交付前必须做一次 **Kernel → Restart Kernel and Run All Cells**，
从空内核一把跑通到尾。只有这一次跑通的状态，才等于「别人 clone 下来也能跑通」的状态。

**Why it matters:** Week 3 我在 `02_jupyter_workflow.ipynb` 里反复试 `add_density` 的不同实现，
中间有几个 cell 依赖了上面删掉的变量、或是顺序被我手动打乱过——在当前内核里因为内存里还留着旧值，一路绿灯。
要不是临交付前按了 Restart & Run All，这个 notebook 导出成 HTML 发给同事之后，对方 `uv sync` + 重跑会直接在第 4 个 cell 炸掉
（`NameError: name 'df_clean' is not defined`），而我自己那边怎么试都「明明好好的」。
**Notebook 的当前内核状态 ≠ 源码状态**——可复现性只认源码。

```bash
# 交付前三连击（顺序不能错）
# 1. 清掉所有输出，避免老输出误导读者
#    JupyterLab: Edit → Clear Outputs of All Cells
# 2. 重启内核并从头跑
#    JupyterLab: Kernel → Restart Kernel and Run All Cells
# 3. 导出 HTML 给非技术读者 / 老板
uv run jupyter nbconvert --to html notebooks/02_jupyter_workflow.ipynb
```

配套的三条纪律：

- **新实验永远加在最下面。** 想不破坏叙事顺序地试一段代码？在 notebook 末尾新开 cell，验完再决定要不要合回叙事里。
- **每个 code cell 上方配一个 Markdown cell**，写「这个 cell 回答什么问题」。Restart & Run All 时你在读的是叙事，不是代码。
- **`%autoreload 2` 覆盖不到新函数签名。** 改 `src/` 里已有函数的实现会自动生效；新增函数 / 改参数列表仍需 Restart。

```python
# ❌ Don't — 依赖内核里「还活着」的变量
# cell 5 定义了 df_clean
# cell 9 用 df_clean 画图
# 后来把 cell 5 删了，cell 9 在当前内核里照样能跑（内存还在），
# 但 Restart & Run All 会立刻 NameError。

# ✅ Do — 每个叙事步骤自给自足，或显式依赖上一步的输出变量
# 交付前强制 Restart & Run All，用空内核验证一次。
```

<!-- Template

## NN. Short, opinionated title

**Takeaway:** one sentence someone can act on.

**Why it matters:** what went wrong or nearly went wrong.

```python
# optional minimal example
```

-->
