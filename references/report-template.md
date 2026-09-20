# 研报模板（HTML）

研报交付形态为单文件 HTML。本文件给出页面骨架、各章节的写作要求与图表配置。方括号内为写作提示，成稿时替换为实际内容。可视化细节见 `visual-guide.md`，来源标注见 `source-policy.md`。

## 输出格式硬规则

**HTML 正文中不得出现 Markdown 语法。** 加粗写 `<strong>`，斜体写 `<em>`，列表写 `<ul>` 或 `<ol>`，表格写 `<table>`。若写成 `**加粗**`，浏览器会原样显示星号，读者一望即知是程序生成且未做清理。

成稿前须全文检索两个符号：`**` 与行首的 `#`。出现即须转为 HTML 标签。这类缺陷不会报错，只会直接印在页面上，是交付前的必检项。

**表格与标题一律用 HTML 标签。** 不使用 Markdown 的管道符表格与井号标题。Markdown 语法只在起草阶段使用。

**章节编号不用序数词。** 小标题直接写名称，不写"一、""二、"。正文内需要分点时用"第一，……第二，……"，这不算小标题。

## 页面骨架

直接以此骨架为起点，替换方括号内容并增删图表。样式与脚本全部内联，不引用外部资源。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[公司名称]（[股票代码]）运营模式与风险研判</title>
<style>
  /* ===== 设计系统：现代研报风格（浅色底，适配打印与长文阅读） ===== */
  :root{
    --primary:#1a1f36;--primary-light:#2d3250;
    --accent:#6366f1;--accent-light:#818cf8;--accent-glow:rgba(99,102,241,0.12);
    --up:#ef4444;--up-bg:rgba(239,68,68,0.08);   /* 涨 红 */
    --down:#22c55e;--down-bg:rgba(34,197,94,0.08); /* 跌 绿 */
    --neutral:#64748b;
    --ink:#0f172a;--ink-2:#334155;--ink-3:#64748b;--ink-4:#94a3b8;
    --border:#e2e8f0;--border-light:#f1f5f9;
    --surface:#ffffff;--bg:#f8fafc;
    --radius-sm:6px;--radius:12px;--radius-lg:16px;
    --shadow-sm:0 1px 2px rgba(0,0,0,0.04);
    --shadow:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:0 4px 6px -1px rgba(0,0,0,0.07),0 2px 4px -2px rgba(0,0,0,0.05);
    --space-xs:4px;--space-sm:8px;--space-md:16px;--space-lg:24px;
    --space-xl:40px;--space-2xl:64px;
    --transition:0.2s cubic-bezier(0.4,0,0.2,1);
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",
      "PingFang SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif;
    font-size:15px;line-height:1.8;
    -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
    text-rendering:optimizeLegibility;}
  .wrap{max-width:960px;margin:0 auto;padding:0 var(--space-lg) var(--space-2xl);background:var(--surface);}
  nav.toc{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.85);
    backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
    border-bottom:1px solid var(--border);padding:0 var(--space-lg);
    max-width:960px;margin:0 auto;overflow-x:auto;white-space:nowrap;scrollbar-width:none;}
  nav.toc::-webkit-scrollbar{display:none;}
  nav.toc a{display:inline-block;padding:14px 12px;color:var(--ink-3);text-decoration:none;
    font-size:13px;font-weight:500;letter-spacing:.01em;
    border-bottom:2px solid transparent;transition:color var(--transition),border-color var(--transition);}
  nav.toc a:hover{color:var(--ink);border-bottom-color:var(--accent);}
  header.rpt{padding:var(--space-2xl) 0 var(--space-xl);border-bottom:none;position:relative;}
  header.rpt::after{content:"";position:absolute;bottom:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,var(--accent),transparent 60%);}
  header.rpt h1{font-size:32px;font-weight:700;letter-spacing:-.02em;line-height:1.3;
    color:var(--ink);margin-bottom:var(--space-md);}
  .meta{display:flex;flex-wrap:wrap;gap:var(--space-sm) var(--space-lg);font-size:13px;color:var(--ink-3);}
  .meta span{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;
    background:var(--bg);border-radius:100px;font-weight:500;}
  h2{font-size:22px;font-weight:700;letter-spacing:-.01em;margin:var(--space-2xl) 0 var(--space-lg);
    padding-left:16px;border-left:4px solid var(--accent);line-height:1.4;}
  h3{font-size:16px;font-weight:600;color:var(--ink-2);margin:var(--space-xl) 0 var(--space-md);letter-spacing:-.005em;}
  p{margin:var(--space-md) 0;color:var(--ink-2);}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
    gap:var(--space-md);margin:var(--space-lg) 0;}
  .card{position:relative;background:var(--surface);border:1px solid var(--border);
    border-radius:var(--radius);padding:var(--space-lg);overflow:hidden;
    transition:box-shadow var(--transition),transform var(--transition);}
  .card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;}
  .card:hover{box-shadow:var(--shadow-md);transform:translateY(-1px);}
  .card.struct::before{background:linear-gradient(90deg,var(--down),var(--down-bg));}
  .card.trans::before{background:linear-gradient(90deg,var(--accent),var(--accent-light));}
  .card.stage::before{background:linear-gradient(90deg,var(--up),#f97316);}
  .card h4{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;
    color:var(--ink-3);margin-bottom:var(--space-sm);}
  .card p{font-size:15px;color:var(--ink);line-height:1.7;margin:0;}
  figure{margin:var(--space-xl) 0;padding:var(--space-lg);background:var(--surface);
    border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow-sm);
    transition:box-shadow var(--transition);}
  figure:hover{box-shadow:var(--shadow);}
  figure .fig-body{width:100%;overflow-x:auto;}
  figure svg{display:block;}
  figcaption{margin-top:var(--space-md);padding-top:var(--space-md);
    border-top:1px solid var(--border-light);font-size:13px;line-height:1.7;}
  figcaption .fig-title{display:block;font-weight:600;color:var(--ink);margin-bottom:var(--space-xs);font-size:14px;}
  figcaption .fig-src{display:block;color:var(--ink-4);}
  figcaption .fig-note{display:block;margin-top:var(--space-sm);color:var(--ink-3);
    padding-left:var(--space-md);border-left:2px solid var(--accent-glow);}
  table{width:100%;border-collapse:separate;border-spacing:0;margin:var(--space-lg) 0;
    font-size:14px;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;}
  thead th{background:var(--bg);font-weight:600;font-size:12px;text-transform:uppercase;
    letter-spacing:.05em;color:var(--ink-3);padding:12px 16px;text-align:left;
    border-bottom:1px solid var(--border);}
  td{padding:12px 16px;border-bottom:1px solid var(--border-light);color:var(--ink-2);vertical-align:top;}
  tbody tr:last-child td{border-bottom:none;}
  tbody tr{transition:background var(--transition);}
  tbody tr:hover{background:var(--bg);}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;font-feature-settings:"tnum";}
  .up{color:var(--up);font-weight:600;}
  .down{color:var(--down);font-weight:600;}
  .neutral{color:var(--neutral);}
  ol,ul{padding-left:24px;margin:var(--space-md) 0;}
  li{margin:var(--space-sm) 0;color:var(--ink-2);line-height:1.75;}
  li::marker{color:var(--ink-4);}
  .bracket{color:var(--ink-2);font-size:13px;}
  .src-note{font-size:12px;color:var(--ink-4);margin-top:var(--space-sm);font-style:italic;}
  footer.rpt{margin-top:var(--space-2xl);padding-top:var(--space-lg);
    border-top:1px solid var(--border);font-size:12px;color:var(--ink-4);line-height:1.8;}
  /* 结论卡展开依据 */
  .card details{margin-top:var(--space-md);border-top:1px solid var(--border-light);padding-top:var(--space-md);}
  .card details summary{cursor:pointer;font-size:13px;font-weight:500;color:var(--accent);
    list-style:none;transition:color var(--transition);}
  .card details summary::-webkit-details-marker{display:none;}
  .card details summary::before{content:"▸ ";font-size:11px;}
  .card details[open] summary::before{content:"▾ ";}
  .card details summary:hover{color:var(--accent-light);}
  .card details .basis{font-size:13px;color:var(--ink-3);margin-top:var(--space-sm);
    line-height:1.75;padding-left:var(--space-md);border-left:2px solid var(--border);}
  /* 数据来源表筛选 */
  .filters{display:flex;gap:var(--space-sm);flex-wrap:wrap;align-items:center;margin-bottom:var(--space-md);}
  .filters span{font-size:13px;color:var(--ink-3);font-weight:500;}
  .filters button{font:inherit;font-size:12px;font-weight:500;padding:6px 16px;
    border:1px solid var(--border);background:var(--surface);color:var(--ink-3);
    border-radius:100px;cursor:pointer;transition:all var(--transition);letter-spacing:.01em;}
  .filters button:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-glow);}
  .filters button[aria-pressed="true"]{background:var(--primary);color:#fff;border-color:var(--primary);}
  tr.hide{display:none;}
  @media (max-width:768px){
    body{font-size:14px;line-height:1.75;}
    .wrap{padding:0 var(--space-md) var(--space-xl);}
    nav.toc{padding:0 var(--space-md);}
    nav.toc a{padding:12px 10px;font-size:12px;}
    header.rpt{padding:var(--space-xl) 0 var(--space-lg);}
    header.rpt h1{font-size:24px;}
    h2{font-size:19px;margin:var(--space-xl) 0 var(--space-md);}
    .cards{grid-template-columns:1fr;gap:var(--space-md);}
    figure{padding:var(--space-md);}
    table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius-sm);}
    th,td{padding:10px 12px;font-size:13px;}
    .meta{flex-direction:column;gap:var(--space-sm);}
  }
  @page{margin:18mm 16mm;}
  @media print{
    body{background:#fff;font-size:12pt;line-height:1.6;}
    .wrap{max-width:100%;padding:0;}
    nav.toc{display:none;}
    .card{box-shadow:none;border:1px solid #ddd;break-inside:avoid;}
    .card:hover{transform:none;box-shadow:none;}
    figure{break-inside:avoid;page-break-inside:avoid;box-shadow:none;}
    h2{break-after:avoid;}
    .filters{display:none;}
    tr.hide{display:table-row;}
    tbody tr:hover{background:transparent;}
  }
</style>
</head>
<body>

<nav class="toc">
  <a href="#summary">核心结论</a>
  <a href="#industry">行业环境</a>
  <a href="#profile">公司概况</a>
  <a href="#revenue">收入结构</a>
  <a href="#risk">风险来源</a>
  <a href="#switch">可转换性</a>
  <a href="#robust">抗风险能力</a>
  <a href="#transform">转型可行性</a>
  <a href="#counter">另一面</a>
  <a href="#caution">风险提示</a>
  <a href="#conclusion">结论</a>
  <!-- 可选：未纳入估值参照时，本行与正文中的估值参照节一并删除 -->
  <a href="#valuation">估值参照</a>
  <a href="#advice">投资建议</a>
  <!-- 可选：未纳入外部观点辑录时，本行与正文中的该节一并删除 -->
  <a href="#digest">外部观点辑录</a>
  <a href="#sources">数据来源</a>
</nav>

<div class="wrap">

<header class="rpt">
  <h1>[公司名称]（[股票代码]）运营模式与风险研判</h1>
  <div class="meta">
    <span>报告日期：[YYYY-MM-DD]</span>
    <span>数据截止：[最新报告期]</span>
    <span>分析框架：三步追问法</span>
  </div>
</header>

<h2 id="summary">核心结论</h2>
<div class="cards">
  <div class="card [struct|trans|stage]">
    <h4>[该层面的判断，如"收入层面"]</h4>
    <p>[一句判断]</p>
    <details>
      <summary>看依据</summary>
      <div class="basis">[支撑该判断的数据项与来源，逐条列出。格式：指标：数值（来源层级·文件名称，报告期）]</div>
    </details>
  </div>
  <div class="card [struct|trans|stage]">
    <h4>[另一层面，如"利润层面"]</h4>
    <p>[一句判断]</p>
    <details>
      <summary>看依据</summary>
      <div class="basis">[同上]</div>
    </details>
  </div>
</div>
<p>[在三到五句内说清：模式定位、风险位置、可转换性判断、判断失效的条件。]</p>

<h2 id="industry">行业环境</h2>
<p>[必选章节，置于公司概况之前。战略分析的标准顺序是行业、公司、判断。跳过行业直接分析公司，会使后文所有"属行业性还是个体性"的判断失去依据，也让公司的利润率水平无法解释。]</p>

<h3>市场容量与生命周期</h3>
<p>[行业市场规模与增速，是否接近饱和，处于导入、成长、成熟还是衰退阶段。该判断决定替代路径的时间窗口是否成立：行业若已进入成熟或衰退期，则转型方向本身即值得怀疑，与路径快慢无关。]</p>

<h3>行业盈利水平与竞争结构</h3>
<p>[行业平均毛利率与净利率的区间及近年走势；集中度指标（如 CR5）；进入与退出壁垒的高低。本节解释公司自身利润率水平的行业成因。缺少本节，公司的高利润率或低利润率只能作为参数使用，无法说明其来源。]</p>

<h3>成本与技术特征</h3>
<p>[主要原材料的价格机制与供应格局；技术变量，如自动化程度与产品迭代速度；产品同质化程度。]</p>

<h3>规模经济与范围经济</h3>
<p>[规模经济体现在单位成本曲线的哪一段；范围经济体现在何处，如同一产线生产多品类、同一客户群销售多产品；行业产能利用率。]</p>

<h3>纵向整合与客户结构</h3>
<p>[行业内是否存在向上游或下游延伸的趋势；下游客户的集中度与议价能力。]</p>

[本节允许部分维度缺少数据。缺数据的维度须在"分析覆盖范围"中如实声明，不得沉默跳过。沉默跳过会让读者误以为分析已经完整，这比明确写出"未覆盖"更危险。]

[本节建议配一张图，呈现行业规模、集中度或行业利润率走势。]

<h2 id="profile">公司概况</h2>
<p>[一页以内说清它是谁。不写历史沿革，只写理解业务必需的信息。]</p>
<table>
  <thead><tr><th>业务板块</th><th class="num">收入</th><th class="num">占比</th><th class="num">同比</th><th class="num">毛利率</th></tr></thead>
  <tbody>
    <tr><td></td><td class="num"></td><td class="num"></td><td class="num"></td><td class="num"></td></tr>
    <tr><td><strong>合计</strong></td><td class="num"></td><td class="num">100%</td><td class="num"></td><td class="num"></td></tr>
  </tbody>
</table>

<h2 id="revenue">收入结构：它靠什么挣钱</h2>
<p>[第一步。落到具体收入构成，识别底盘。说明各类收入的现金流特征与可预测性。]</p>

<figure>
  <div class="fig-body">[图一：收入构成环形图或堆叠条形图]</div>
  <figcaption>
    <span class="fig-title">图 1　[收入构成与占比：各业务板块]</span>
    <span class="fig-src">数据来源：[层级]·[文件名称与报告期]</span>
    <span class="fig-note">读图要点：[该图支持什么判断]</span>
  </figcaption>
</figure>

<h2 id="risk">风险来源：它最怕什么变化</h2>
<h3>外部压力的来源</h3>
<p>[按支付端、采购端、结算端三类分别说明。写明各自传导至价格、份额还是成本。]</p>

<figure>
  <div class="fig-body">[图二：关键财务指标的逐期折线图]</div>
  <figcaption>
    <span class="fig-title">图 2　[关键指标的逐期变化]</span>
    <span class="fig-src">数据来源：[层级]·[文件名称与报告期]</span>
    <span class="fig-note">读图要点：[趋势说明了什么]</span>
  </figcaption>
</figure>

<h3>同业对照</h3>
<p>[说明对照对象的选择依据，须为同行业、同模式、同收入结构。]</p>

<figure>
  <div class="fig-body">[图三：公司与可比公司的同期分组柱状图，营收与净利各一组]</div>
  <figcaption>
    <span class="fig-title">图 3　[同期营收与净利同比：公司与可比公司对照]</span>
    <span class="fig-src">数据来源：[层级]·[各公司同期报告]</span>
    <span class="fig-note">读图要点：[压力属行业性还是个体性]</span>
  </figcaption>
</figure>

<h2 id="switch">可转换性：换不换得动</h2>
<p>[第三步，全文关键。依次回答三个子问题。]</p>
<p><strong>是否存在替代路径</strong>：[有／无。若有，是什么。]</p>
<p><strong>替代路径的体量是否足够</strong>：[计算主业缺口的绝对金额，与替代业务的体量对照，说明按当前增速所需时间。]</p>
<p><strong>转换的代价</strong>：[已投入的重资产、组织与渠道，量化转换成本的量级。]</p>

<figure>
  <div class="fig-body">[图四：主业缺口与替代业务体量的对照条形图或瀑布图]</div>
  <figcaption>
    <span class="fig-title">图 4　[主业缺口与替代业务体量对照]</span>
    <span class="fig-src">数据来源：[层级]·[文件名称与报告期]</span>
    <span class="fig-note">读图要点：[体量是否足以补足缺口]</span>
  </figcaption>
</figure>

<p><strong>判断</strong>：[换不动／换得动但慢／换得动。对应风险类别。]</p>

<h2 id="robust">抗风险能力的两层分辨</h2>
<p><strong>第一层·来源</strong>：[属主动设计的部分与属周期巧合的部分分别是什么。]</p>
<p><strong>第二层·可控性</strong>：[哪些在下一周期仍可沿用，哪些随窗口变化而失效。]</p>
<p>[若抗风险能力来自周期错位而非制度设计，须明确指出。]</p>

<h2 id="transform">转型路径的可行性</h2>
<table>
  <thead><tr><th>路径</th><th>基础</th><th>难点</th><th>见效时间</th></tr></thead>
  <tbody><tr><td></td><td></td><td></td><td></td></tr></tbody>
</table>
<p>[方向正确与能否在所需时间内见效是两个问题，须分别作答。]</p>

<h2 id="counter">需要承认的另一面</h2>
<p>[列出对公司有利的事实与支撑数据。缺此节会使分析偏颇，可信度下降。]</p>

<h2 id="caution">风险提示</h2>
<ul>
  <li><strong>数据边界</strong>：哪些数据未获取或标注为待核实，及其对结论的影响范围</li>
  <li><strong>假设前提</strong>：分析基于哪些假设，假设不成立时结论如何变化</li>
  <li><strong>外部风险</strong>：哪些政策或市场变化会推翻判断</li>
  <li><strong>时点风险</strong>：分析基于截至某期的数据，此后的变化未纳入</li>
</ul>

<h3>分析覆盖范围</h3>
<p>[逐项声明行业经济特征各维度的覆盖情况。未覆盖的维度必须列出并说明原因，不能省略。读者据此判断分析的完整程度。]</p>
<table>
  <thead><tr><th>行业特征</th><th>状态</th><th>说明</th></tr></thead>
  <tbody>
    <tr><td>产业盈利水平及变动趋势</td><td></td><td></td></tr>
    <tr><td>市场规模和增长率</td><td></td><td></td></tr>
    <tr><td>行业生命周期阶段</td><td></td><td></td></tr>
    <tr><td>技术进步速度</td><td></td><td></td></tr>
    <tr><td>规模经济与经验影响</td><td></td><td></td></tr>
    <tr><td>范围经济效应</td><td></td><td></td></tr>
    <tr><td>产能利用情况</td><td></td><td></td></tr>
    <tr><td>进入与退出壁垒</td><td></td><td></td></tr>
    <tr><td>纵向整合程度</td><td></td><td></td></tr>
    <tr><td>资源需求与供应状况</td><td></td><td></td></tr>
    <tr><td>客户需求与条件</td><td></td><td></td></tr>
    <tr><td>产品技术特征与主要参与者</td><td></td><td></td></tr>
    <tr><td>竞争者数量与分布</td><td></td><td></td></tr>
  </tbody>
</table>
<p>[说明哪几项未覆盖对结论影响最大，该缺失是否影响主要判断的成立。]</p>

<h2 id="conclusion">结论</h2>
<p>[回应开篇提出的命题，明确作答。]</p>
<p>[直接给出判断，不使用"综上所述""总而言之"这类结构。]</p>

<!-- 可选：仅在用户确认纳入估值参照时保留本节，其余情形连同导航链接一并删除 -->
<h2 id="valuation">估值参照</h2>
<p>[一句说明本节回答的问题：当前价格隐含什么假设，该假设与本报告的模式判断是否相容。须写明本节不产出目标价与买卖结论。]</p>

<h3>估值口径</h3>
<table>
  <thead><tr><th>指标</th><th>数值</th><th>口径</th><th>取数日</th></tr></thead>
  <tbody>
    <tr><td>市盈率（TTM）</td><td></td><td>滚动十二个月，注明起止期间</td><td></td></tr>
    <tr><td>市盈率（静态）</td><td></td><td>上一完整会计年度</td><td></td></tr>
    <tr><td>市净率</td><td></td><td>注明净资产口径</td><td></td></tr>
    <tr><td>[市销率或 EV/EBITDA，按行业特征增列]</td><td></td><td></td><td></td></tr>
  </tbody>
</table>
<p>[历史分位及其区间与起算年份；同业分位及其名单。两者含义不同，须分别标注，不得笼统称为估值分位。同业名单须与同群对照组一致。]</p>

<h3>价格隐含的假设</h3>
<p>[取历史峰值利润、最近一期利润、本报告判断的常态利润三个基准，分别计算对应倍数，显示当前价格落在何处。]</p>
<p>[写成检验句，规范形式为"当前价格隐含的前提是"，指向具体经营结果，不写成"市场看好该公司"。]</p>
<p>[与可转换性判断对照，给出三态关系中的一种：定价偏悲观、定价偏乐观、与判断一致。第二种关系须说明判断定价偏乐观不等于预测价格下跌。]</p>

<h3>本节边界</h3>
<p>[写明所用假设及其依据，未列明依据的假设不得进入结论。说明估值数据的取数时点与未纳入的因素。]</p>

<h2 id="advice">给投资者的建议</h2>
<h3>估值隐含的预期</h3>
<p>[已设估值参照节时，本段复用该节结论，不重复列示口径表。未设该节时，本段自行说明估值水平、口径、取数日期与来源，并反推该价格已假设的经营结果。两处结论须一致。]</p>

<h3>应当关注的指标</h3>
<table>
  <thead><tr><th>观察点</th><th>看什么</th><th>说明什么</th></tr></thead>
  <tbody><tr><td></td><td></td><td class="neutral">恶化／改善</td></tr></tbody>
</table>
<p>[同时写明哪些指标不需关注，排除与结论无关的短期波动。]</p>

<h3>按立场的应对</h3>
<p>[按未持仓、已持仓、低风险偏好三类分别说明判断依据与需观察的条件。不给出目标价与买卖建议。]</p>

<h3>边界说明</h3>
<p>[说明估值取自哪个时点、市场情绪未纳入、建议基于公开信息、不构成投资决策依据。]</p>

<!-- 可选：仅在用户确认纳入外部观点辑录时保留本节。本节为隔离区，只列不评，其他章节不得回引 -->
<h2 id="digest">附录：外部资料与市场观点辑录</h2>
<p class="src-note">本节所收内容均为第三方公开发布，收录用于呈现该公司所处的信息公开环境，<strong>不代表本报告采纳其中任何判断</strong>，也不构成本报告的论据。本节内容不在其他章节引用。</p>

<h3>公司口径的历史表述</h3>
<table>
  <thead><tr><th>日期</th><th>来源文件</th><th>表述摘录</th><th>获取途径</th></tr></thead>
  <tbody>
    <tr><td></td><td></td><td>[摘录原话或忠实转述，保留原有限定语与条件状语]</td><td></td></tr>
  </tbody>
</table>

<h3>监管与主管部门文件</h3>
<table>
  <thead><tr><th>发布日期</th><th>发布主体</th><th>文件名称或事项</th><th>与本行业相关的表述</th></tr></thead>
  <tbody>
    <tr><td></td><td></td><td></td><td></td></tr>
  </tbody>
</table>

<h3>机构观点</h3>
<p class="src-note">评级与目标价为原文照录，属第三方观点。同一指标在不同机构之间不一致时并列列出并说明分歧所在，不得只取一家。</p>
<table>
  <thead><tr><th>机构</th><th>报告主题</th><th>日期</th><th>评级</th><th>目标价</th><th>观点要点摘录</th><th>原文途径</th></tr></thead>
  <tbody>
    <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  </tbody>
</table>

<h3>个人投资者观点</h3>
<p class="src-note">单独成组，不与机构观点合并排序或统计。所引数据不因收录而获得来源地位。</p>
<ul>
  <li>[平台、账号、日期]　[观点摘录]</li>
</ul>

<h3>市场反应</h3>
<table>
  <thead><tr><th>触发事件</th><th>事件日期</th><th>后 1 个交易日</th><th>后 5 个交易日</th><th>后 20 个交易日</th><th>同期基准</th></tr></thead>
  <tbody>
    <tr><td></td><td></td><td></td><td></td><td></td><td>[大盘指数与所属行业指数的同期涨跌幅]</td></tr>
  </tbody>
</table>
<p class="src-note">行情来源、复权口径与取数日：[须写明]。本节不解释涨跌原因，时间相邻不等于存在因果关系。</p>

<h2 id="sources">数据来源</h2>
<div class="filters">
  <span>筛选：</span>
  <button type="button" data-filter="all" aria-pressed="true">全部</button>
  <button type="button" data-filter="level1" aria-pressed="false">一级来源</button>
  <button type="button" data-filter="level2" aria-pressed="false">二级来源</button>
  <!-- 仅当来源表存在三级来源行时保留本行，并在脚本的显示判断中补入 level3 一项；
       否则三级行会随任一层级筛选消失且无法单独筛出。 -->
  <button type="button" data-filter="level3" aria-pressed="false">三级来源</button>
  <button type="button" data-filter="pending" aria-pressed="false">待核实</button>
</div>
<table>
  <thead><tr>
    <th>数据项</th><th>数值／口径</th><th>层级</th><th>来源名称</th>
    <th>日期</th><th>定位</th><th>状态</th>
  </tr></thead>
  <tbody>
    <tr data-level="1" data-status="ok"><td></td><td></td><td>一级</td><td></td><td></td><td></td><td>已核实</td></tr>
  </tbody>
</table>
<p class="src-note">[筛选按钮的 data-filter 取值为 all／level1／level2／pending。每行须标注 data-level（1 或 2）与 data-status（ok 或 pending），缺一即筛选失效。]</p>

<footer class="rpt">
  <p>本报告依据公开信息编制，所引数据均标注来源与核实状态，核实状态见上方数据来源表。报告中的判断为本方法框架下的分析结论，不构成投资决策依据。</p>
</footer>

<script>
(function(){
  var btns = document.querySelectorAll('.filters button');
  var rows = document.querySelectorAll('#sources tbody tr');
  Array.prototype.forEach.call(btns, function(b){
    b.addEventListener('click', function(){
      Array.prototype.forEach.call(btns, function(x){ x.setAttribute('aria-pressed','false'); });
      b.setAttribute('aria-pressed','true');
      var f = b.getAttribute('data-filter');
      Array.prototype.forEach.call(rows, function(r){
        var lvl = r.getAttribute('data-level');
        var st = r.getAttribute('data-status');
        var show = (f === 'all') || (f === 'level1' && lvl === '1')
                || (f === 'level2' && lvl === '2') || (f === 'level3' && lvl === '3')
                || (f === 'pending' && st === 'pending');
        r.classList.toggle('hide', !show);
      });
    });
  });
  function beforePrint(){
    Array.prototype.forEach.call(document.querySelectorAll('details'), function(x){ x.open = true; });
    Array.prototype.forEach.call(rows, function(r){ r.classList.remove('hide'); });
  }
  window.addEventListener('beforeprint', beforePrint);
})();
</script>

</div>
</body>
</html>
```

## 图表配置要求

正文须含四至七张图表，分别承载下列判断。图表类型的选择依据见 `visual-guide.md`。

| 序号 | 承载的判断 | 建议图表类型 |
|---|---|---|
| 图 1 | 收入的构成与底盘所在 | 环形图或堆叠条形图 |
| 图 2 | 外部压力在财务指标上的时间轨迹 | 折线图 |
| 图 3 | 压力属行业性还是个体性 | 分组柱状图，公司与可比公司并列 |
| 图 4 | 替代路径的体量能否补足主业缺口 | 对照条形图或瀑布图 |
| 图 5（可选） | 公司与同业在多项指标上的相对位置 | 雷达图或热力表 |
| 图 6（可选） | 既定目标与当前水平的距离 | 进度条形图 |
| 图 7（可选） | 关键变量变化对结论的影响 | 龙卷风图或敏感性条形图 |

图 7 仅在含情景分析时出现，规范见 `scenario-guide.md`。

每张图表下方的三行标注（标题、来源、读图要点）不可省略。图表中的数据须与正文一致，取整规则统一。

## 交互元素

报告须含四类交互元素，规范见 `visual-guide.md`。骨架中已内置实现，成稿时保留并补齐内容。

| 元素 | 位置 | 实现方式 |
|---|---|---|
| 结论卡展开依据 | 核心结论各卡片内 | `details` 与 `summary`，展开后显示支撑该判断的数据与来源 |
| 数据来源表筛选 | 数据来源表上方 | 按钮组切换行的显示，按层级与核实状态筛 |
| 图表数值提示 | 各图表图形元素内 | SVG 的 `title`，悬停显示精确值 |
| 图表口径切换 | 多指标对照图 | 按钮切换两组数据，避免并排成两张小图 |

**渐进增强是硬要求。** 关闭脚本后报告的全部内容仍须可读，打印预览中不得有内容因折叠或筛选而缺失。骨架中的脚本在 `beforeprint` 时自动展开全部折叠项并清除筛选，成稿时不得删去该处理。

**交互控件须有文字标签**，不用图标代替。来源表的 `data-level` 与 `data-status` 两个属性不得遗漏，否则筛选失效。

## 写作检查

成稿前逐项核对：

- 核心结论可在三到五句内完整表述
- 每一步追问均落在具体数据上，无空泛论断
- 同业对照已做，且给出行业性或个体性的判断
- 第三步给出明确的可转换性答案
- 结论已分层，收入层面与利润层面分别表述
- 已写入"需要承认的另一面"
- 风险提示写清数据边界与假设前提
- 图表在四至七张之间，且覆盖收入构成、时间趋势、同业对照、体量缺口四类判断
- 无重复作图的图表（同一结论对应多张图属凑数）
- 每张图表的标题、来源、读图要点三行齐全
- 涨跌配色遵循 A 股惯例，且全篇一致
- 若有投资建议节：估值标注了口径、取数日期与来源
- 若有估值参照节：口径表含口径与取数时点，未只给单一数字
- 若有估值参照节：历史分位与同业分位分别标注，同业名单与同群对照组一致
- 若有估值参照节：已给出"当前价格隐含的前提是"形式的检验句，且指向具体经营结果
- 若有估值参照节：结论与可转换性判断一致，且与投资建议节无矛盾
- 标的亏损或属周期性行业时，已按 `valuation-guide.md` 的特殊情形规则处理，未硬套市盈率
- 估值参照中若引入假设，其取值依据已写入风险提示或本节边界
- 若有外部观点辑录节：节首已写声明，收录不等于认同，本节不构成论据
- 若有外部观点辑录节：每条均标注发布主体、日期与原文获取途径
- 若有外部观点辑录节：全文无评价性表述，未出现"切中要害""已被证实""值得关注""观点偏颇"一类用语
- 若有外部观点辑录节：其他章节未回引本节，检索"如某机构所言""据业内人士"为零
- 若有外部观点辑录节：评级与目标价均已标注为第三方观点，未混入本报告结论
- 若有外部观点辑录节：同一指标存在不一致数值时已并列并说明分歧
- 若有外部观点辑录节：市场反应的每个时点均含触发事件、阶段涨跌幅与比较基准，且未解释涨跌原因
- 若有外部观点辑录节：四组条数与总篇幅均在上限之内，个人观点单独成组
- 若有投资建议节：观察点控制在三到四个，且可由公开信息验证
- 若有投资建议节：未出现"建议买入""目标价"这类表述
- 数据来源表七个字段齐全，层级与状态无遗漏
- 正文未以固定数字声称待核实或未核实的项数；若声称，该数字须与来源表实际行数一致
- 正文数字控制在十处以内，精确数据收进来源表
- 每个数字标了来源，无无来源数字
- 未获取的数据如实标注，未用推测填充
- 页面不依赖外部资源，可离线正常显示与打印
- 含窄屏响应式规则，表格在手机上可横向滚动
- 正文检索 `**` 与行首 `#` 均为零，无残留 Markdown 语法
- 已含行业环境章节，且置于公司概况之前
- 已含分析覆盖范围表，未覆盖的维度如实列出并说明原因
- 每张柱状图的柱长与数值成比例，逐柱验算比值一致
- 柱状图的正负以方向区分，零线有标注，方向含义写入读图要点
- 所有 SVG 文字坐标加上所属分组偏移量后仍在画布范围内
- 核心结论未单独依赖"待核实"数据；若确有依赖，已在数据边界中写明影响范围
- 四类交互元素齐备，且关闭脚本后内容仍完整可读
- 打印预览中无内容因折叠或筛选而缺失
- 来源表各行的 `data-level` 与 `data-status` 已标注，筛选可用
- 已自查无破折号插入语、无提示性冒号、无加粗小标题式罗列、无段段升华收尾，并符合本技能的学术语体要求；环境中若有 `lieflat-less-ai-tone`，已按其规则集完整检查
