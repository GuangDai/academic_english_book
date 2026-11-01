# 学术英语段落构建、逻辑论证、深度修改与全篇写作实战题库（Package 2）

本工程包是 **116 天全量词汇与句法基础包（`academic_english_training.zip`）** 的高阶篇章级进阶伴侣包，专为**“已经认识词汇和基础句型，但要真正动手写整段话、写 AI/时间序列/生成模型/具身智能小论文、写六级/雅思/托福大小作文、准备学术演讲（Tech Talk）与审稿回复（Rebuttal）”**而设计。

## 一、核心解决的四大实战问题
1. **“我这一段到底要表达什么 → 那么每一句该怎么写？”**
   - 内置 **`blueprints/intent_to_paragraph_handbook.md`（48 个核心段落构建蓝图 `BP01–BP48`）**，覆盖顶会论文全章节（Abstract / Intro / Related Work / Method / Experiments / Ablation / Limitations）、雅思图表小作文与托福综合写作、六级/雅思/托福大作文、学术演讲与顶会 Rebuttal。
   - 每个蓝图精准定义 **第 1 句到第 5 句的功能角色**、**句子成分骨架**、**病段反例** 与 **零 AI 味母语级标杆段**。
2. **“句子之间怎么表达逻辑、怎么自然衔接、怎么严密论证？”**
   - 内置 **`blueprints/logic_and_argumentation_handbook.md`（30 条篇章逻辑与论证引擎 `L001–L030`）**。
   - 彻底告别机械贴 *First, Second, Moreover*，系统训练 **旧信息→新信息链（Given-to-New）**、**主位推进模式**、**`This/Such + 概念浓缩指代词`**、**Toulmin 五步微论证**、**先让步后釜底抽薪式反驳** 以及 **反事实推演**。
3. **“写出来的草稿怎么修改？怎么彻底拔除五大语病与 AI 痕迹？”**
   - 内置 **`blueprints/revision_clinic_handbook.md`（60 例病段深度诊断与重构图谱 `RC01–RC60`）**。
   - 每例均针对 **头重脚轻长主语、散装短句、口语化、名词化僵尸句、不精确（缺基线/指标）、空洞夸张无实例、重度 AI 套话** 执行七维诊断与四步修改手术。
4. **“怎么把段落串成整篇小论文、整篇大小作文和完整演讲稿？”**
   - 内置 **`full_text_anthology/`（24 篇完整带逐段意图与蓝图链拆解的全文样板 `FT01–FT24`）** 与 **60 天实战训练课程（`days/day_0001`–`day_0060`，共 720 道深度大题 + 完整解析与自检量表）**。

## 二、目录结构一览
- `blueprints/intent_to_paragraph_handbook.md` & `.json`：48 个“表达意图 → 逐句写法”核心段落蓝图（`BP01–BP48`）
- `blueprints/logic_and_argumentation_handbook.md` & `.json`：30 条篇章逻辑衔接、信息流推进与论证法则（`L001–L030`）
- `blueprints/revision_clinic_handbook.md` & `.json`：60 组“病段 vs. 诊断批注 vs. 四步手术 vs. 母语定稿”对照库（`RC01–RC60`）
- `full_text_anthology/ANTHOLOGY_COMPLETE_HANDBOOK.md` & `FT01–FT24.json`：24 篇完整小论文、演讲稿、Rebuttal、SoP、六级/雅思/托福满分范文及段落拆解
- `curriculum_60days.json`：60 天四阶段进阶课程全局规划
- `days/day_0001` 至 `days/day_0060`：每日包含 `lesson.json`、`tasks.json` 与可直接阅读打印的 `tasks.md`（每天 12 道深度任务）
- `answer_keys/day_0001.json` 至 `day_0060.json`：720 道任务的完整母语级参考段落、跨文体改写版本、逐句成分与信息流剖析及七维自检评分表
- `schemas/`：全部数据文件的 JSON Schema 校验规范