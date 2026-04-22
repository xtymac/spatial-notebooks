# Week 4 — Kickoff prompt

Paste this into a fresh Claude session to start Week 4 work.

---

我在做 `spatial-notebooks` 学习项目（https://github.com/xtymac/spatial-notebooks），Week 1–3 已经完成（Python 基础 / mypy strict / Jupyter 工作流 + 可复现性）。现在开始 **Week 4 — pandas + matplotlib（数据分析 + 可视化）**。

计划在 `docs/learning-plan.md` 的 **Week 4 checklist**：

- [ ] 下载一份真实数据集（优先名古屋市 open data，或手头项目相关数据）
- [ ] 原始数据放 `data/raw/`（已 gitignore），在 `src/` 写 loading 脚本
- [ ] 新建 `notebooks/03_data_analysis.ipynb`
- [ ] 数据清洗流水线：处理 NaN、修 dtype、统一列名
- [ ] 用 matplotlib 画 3 张探索性图（分布、趋势、对比各 1 张，每张都要回答一个具体问题，不要「这是一张图」）
- [ ] 把 `clean_*()` 函数抽到 `src/spatial_notebooks/`，配 pytest 测试
- [ ] 在 `docs/tips.md` 写 Tip #04
- [ ] 周五异步更新（1 张截图 + 3 行：学到什么 / 做了什么 / 下周计划）

要学 & 贴近工作：

- **pandas**：`read_csv` / `groupby` / `merge` / `pivot_table` / `resample`
- **numpy**：向量化、broadcasting、`np.where`
- **matplotlib**：figure/axes/subplots/`savefig`
- 复用 `docs/learning-plan.md` 里已有的 pandas / matplotlib pattern（Useful patterns 小节）

要守的纪律（从 Week 1–3 沉淀下来的）：

1. **数据处理逻辑稳定后立刻抽到 `src/`**，notebook 只负责叙事 + 调用；`src/` 函数必须有 pytest 测试（参考 `docs/tips.md` Tip #01）
2. **`py.typed` + mypy strict** 要保持绿（参考 `docs/tips.md` Tip #02）；新函数都要写完整类型
3. **Notebook 叙事结构** Goal → Data → Analysis → Conclusion；每个 code cell 上方配 Markdown cell 说明「这个 cell 回答什么问题」
4. **交付前 Restart & Run All**，可复现性只认源码（参考 `docs/tips.md` Tip #03）
5. **5 张图每张都回答一个具体问题**；避免「here's a plot」式的 EDA 垃圾图

第一步请先帮我：

1. 列出 2–3 个名古屋市 open data portal 上合适的候选数据集（要求：≥ 2 个数值列、≥ 1 个分类或时间维度、license 允许学习使用），各说明为什么适合这周的练习；
2. 推荐的 `src/` 模块拆分（比如 `loaders.py` vs `cleaning.py` 的边界）；
3. 建议的 Tip #04 候选主题（从 pandas / matplotlib 里最容易踩坑的点挑 3 个给我选）。

在我确认数据集之前先不动代码。
