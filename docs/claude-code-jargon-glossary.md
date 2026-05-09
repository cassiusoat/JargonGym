# Claude Code 黑话词典（IT / 互联网术语对照）

> 通用速查手册。专门收录 Claude Code（Opus 4.7）回答中频繁出现，但**英文缩写不直观**或**比喻味重**的词。
>
> 每条提供：英文术语 → 常见中文译法 → 字面 / 来源 → 实际含义 → 典型用法 → 例句。

---

## 目录

- [一、测试与质量](#一测试与质量)
- [二、调试与排查](#二调试与排查)
- [三、工程实践（代码 / 架构）](#三工程实践代码--架构)
- [四、流程与项目管理](#四流程与项目管理)
- [五、性能与运维](#五性能与运维)
- [六、部署与上线](#六部署与上线)
- [七、论证 / 沟通比喻类](#七论证--沟通比喻类)
- [八、Claude Code / Git / AI 工具特有](#八claude-code--git--ai-工具特有)
- [九、聊天 / 协作高频缩写](#九聊天--协作高频缩写)
- [附：Opus 4.7 偏爱但易误解的比喻词](#附opus-47-偏爱但易误解的比喻词)

---

## 一、测试与质量

### smoke test —— 冒烟测试

- **字面**：硬件年代用语，电路接通后只检查"会不会冒烟"。
- **含义**：跑一组最浅的检查，确认整体能启动 / 主流程能走通。不深入测细节。
- **用法**：改完一处后先跑 smoke test → 没炸再跑全套 unit / integration test。
- **例**：`pytest -k smoke` / "我先跑个冒烟，确认 import 不报错"。

### regression test —— 回归测试

- **字面**：regression = "退化、回退"。
- **含义**：固定一组老用例，每次改完都重跑，**确认没把以前能用的功能弄坏**。
- **用法**：CI 流水线上每个 PR 自动触发的全量测试通常就是回归。
- **常见说法**："这次改动有没有引入回归（regression）？"

### TDD（Test-Driven Development）—— 测试驱动开发

- **三步循环**：
  1. **Red**：先写一个**会失败**的测试。
  2. **Green**：写最少的实现，让它变绿。
  3. **Refactor**：在不动测试的前提下整理代码。
- **用途**：用测试先把"我要做什么"钉死，避免实现跑偏。

### BDD（Behavior-Driven Development）—— 行为驱动开发

- TDD 的人话版本：测试用 `Given / When / Then` 描述用户行为，让产品 / QA 也读得懂。

### E2E（end-to-end）—— 端到端测试

- 模拟真实用户从 UI 一直点到数据库的全链路，最贵但最能反映真实情况。
- **对比**：unit（单函数）< integration（多模块）< E2E（整条链路）。

### unit / integration test —— 单元 / 集成测试

- **unit**：测一个函数 / 类，依赖全用假对象替代。
- **integration**：把多个真实模块拼起来测，可能连真数据库 / 真 HTTP。

### mock / stub / fake / spy / fixture —— 测试替身家族

| 词 | 中文 | 干啥的 |
|---|---|---|
| mock | 桩 / 模拟 | 假对象，可以**断言**它被怎么调用了 |
| stub | 存根 | 假对象，只负责返回预设值，不断言 |
| fake | 假实现 | 简化版真实现（如内存版数据库） |
| spy | 间谍 | 包真对象 + 偷偷记录调用 |
| fixture | 夹具 | 测试前后准备 / 清理用的固定数据或环境 |

### happy path / golden path —— 黄金路径 / 主流程

- 一切正常、用户按预期操作的那条路。
- **对比**：edge case（边界）/ corner case（角落 / 罕见组合）/ unhappy path（异常路径）。

### edge case / corner case —— 边界 / 角落用例

- **edge case**：单一维度极端值（空字符串、超长、负数、最大整数）。
- **corner case**：多个边界**同时**触发（空数组 + 离线 + 高并发）。

### flaky test —— 抖动测试

- 时好时坏的测试，**没改代码也会偶尔挂**，最招人恨。常见原因：时间依赖、网络、并发、随机数。
- 对策：定位 root cause，或暂时 `@pytest.mark.flaky` 标记。

### xfail / skip —— 预期失败 / 跳过

- `xfail`：标记"已知会挂"的测试，CI 不当 fail，但万一突然过了会提醒（unexpected pass）。
- `skip`：直接跳过不跑。

### snapshot test —— 快照测试

- 把首次输出存档成"快照"，下次跑只对比是否一致。前端组件 / 报表常用。
- 缺点：误改后要谨慎更新快照，否则掩盖 bug。

### sanity check —— 合理性 / 体检式检查

- 不严谨，只扫一眼"数量级 / 方向 / 类型"对不对。比如算完税额扫一眼是不是 0.x，不是 100x。

### dogfooding —— 吃自家狗粮

- 团队**自己先用自家产品**，发现痛点再改。

---

## 二、调试与排查

### root cause —— 根因

- 真正的源头，相对于 symptom（症状）和 proximate cause（直接原因）。
- **常见反模式**：只修症状（"返回 null 时直接 catch 掉"）而没修根因（"为什么会返回 null"）。

### repro（reproduction）—— 复现

- "能稳定再现 bug 的最小步骤"。"先给我一个 repro" = "先告诉我怎么稳定触发"。
- **MRE（Minimal Reproducible Example）**：最小可复现示例。

### bisect —— 二分定位

- `git bisect`：在一段提交区间里二分查找"哪个 commit 引入了 bug"。
- 引申用法：在大块代码里二分注释 / 二分配置。

### off-by-one —— 差一错位

- 经典 bug：循环 / 索引 / 页码差 1。
- **典型场景**：`for i in range(n)` 想要 `n+1` 次；分页接口第一页该是 0 还是 1；OCR 给出的页码总错 1 页。

### race condition —— 竞态

- 多线程 / 多进程下，"谁先到不确定"导致结果飘。
- **对比**：deadlock（死锁）/ livelock（活锁，互相让到死）/ starvation（饥饿，永远轮不到）。

### deadlock —— 死锁

- A 等 B 释放锁，B 等 A 释放锁，永远卡死。

### memory leak —— 内存泄漏

- 用完的内存没释放，越跑越胖直到 OOM（Out Of Memory，内存爆了）。
- **类比**：file descriptor leak（文件描述符泄漏）/ socket leak。

### heisenbug —— 海森堡 bug

- 致敬不确定性原理：**一加日志 / 调试器它就消失**。多半是时序、并发、优化器导致的。

### Mandelbug —— 曼德博 bug

- 来自 Mandelbrot（分形）：每次复现细节都不一样，分形般诡异。

### regression —— 回归（bug 语境）

- 以前能用的功能，因为新改动又坏了。

### ICE —— 内部编译器错误

- Internal Compiler Error，编译器自己挂了，不是你代码的锅（理论上）。

---

## 三、工程实践（代码 / 架构）

### refactor —— 重构

- **不改外部行为、只改内部结构**。改完测试都该照样过。
- **对比**：rewrite（重写）= 推倒重来。

### legacy code —— 遗留代码

- 老的、文档稀薄、没人想动但不能删的代码。常带技术债。

### boilerplate —— 样板代码

- 没营养但不写不行的模板代码（如 Java 的 getter/setter）。

### scaffolding —— 脚手架

- 先搭一个能跑的空架子，再逐步填血肉。
- 工具：`create-react-app` / `cookiecutter` / `vite create` 之类。

### tech debt —— 技术债

- 当初赶工偷懒留下的烂账，**迟早要还利息**（维护成本越拖越高）。

### DRY —— Don't Repeat Yourself（别重复自己）

- 同一段逻辑别复制粘贴。
- **反向忠告**：WET（Write Everything Twice）—— 在抽象未明前，宁可写两遍。

### KISS —— Keep It Simple, Stupid（保持简单）

- 别炫技，能用 if-else 解决就别上设计模式。

### YAGNI —— You Ain't Gonna Need It（不需要就别写）

- 别为"将来可能用到"加抽象层、配置项、扩展点。
- **Claude Code 系统提示反复强调这一条**。

### SOLID —— 面向对象五原则

- **S**ingle Responsibility（单一职责）/ **O**pen-Closed（开闭）/ **L**iskov Substitution（里氏替换）/ **I**nterface Segregation（接口隔离）/ **D**ependency Inversion（依赖倒置）。

### SoC（Separation of Concerns）—— 关注点分离

- 不同职责放在不同模块 / 文件 / 层。

### SSOT（Single Source of Truth）—— 单一可信源

- 一份数据**只有一个权威出处**，别处都从这里推导，避免不一致。

### idempotent —— 幂等

- 同一操作执行 1 次和 N 次结果相同。HTTP 的 `PUT` / `DELETE` 是幂等，`POST` 不是。
- 设计 API 时常被要求"重试要安全" → 接口必须幂等。

### atomic —— 原子操作

- "要么全做，要么全不做"，不会半截。数据库事务的 A。

### side effect —— 副作用

- 函数除了返回值还**动了外部状态**：写盘、改全局变量、发网络请求。
- **pure function（纯函数）** = 无副作用。

### short-circuit —— 短路

- `A && B`：A 为假就不算 B；`A || B`：A 为真就不算 B。
- 引申："提前 return / 跳出"也叫 short-circuit。

### shim —— 垫片

- 中间夹一层薄代码，把旧接口适配到新接口（或反过来）。
- **类似词**：adapter（适配器）/ polyfill（前端给老浏览器补特性）。

### facade —— 门面

- 在一堆复杂子系统前提供一个简单统一的入口。

### middleware —— 中间件

- 夹在请求和处理函数之间的"过滤层"，做鉴权、日志、限流等。

### pipeline / workflow —— 流水线 / 工作流

- 多步串联的处理过程：CI 流水线、数据 ETL、AI agent 链。

### backwards compatibility —— 向后兼容

- 新版本不破坏老用法 / 老数据。
- **对比**：breaking change（破坏性变更）= 升级后老代码会挂。

### hardcode —— 硬编码

- 把值直接写死在代码里，没做配置化。**反义**：configurable（可配置）。

### magic number / magic string —— 魔法值

- 代码里突然冒出的 `42` / `"OK"`，没有命名也没有注释，读者一脸懵。

### footgun —— 坑脚枪

- "字面意思：朝自己脚开枪的接口"。容易踩坑、用错的 API 设计。

### gotcha —— 坑点

- 反直觉的小陷阱，比 bug 轻。"Python 的可变默认参数是个 gotcha"。

### code smell —— 代码异味

- 不至于 bug，但闻着不对：方法过长、参数过多、God class。

### God object / God class —— 上帝对象

- 一个类啥都干，几千行，耦合所有模块。反模式。

### spaghetti code —— 意大利面代码

- 控制流像意面一样缠绕，goto 满天飞。反模式。

### lasagna code —— 千层面代码

- 抽象层堆得太厚，每层只透传，没增值。反模式。

---

## 四、流程与项目管理

### MVP —— Minimum Viable Product（最小可用版本）

- 能跑、能验证假设的最薄版本。"先做个 MVP 给用户试"。

### POC —— Proof of Concept（概念验证）

- 证明"这条路走得通"的小原型，**不追求生产可用**。

### spike —— 探索性任务

- 限时调研性原型，用来回答"这个方案行不行"。做完通常就丢。

### iteration / sprint —— 迭代 / 冲刺

- iteration = 一个时间盒（通常 1-2 周）的开发周期。
- sprint = Scrum 框架里的固定迭代。

### backlog —— 待办池

- 还没排期的需求 / bug 堆。`product backlog`（产品待办）/ `sprint backlog`（本迭代要做的）。

### WIP —— Work In Progress

- 进行中。也指 PR 的 `[WIP]` 前缀（"还没改完，先别合"）。

### ETA / ETC —— 预计完成 / 剩余时间

- Estimated Time of Arrival / to Completion。

### TBD / TBA / TBC —— 待定 / 待公布 / 待确认

- To Be Determined / Announced / Confirmed。

### triage —— 分诊 / 分类

- **医院术语**：急诊把病人按严重度排队。
- 软件语境：把 bug / issue 按 severity × priority 分桶。

### punch list —— 收尾清单

- **来自建筑业**：竣工前剩下的小修小补清单。
- 软件：上线前最后那张"还差什么"清单。

### scope creep —— 范围蔓延

- 需求边做边膨胀，越改越大。常见提案："顺便把那个也改了吧"。

### post-mortem —— 事后复盘

- **字面**：尸检。
- 含义：故障 / 项目结束后，分析根因 + 教训 + 改进点的文档，**不追责**。

### retro（retrospective）—— 回顾会

- 团队定期复盘"这段时间什么做得好 / 不好 / 下次改什么"。

### stakeholder —— 利益相关方

- 被这事影响 / 关心结果的人：用户、PM、老板、合规、法务。

### alignment —— 对齐

- 让相关方在目标 / 方案上达成共识。"先和老板对齐一下方向"。

### onboarding / offboarding —— 入职 / 离职（流程）

- 引申：新员工接入项目 / 老员工交接离开。

### handover —— 交接

- 把工作 / 知识 / 权限转给下一个人。

### KPI / OKR —— 关键绩效指标 / 目标与关键结果

- KPI：考核用的硬指标（如月活、收入）。
- OKR：Objective（方向） + Key Results（如何衡量进展）。

### bandwidth —— 带宽（人的）

- "我这周没 bandwidth" = "我这周没精力 / 没空"。

### bus factor —— 公交车系数

- "团队里几个人被公交车撞了项目就完蛋"。bus factor=1 = 全靠一个人。

---

## 五、性能与运维

### bottleneck —— 瓶颈

- 整条链路最慢、决定整体上限的那一环。

### throughput / latency —— 吞吐 / 延迟

- throughput：单位时间能处理多少（QPS、TPS）。
- latency：单次请求从发出到收到的耗时。
- **关系**：高 throughput 不代表低 latency；可能批量大但单次慢。

### p50 / p95 / p99 —— 分位延迟

- 把所有请求耗时排序，第 50% / 95% / 99% 那一条的耗时。**长尾通常看 p95 / p99**。

### N+1 query —— N+1 查询问题

- 列出 N 条记录用 1 次查询，但每条又额外查 1 次 → 一共 N+1 次查询。ORM 常见坑。
- 解法：JOIN / `select_related` / 批量预取。

### cache hit / miss —— 缓存命中 / 未命中

- hit：命中缓存直接返回。
- miss：没命中，要回源。
- **hit rate / hit ratio**：命中率。

### TTL —— Time To Live（生存时间）

- 缓存条目 / token / DNS 记录的过期秒数。

### cold start / warm-up —— 冷启动 / 预热

- cold start：第一次跑、缓存为空、JIT 没编译，特别慢。
- warm-up：先跑几次让缓存 / JIT 热起来再开始测。

### backfill —— 回填

- 给历史数据补字段 / 补任务。新加列后跑脚本把老行填上。

### dry run —— 演练 / 空跑

- **只打印 / 模拟，不真执行**。验证脚本逻辑、避免误操作生产数据。

### graceful shutdown —— 优雅停机

- 收到 SIGTERM 后停止接新请求、等老请求做完、再退出，不直接 kill。

### graceful degradation —— 优雅降级

- 部分功能挂了，整体仍能用（缩水版）。**对比** fail-fast（直接挂）。

### circuit breaker —— 熔断器

- 下游服务挂了，**主动停止调用**一段时间，避免雪崩。

### debounce / throttle —— 防抖 / 节流

- debounce：连续触发只在最后一次后 N 毫秒执行（搜索框联想）。
- throttle：固定频率执行（滚动事件每 100ms 才响应一次）。

### eventual consistency —— 最终一致

- 分布式系统，写完后短期内各节点不一致，但**最终会收敛**。对比 strong consistency。

### CAP / BASE / ACID —— 数据库 / 分布式三套缩写

- ACID：原子 / 一致 / 隔离 / 持久（关系库事务保证）。
- CAP：Consistency / Availability / Partition tolerance（分布式三选二）。
- BASE：Basically Available / Soft state / Eventual consistency（NoSQL 风格）。

---

## 六、部署与上线

### rollout —— 上线 / 推流

- 把新版本推到生产。常分 staged rollout（分批）/ full rollout（全量）。

### rollback —— 回滚

- 撤回到旧版本。生产事故第一反应。

### hotfix —— 热修复

- 紧急上线的小补丁，绕过常规发布流程。

### canary release —— 金丝雀发布

- **来源**：矿工带金丝雀下井，鸟先死预警瓦斯。
- 含义：先放给 1% 用户，观察一段时间没事再放量。

### blue-green deployment —— 蓝绿部署

- 同时维护蓝、绿两套环境，新版本先在绿环境跑稳，**切流量过去**；蓝环境保留作回滚兜底。

### feature flag / feature toggle —— 特性开关

- 代码已部署但靠开关控制是否启用。可以做 A/B、灰度、紧急关闭。
- 常见库：LaunchDarkly / GrowthBook / Unleash。

### A/B test —— A/B 实验

- 用户随机分两组，对比哪个版本指标更好。

### shadow traffic / dark launch —— 影子流量 / 暗发布

- 把生产流量**复制**一份打到新系统，**结果丢弃**，只用来压测 / 对比。

### migration —— 迁移

- **schema migration**：数据库表结构变更（新增列、改类型）。
- **data migration**：把数据搬到新格式 / 新系统。

### SLA / SLO / SLI —— 服务等级 协议 / 目标 / 指标

- SLI：实际测量值（"实际可用率 99.95%"）。
- SLO：内部目标（"目标 99.9%"）。
- SLA：对外承诺 + 违约赔偿（"承诺 99.5%，达不到退钱"）。

### error budget —— 错误预算

- SLO 99.9% → 一个月最多挂 43 分钟，这 43 分钟就是预算。烧完就冻结发布、专心修稳定性。

### incident —— 故障事件

- 生产出问题。按等级分 SEV1（最严重）/ SEV2 / SEV3。
- 流程：detect → mitigate → fix → post-mortem。

---

## 七、论证 / 沟通比喻类

> **这一节是 Opus 4.7 在分析 / 写文案场景特别爱用的词。**

### fallback —— 退路 / 备用方案

- 第一招不灵时的第二招。
- **例**："如果远程 API 挂了，fallback 到本地缓存"；"主论据被驳回时的 fallback 论点是什么"。

### GO / NO-GO —— 上 / 不上 二元决策

- 来自航天发射前的检查表。每项要么 GO 要么 NO-GO，全 GO 才发射。

### de minimis —— 微不足道（拉丁语）

- 全称 *de minimis non curat lex*："法律不理会琐碎小事"。
- 用于法律 / 合规 / 风险评估："这个量级太小，可忽略"。

### circular reasoning —— 循环论证

- 拿被怀疑的东西自证清白。"A 因为 B，B 因为 A"。

### straw man —— 稻草人

- 故意扭曲对方观点变成更容易反驳的版本，再去打。

### steel man —— 钢人

- 反过来：用**最强版本**表述对方观点，再来反驳。诚实辩论的姿态。

### caveat —— 限定 / 警告

- "这话有前提，别外推"。`caveat emptor` = 买家自负。

### rationale —— 理据

- "为什么这么做"的理由 / 推理过程。PR 描述里 reviewer 最想看的部分。

### ground truth —— 真值 / 基准

- 拿来对比的"客观标准答案"。机器学习里特别常用。

### north star —— 北极星指标

- 最该长期盯的那一个核心指标，所有其他指标围着它转。

### Tier 1 / Tier 2 / Tier 3 —— 分级

- 按精度 / 优先级 / 重要性分层。Tier 1 = 最核心 / 最粗算 / 最高优。**语境决定方向**：
  - 精度语境：Tier 1 粗算（默认值） → Tier 2 细算（实测 / 校准值）。
  - 客户分级：Tier 1 = 最大客户。
  - 故障分级：Tier 1 = 一线支持。
- **建议**：Opus 4.7 第一次出现时务必显式说明哪个方向。

### apples to oranges —— 苹果对橘子（不可比）

- "这俩根本不是一类东西，没法直接比"。

### low-hanging fruit —— 低垂果实

- 最容易摘的、性价比最高的活，先做这个。

### moving target —— 移动靶

- 需求 / 标准 / 接口在不停变，让人很难命中。

### chicken-and-egg —— 鸡生蛋蛋生鸡

- 互为前置依赖，谁都没法先启动。

### bikeshedding —— 自行车棚效应

- **来源**：核电站审批会议上没人质疑反应堆设计，却为自行车棚的颜色争论一小时。
- 含义：**大事拍板秒过，小事（命名 / 颜色）讨论一整天**。

### yak shaving —— 剃牦牛

- 为了做 A 不得不先做 B、再做 C…无限套娃。"我只是想合并一个 PR，结果先在剃牦牛"。

---

## 八、Claude Code / Git / AI 工具特有

### prompt —— 提示词

- 给模型的输入。`system prompt`（系统提示）/ `user prompt`（用户输入）。

### token —— 词元

- 模型计费 / 长度限制单位，约等于半个英文单词或 1-2 个中文字。

### context window —— 上下文窗口

- 模型一次能看的最大 token 数。Opus 4.7 提供 1M 版本。**超出会被压缩 / 丢早期内容**。

### prompt cache / cache hit —— 提示缓存命中

- 同一段 prompt 5 分钟内重复发，**直接读缓存**，便宜且快。

### prompt injection —— 提示注入

- 攻击手法：在工具返回 / 用户输入里塞"忽略前面所有指令"，劫持模型。

### subagent —— 子代理

- Claude 派出去做子任务的 Agent，独立上下文。Explore / general-purpose 等。

### skill —— 技能

- Claude Code 的可复用工作流模板，存放于 `.claude/skills/`。

### hook —— 钩子

- 事件触发的回调脚本。如 `SessionStart`、`UserPromptSubmit`。

### worktree —— 工作树

- `git worktree`：同一仓库的多个目录并行检出不同分支。Claude Code 的 isolated agent 会用 worktree 起隔离副本。

### diff / delta —— 差异 / 增量

- 两版之间的变化。`git diff` 是结构化版本。

### staged / unstaged —— 已暂存 / 未暂存

- staged = `git add` 过、待 commit 的；unstaged = 改了但还没 add 的。

### stash —— 暂存草稿

- `git stash`：临时塞一边的未提交改动，切分支用。`git stash pop` 恢复。

### rebase / merge —— 变基 / 合并

- merge：保留两边历史，新增一个 merge commit。
- rebase：把你的 commits **挪到对方 HEAD 上重新接**，历史更线性。

### squash —— 压缩 commits

- 把多个零碎 commits 合成一个，再合主干。

### cherry-pick —— 摘樱桃

- 单挑某个 commit 应用到当前分支。

### fast-forward —— 快进合并

- 目标分支没新提交，**直接把指针向前移**，不产生 merge commit。

### force push —— 强推

- `git push --force`：覆盖远程历史。**危险**，可能抹掉别人推上去的提交。`--force-with-lease` 是安全版。

### blame / annotate —— 追责 / 标注

- `git blame`：显示每行最后被谁改的、哪个 commit。

### LGTM —— Looks Good To Me

- code review 通过。"我看了，可以合"。

### nit / nitpick —— 鸡蛋挑骨头

- 评审时的"小毛病无伤大雅"。"nit: 这变量名打错了"，作者可改可不改。

### CR —— Code Review

- 代码评审。

### MR / PR —— Merge / Pull Request

- 合并请求。GitLab 叫 MR，GitHub / Bitbucket 叫 PR。

### in-flight —— 进行中（请求）

- 已发出但还没收到响应的调用。

### in-place —— 原地（修改）

- 不复制、直接改原对象 / 原文件。`list.sort()` 是 in-place，`sorted(list)` 不是。

### guardrail —— 护栏

- 兜底校验 / 边界保护，防止离谱输入 / 操作。

### sentinel —— 哨兵值

- 特殊标记值，表示"无 / 结束 / 未设置"。如 `-1`、`None`、`UNSET`。

### nuke —— 核平

- 全删（"`rm -rf` 整个目录"那种语气）。

### hermetic —— 密闭的

- 测试 / 构建**完全隔离**外部依赖（网络、时间、随机），保证可复现。

### deterministic / non-deterministic —— 确定性 / 非确定性

- 同输入是否同输出。LLM 默认 non-deterministic，靠 temperature=0 + seed 才接近 deterministic。

---

## 九、聊天 / 协作高频缩写

| 缩写 | 全称 | 中文 |
|---|---|---|
| ASAP | As Soon As Possible | 尽快 |
| FYI | For Your Information | 供参考 |
| FYA | For Your Awareness | 知会一下 |
| IMO / IMHO | In My (Humble) Opinion | 我（个人）认为 |
| AFAIK | As Far As I Know | 据我所知 |
| AFAICT | As Far As I Can Tell | 据我看 |
| TL;DR | Too Long; Didn't Read | 太长不看 / 摘要 |
| N/A | Not Applicable | 不适用 |
| TBD / TBA / TBC | To Be Determined / Announced / Confirmed | 待定 / 公布 / 确认 |
| WIP | Work In Progress | 进行中 |
| ETA | Estimated Time of Arrival | 预计完成时间 |
| OOO | Out Of Office | 不在工位 |
| EOD / EOW | End Of Day / Week | 今日 / 本周末前 |
| RFC | Request For Comments | 征求意见稿 |
| NIT | Nitpick | 小毛病 |
| OOTB | Out Of The Box | 开箱即用 |
| YMMV | Your Mileage May Vary | 因人而异 |
| IIRC | If I Recall Correctly | 没记错的话 |
| IIUC | If I Understand Correctly | 我理解没错的话 |
| WRT | With Respect To | 关于 |
| AKA | Also Known As | 别名 |
| TIL | Today I Learned | 今天才知道 |
| RTFM | Read The Fucking Manual | 自己看文档 |
| PEBKAC | Problem Exists Between Keyboard And Chair | 是用户的问题 |
| LGTM | Looks Good To Me | 我看可以 |
| SGTM | Sounds Good To Me | 听上去不错 |
| PTAL | Please Take A Look | 麻烦看一下 |
| OTOH | On The Other Hand | 另一方面 |
| FWIW | For What It's Worth | 仅供参考（弱势一点） |

---

## 附：Opus 4.7 偏爱但易误解的比喻词

Opus 4.7 行文偏文学化，下面这些**比喻味重**的词如果初次出现没解释，容易让人懵。建议在项目级提示文件（`CLAUDE.md` / `AGENTS.md`）里明确"避免使用 / 第一次出现必须括注"。

| 词 | 字面 | 实际想表达的 |
|---|---|---|
| **弹药 / ammo** | 子弹 | 论据、备选方案、可用资源 |
| **骨架 / skeleton** | 骨头架子 | 代码 / 文档的最小框架结构（同 scaffolding） |
| **锚定 / anchor** | 抛锚 | 把某个值 / 选项设为基准参考点 |
| **抓手 / handle / hook** | 把手 | 切入点、入口、可操作点 |
| **打通 / wire up** | 接线 | 把模块 / 端到端连起来跑通 |
| **闭环 / closed loop** | 回路闭合 | 流程从开始到结束、反馈回到起点 |
| **对齐 / alignment** | 对齐 | 达成共识 / 让格式 / 数据一致 |
| **拉齐 / level set** | 校平 | 让各方信息同步到同一水平线 |
| **赋能 / empower** | 授予能力 | 提供工具 / 数据让对方能做某事 |
| **沉淀 / precipitate** | 沉淀 | 把经验 / 知识固化成文档 / 规范 |
| **抽象 / abstract** | 抽象 | 把共性提取出来做通用层 |
| **解耦 / decouple** | 解耦 | 减少模块间依赖，各自独立 |
| **下沉 / sink** | 下沉 | 把功能 / 逻辑放到更底层的公共层 |
| **打平 / flatten** | 拍平 | 消除层级，变成扁平结构 |
| **黑盒 / 白盒** | — | 不看 / 看内部实现的测试视角 |
| **吃下 / swallow** | 吞 | 接住并消化（异常 / 任务 / 流量） |
| **冒泡 / bubble up** | 冒泡 | 异常 / 事件向上层传递 |
| **打点 / instrument** | 安埋点 | 在代码里加监控 / 日志记录 |
| **兜底 / fallback** | 兜底 | 主路径失败时的保底逻辑 |
| **脏写 / dirty write** | — | 未经校验直接写入 |
| **刷数 / backfill** | — | 跑脚本批量补 / 改老数据 |
| **打掉 / drop / remove** | — | 删除该功能 / 字段 |
| **下线 / deprecate** | — | 停用、不再维护 |
| **提优先级 / bump priority** | 撞 | 把任务从低优提到高优 |
| **拉群** | — | 建讨论组（中文互联网） |
| **拉通 / sync up** | — | 跨团队同步信息 |

---

## 维护说明

- 新增词条按上面 9 个分类放入，**第十节"附"专放比喻词**。
- 每条尽量给"字面 → 含义 → 用法 → 例"四要素，便于查阅。
- 如果想让 Claude 说"人话"，可以在项目级提示文件（`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` 等）加一段：

  > **沟通风格**：避免使用"弹药 / 骨架 / 锚定 / 沉淀"等比喻；首次出现的英文术语必须在中文括注里标出全称（如 `MVP（最小可用版本）`）。
