#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研报 HTML 自检脚本

用法:
    python validate-report.py <报告文件.html>

输出每项检查的 PASS / WARN / FAIL，末尾给出汇总。
存在 FAIL 时退出码为 1，仅 WARN 时为 0。

设计原则（改动本脚本时须遵守）:
    校验的输入必须来自被校验的文件，不能来自作者对文件的记忆。
    把数值与像素坐标写死进脚本，只能验证"抄进来的数字与算出的比例
    一致"，发现不了锚点错位与刻度失配，因为两者用的是同一套错误坐标。
"""

import re
import sys
from pathlib import Path

ICONS = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}
COUNTS = {"PASS": 0, "WARN": 0, "FAIL": 0}
LOG = []


def chk(label, cond, extra="", warn_only=False):
    """cond 为假时，warn_only 决定记为 WARN 还是 FAIL"""
    level = "PASS" if cond else ("WARN" if warn_only else "FAIL")
    COUNTS[level] += 1
    LOG.append((level, label, extra))
    return cond


def note(text):
    LOG.append(("", text, ""))


# ---------------------------------------------------------------- 文本解析
CN = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
      "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def region(doc, start_id, end_id=None):
    """取出 id=start_id 到 id=end_id 之间的片段，用于分区检查"""
    parts = doc.split(start_id, 1)
    if len(parts) < 2:
        return None
    seg = parts[1]
    if end_id:
        seg = seg.split(end_id, 1)[0]
    return seg


# ---------------------------------------------------------------- 1. 格式
def check_format(h):
    star = h.count("**")
    chk("无残留 Markdown 加粗 (**)", star == 0, f"计数={star}")
    chk("无行首 Markdown 标题", not re.search(r"^\s*#{1,6}\s", h, re.M))
    chk("无表头管道符表格", not re.search(r"^\|.*\|$", h, re.M))
    # HTML 与 SVG 标签都须配对。
    # SVG 图形元素曾长期不在本列表内，导致 15 处未闭合的 <rect> 全部漏检，
    # 报告仍显示"全部通过"。凡图表中会出现的标签都要列入。
    for tag in ["div", "table", "svg", "g", "text", "script", "details",
                "figure", "nav", "header", "footer", "tbody", "thead",
                "tr", "td", "th", "ul", "ol", "li", "p", "strong", "span",
                # SVG 图形与容器元素
                "rect", "circle", "ellipse", "path", "polygon", "polyline",
                "line", "title", "tspan", "defs", "linearGradient",
                "radialGradient", "stop", "clipPath", "marker", "filter",
                "feDropShadow", "feGaussianBlur"]:
        o = len(re.findall(r"<" + tag + r"[\s/>]", h))
        c = len(re.findall(r"</" + tag + r">", h))
        sc = len(re.findall(r"<" + tag + r"\b[^>]*/>", h))
        chk(f"标签配对 <{tag}>", o == c + sc, f"开{o} 闭{c} 自闭合{sc}")


# ---------------------------------------------------------------- 2. 交互元素
def check_interaction(h):
    chk("结论卡 details/summary", "<details>" in h and "<summary>" in h,
        warn_only=True)
    chk("来源表筛选按钮", 'data-filter="all"' in h, warn_only=True)
    chk("内联脚本", "<script>" in h, warn_only=True)
    chk("打印处理 beforeprint", "beforeprint" in h, warn_only=True)

    # 筛选按钮的取值须与脚本判断一致，否则按钮点了没反应
    filters = set(re.findall(r'data-filter="([a-z0-9]+)"', h))
    logic = set(re.findall(r"f === '([a-z0-9]+)'", h))
    if filters:
        chk("筛选取值与脚本一致", filters == logic,
            f"按钮 {sorted(filters)}，脚本 {sorted(logic)}", warn_only=True)
    mb = set(re.findall(r'data-metric="([a-z0-9]+)"', h))
    ml = set(re.findall(r"m === '([a-z0-9]+)'", h))
    if mb:
        chk("图表切换取值与脚本一致", mb == ml,
            f"按钮 {sorted(mb)}，脚本 {sorted(ml)}", warn_only=True)


# ---------------------------------------------------------------- 3. 样式
def check_style(h):
    chk("窄屏响应式规则", "@media" in h and "max-width" in h,
        "缺少时多列来源表在手机上会溢出")
    chk("打印页边距", "@page" in h, warn_only=True)
    chk("打印时恢复被筛行", "beforeprint" in h, warn_only=True)
    chk("无外部资源引用", not re.search(r'(src|href)="https?://', h),
        "单文件 HTML 不应依赖外部资源")


# ---------------------------------------------------------------- 4. 图表几何
# 全部从文件解析。写死数值与像素高度无法发现锚点错位与刻度失配。
def scan_svgs(doc):
    figs = []
    for vb, body in re.findall(
            r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*?)</svg>', doc, re.S):
        tx = ty = 0.0
        stack, bars, ticks = [], [], []
        panel = "root"
        for line in body.split("\n"):
            gm = re.search(r"<g\b([^>]*)>", line)
            if gm:
                stack.append((tx, ty, panel))
                attrs = gm.group(1)
                mt = re.search(r"translate\((-?[\d.]+)[ ,]+(-?[\d.]+)\)", attrs)
                if mt:
                    tx += float(mt.group(1))
                    ty += float(mt.group(2))
                mid = re.search(r'\bid="([^"]+)"', attrs)
                if mid:
                    panel = mid.group(1)      # 具名分组视为独立面板
            if "</g>" in line and stack:
                tx, ty, panel = stack.pop()
            rm = re.search(r"<rect([^>]*)>(?:\s*<title>([^<]*)</title>)?", line)
            if rm:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', rm.group(1)))
                if all(k in d for k in ("x", "y", "width", "height")):
                    bars.append(dict(
                        x=tx + float(d["x"]), y=ty + float(d["y"]),
                        w=float(d["width"]), h=float(d["height"]),
                        op=float(d.get("opacity", 1)), panel=panel,
                        title=rm.group(2) or ""))
            tm = re.search(r"<text\b([^>]*)>([^<]*)</text>", line)
            if tm:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', tm.group(1)))
                if "y" in d:
                    ticks.append(dict(y=ty + float(d["y"]), panel=panel,
                                      txt=tm.group(2).strip()))
        figs.append(dict(vb=vb, bars=bars, ticks=ticks,
                         ntitle=len(re.findall(r"<title>", body))))
    return figs


def magnitudes(title):
    """条形取值可能是百分比，也可能是金额，两种口径都取出备用"""
    out = {}
    m = re.search(r"([+−-]?\d+(?:\.\d+)?)\s*%", title)
    if m:
        out["百分比"] = float(m.group(1).replace("−", "-").replace("+", ""))
    m = re.search(r"(\d+(?:\.\d+)?)\s*亿元", title)
    if m:
        out["亿元"] = float(m.group(1))
    return out


def titled(bars):
    return [x for x in bars if magnitudes(x["title"])]


def by_panel(bars):
    g = {}
    for x in bars:
        g.setdefault(x["panel"], []).append(x)
    return g


def prop(units, group, size):
    """在候选口径中找出使条形长度与数值成正比的那一个"""
    best, bestr = None, []
    for unit in units:
        vals = [(magnitudes(x["title"]).get(unit), x) for x in group]
        if any(v is None for v, _ in vals):
            continue
        rs = [x[size] / abs(v) for v, x in vals if abs(v) > 0.5]
        if len(rs) < 2:
            continue
        spread = (max(rs) - min(rs)) / max(rs)
        if spread < 0.02:
            return unit, rs
        cur = (max(bestr) - min(bestr)) / max(bestr) if bestr else 2
        if spread < cur:
            best, bestr = unit, rs
    return best, bestr


def check_charts(h):
    n = h.count("<svg")
    chk("图表数量在 4 至 7 张之间", 4 <= n <= 7, f"实际 {n} 张", warn_only=True)

    figs = scan_svgs(h)
    vert, horiz = [], []
    for f in figs:
        b = titled(f["bars"])
        if len(b) < 3:
            continue
        is_vert = len({round(x["h"], 1) for x in b}) > len({round(x["w"], 1) for x in b})
        (vert if is_vert else horiz).append((f, b))
    note(f"     图表解析：竖柱图 {len(vert)} 张，横条图 {len(horiz)} 张")

    UNITS = ("百分比", "亿元")

    for fi, (f, b) in enumerate(vert, 1):
        for pname, group in by_panel(b).items():
            if len(group) < 2:
                continue
            tag = f"竖柱图{fi}" + (f"〔{pname}〕" if pname != "root" else "")
            # 各柱须锚定同一条基线：正值取底边，负值取顶边
            base = []
            for x in group:
                vs = magnitudes(x["title"])
                v = vs.get("百分比", vs.get("亿元", 0))
                base.append((x["y"] + x["h"]) if v >= 0 else x["y"])
            spread = max(base) - min(base)
            chk(f"{tag} 各柱共同基线", spread < 1.5,
                f"基线散布 {spread:.2f}px，基线 y≈{min(base):.1f}")
            unit, rs = prop(UNITS, group, "h")
            chk(f"{tag} 柱长与数值成比例（口径 {unit}）",
                bool(rs) and (max(rs) - min(rs)) / max(rs) < 0.02,
                "比值 " + ", ".join(f"{r:.3f}" for r in rs) if rs else "无法判定")
            # 轴刻度须与柱长共用同一比例尺，否则网格线在骗人
            if rs:
                sc = sorted(rs)[len(rs) // 2]
                zero = sorted(base)[len(base) // 2]
                mism = []
                for t in f["ticks"]:
                    if t["panel"] != pname:
                        continue
                    m = re.fullmatch(r"([+−-]?)(\d+)\s*%", t["txt"])
                    if not m:
                        continue
                    pct = int(m.group(2)) * (-1 if m.group(1) in ("−", "-") else 1)
                    implied = zero - pct * sc
                    if abs(implied - t["y"]) > 6:
                        mism.append(f"{t['txt']} 应在 y≈{implied:.0f}，实际 {t['y']:.0f}")
                chk(f"{tag} 轴刻度与柱长比例自洽", not mism,
                    "；".join(mism) if mism else f"比例 {sc:.2f}px/单位")

    for fi, (f, b) in enumerate(horiz, 1):
        for pname, group in by_panel(b).items():
            if len(group) < 2:
                continue
            tag = f"横条图{fi}" + (f"〔{pname}〕" if pname != "root" else "")
            sv = sorted(group, key=lambda x: x["x"])
            chain = [abs(sv[i + 1]["x"] - (sv[i]["x"] + sv[i]["w"]))
                     for i in range(len(sv) - 1)]
            if chain and max(chain) < 1.5:
                chk(f"{tag} 各段首尾相接", True,
                    f"最大间隙 {max(chain):.2f}px，共 {len(sv)} 段")
                # 堆叠图各段须在同一行，否则视觉上会错开
                dys = max(x["y"] for x in sv) - min(x["y"] for x in sv)
                dhs = max(x["h"] for x in sv) - min(x["h"] for x in sv)
                chk(f"{tag} 各段同一行", dys < 1.5 and dhs < 1.5,
                    f"y 散布 {dys:.2f}px，高度散布 {dhs:.2f}px")
                # 各段占比之和须为 100%。只检查长度比例是不够的：
                # 若某段同时标注了金额与占比，金额自洽而占比被改错时，
                # 比例检查会按金额口径通过，占比错误就被掩盖了。
                pcts = [magnitudes(x["title"]).get("百分比") for x in sv]
                if all(p is not None for p in pcts):
                    s = sum(pcts)
                    chk(f"{tag} 各段占比合计 100%", abs(s - 100) < 0.5,
                        f"合计 {s:.2f}%")
            else:
                lefts = [x["x"] for x in group]
                rights = [x["x"] + x["w"] for x in group]
                dl, dr = max(lefts) - min(lefts), max(rights) - min(rights)
                anchor = "左端" if dl < 1.5 else ("右端" if dr < 1.5 else "无")
                chk(f"{tag} 各条对齐", anchor != "无",
                    f"对齐于{anchor}；左端散布 {dl:.2f}px，右端散布 {dr:.2f}px")
            unit, rs = prop(UNITS, group, "w")
            chk(f"{tag} 条长与数值成比例（口径 {unit}）",
                bool(rs) and (max(rs) - min(rs)) / max(rs) < 0.02,
                "比值 " + ", ".join(f"{r:.3f}" for r in rs) if rs else "无法判定")

    miss = [i for i, f in enumerate(figs, 1) if f["ntitle"] < 1]
    chk("每张图均含悬停提示", not miss,
        f"无提示的图 {miss}" if miss else f"{len(figs)} 张图均有")
    tot = sum(f["ntitle"] for f in figs)
    nbars = sum(len(titled(f["bars"])) for f in figs)
    chk("带数值的条形均配提示", tot >= nbars,
        f"图表内 title={tot}，带数值条形 {nbars}")

    # 三行标注：标题、来源、读图要点
    titles = len(re.findall(r'class="fig-title"', h))
    if titles:
        chk("图表三行标注齐备", titles >= n, f"fig-title {titles} 处，图 {n} 张")
    else:
        chk("图表三行标注齐备", False, "未检出 fig-title，无法确认三行标注",
            warn_only=True)


# ---------------------------------------------------------------- 4b. 画布越界
# 画布高度不足会让最长的柱、数值标签或类目名被裁掉。这类问题不会报错，
# 只会直接印在页面上，因此必须机器检查而非目测。
def scan_elements(doc):
    """解析每个 svg 的 viewBox，以及矩形与文字的绝对坐标"""
    out = []
    for vb, body in re.findall(
            r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*?)</svg>', doc, re.S):
        nums = [float(x) for x in re.split(r"[\s,]+", vb.strip()) if x]
        box = nums if len(nums) == 4 else None
        tx = ty = 0.0
        stack = []
        rects, texts = [], []
        for line in body.split("\n"):
            gm = re.search(r"<g\b([^>]*)>", line)
            if gm:
                stack.append((tx, ty))
                mt = re.search(r"translate\((-?[\d.]+)[ ,]+(-?[\d.]+)\)", gm.group(1))
                if mt:
                    tx += float(mt.group(1))
                    ty += float(mt.group(2))
            if "</g>" in line and stack:
                tx, ty = stack.pop()
            rm = re.search(r"<rect([^>]*)/?>", line)
            if rm:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', rm.group(1)))
                if all(k in d for k in ("x", "y", "width", "height")):
                    rects.append(dict(x=tx + float(d["x"]), y=ty + float(d["y"]),
                                      w=float(d["width"]), h=float(d["height"])))
            tm = re.search(r"<text\b([^>]*)>([^<]*)</text>", line)
            if tm:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', tm.group(1)))
                if "y" in d:
                    texts.append(dict(
                        x=tx + float(d.get("x", 0)), y=ty + float(d["y"]),
                        fs=float(re.search(r"([\d.]+)", d.get("font-size", "12")).group(1)),
                        anchor=d.get("text-anchor", "start"),
                        txt=tm.group(2).strip()))
        out.append(dict(box=box, rects=rects, texts=texts))
    return out


def est_width(txt, fs):
    """中日韩字符按一个字宽，其余按 0.55 倍估算。估算只用于判越界，不用于排版。"""
    w = 0.0
    for ch in txt:
        w += fs if ord(ch) > 0x2E7F else fs * 0.55
    return w


def check_bounds(h):
    for i, f in enumerate(scan_elements(h), 1):
        if not f["box"]:
            chk(f"图{i} 含 viewBox", False, "无法判越界", warn_only=True)
            continue
        vx, vy, vw, vh = f["box"]
        bad = []
        for r in f["rects"]:
            if r["x"] < vx - 0.5:
                bad.append(f"矩形左侧越出 {vx - r['x']:.1f}px")
            if r["x"] + r["w"] > vx + vw + 0.5:
                bad.append(f"矩形右侧越出 {r['x'] + r['w'] - (vx + vw):.1f}px")
            if r["y"] < vy - 0.5:
                bad.append(f"矩形上方越出 {vy - r['y']:.1f}px")
            if r["y"] + r["h"] > vy + vh + 0.5:
                bad.append(f"矩形下方越出 {r['y'] + r['h'] - (vy + vh):.1f}px")
        for t in f["texts"]:
            w = est_width(t["txt"], t["fs"])
            if t["anchor"] == "middle":
                x0, x1 = t["x"] - w / 2, t["x"] + w / 2
            elif t["anchor"] == "end":
                x0, x1 = t["x"] - w, t["x"]
            else:
                x0, x1 = t["x"], t["x"] + w
            if x0 < vx - 0.5:
                bad.append(f"「{t['txt']}」左侧越出 {vx - x0:.1f}px")
            if x1 > vx + vw + 0.5:
                bad.append(f"「{t['txt']}」右侧越出 {x1 - (vx + vw):.1f}px")
            # 基线上方留出约 0.8 倍字高为字身上沿
            if t["y"] - t["fs"] * 0.8 < vy - 0.5:
                bad.append(f"「{t['txt']}」上方越出 {vy - (t['y'] - t['fs'] * 0.8):.1f}px")
            if t["y"] + t["fs"] * 0.25 > vy + vh + 0.5:
                bad.append(f"「{t['txt']}」下方越出 {t['y'] + t['fs'] * 0.25 - (vy + vh):.1f}px")
        chk(f"图{i} 元素未越出画布", not bad, "；".join(bad[:3]) if bad else
            f"{len(f['rects'])} 矩形、{len(f['texts'])} 文字均在画布内")


# ---------------------------------------------------------------- 5. 章节
REQUIRED = ["核心结论", "行业环境", "公司概况", "收入结构", "风险敞口",
            "可转换性", "抗风险能力", "转型可行性", "另一面", "风险提示",
            "分析覆盖范围", "结论", "数据来源"]
OPTIONAL = ["估值参照", "给投资者的建议", "外部观点辑录", "情景分析"]


def check_sections(h):
    for s in REQUIRED:
        chk(f"含章节「{s}」", s in h)
    found = [s for s in OPTIONAL if s in h]
    note(f"     可选章节：{('、'.join(found)) if found else '无'}")


# ---------------------------------------------------------------- 6. 来源表
LVL = {"1": "一级", "2": "二级", "3": "三级"}
STA = {"ok": "已核实", "pending": "待核实", "unverified": "未核实"}


def check_source_table(h):
    trows = re.findall(r'<tr data-level="(\d)" data-status="(\w+)">(.*?)</tr>', h, re.S)
    if not trows:
        chk("数据来源表存在", False, "未检出带 data-level 的行")
        return []
    stats = {}
    for lv, _, _ in trows:
        stats[lv] = stats.get(lv, 0) + 1
    note("     来源表 %d 行：%s" % (
        len(trows), "、".join(f"{LVL.get(k, k)} {v}" for k, v in sorted(stats.items()))))

    bad = []
    for i, (lv, sname, body) in enumerate(trows, 1):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", body, re.S)
        if len(cells) < 7:
            bad.append(f"第{i}行列数={len(cells)}")
            continue
        if cells[2].strip() != LVL.get(lv):
            bad.append(f"第{i}行层级列「{cells[2].strip()}」≠ data-level={lv}")
        if cells[6].strip() != STA.get(sname):
            bad.append(f"第{i}行状态列「{cells[6].strip()}」≠ data-status={sname}")
    chk("来源表层级／状态两列与属性一致", not bad,
        "；".join(bad[:5]) if bad else f"{len(trows)} 行全部一致")

    # 筛选按钮须覆盖表内出现的全部层级
    btns = sorted(set(re.findall(r'data-filter="level(\d)"', h)))
    tbl = sorted(set(lv for lv, _, _ in trows))
    chk("筛选按钮覆盖表内全部层级", set(tbl) <= set(btns),
        f"表内 {tbl}，按钮 {btns}")

    # 计数漂移：正文写死的数字不会随来源表增删自动更新
    pend_n = sum(1 for _, s, _ in trows if s == "pending")
    unv_n = sum(1 for _, s, _ in trows if s == "unverified")
    body_only = h.split('id="sources"')[0]
    bad_c = []
    for word, kind in re.findall(
            r"([零一二三四五六七八九十]+|\d+)\s*项[^。；，]{0,16}?(待核实|未核实)",
            body_only):
        num = CN.get(word, int(word) if word.isdigit() else None)
        real = pend_n if kind == "待核实" else unv_n
        if num is not None and num != real:
            bad_c.append(f"正文称 {word} 项{kind}，表中实为 {real}")
    chk("正文声称的待核实／未核实项数与表一致", not bad_c,
        "；".join(bad_c) if bad_c else
        f"表中待核实 {pend_n}、未核实 {unv_n}，正文无相悖计数")
    return trows


# ---------------------------------------------------------------- 7. 辑录节隔离
def check_digest(h):
    if 'id="digest"' not in h:
        return
    dg = region(h, 'id="digest"', 'id="sources"') or ""
    chk("辑录节含收录不等于认同的声明",
        "不代表本报告采纳其中任何判断" in dg or "不等于认同" in dg)
    chk("辑录节声明不在其他章节引用", "本节内容不在其他章节引用" in dg)
    chk("辑录节声明不解释涨跌原因", "本节不解释涨跌原因" in dg)

    # 其他章节不得回引
    head = h.split('id="digest"')[0]
    for w in ["如某机构所言", "据业内人士", "业内人士分析", "机构普遍认为"]:
        chk(f"其他部分未回引辑录节：{w}", w not in head)

    # 节内不得出现评价性表述
    for w in ["切中要害", "已被证实", "已被证伪", "值得关注",
              "观点偏颇", "言之成理", "站不住脚"]:
        chk(f"辑录节无评价性表述：{w}", w not in dg)

    # 节内不得解释涨跌原因
    for w in ["用脚投票", "反映了投资者", "说明市场对", "可见市场"]:
        chk(f"辑录节未解释涨跌原因：{w}", w not in dg)

    # 机构观点各行须含机构、日期与原文途径
    oi = dg.split("<h3>机构观点</h3>")
    if len(oi) >= 2:
        orows = [r for r in re.findall(r"<tr>(.*?)</tr>", oi[1].split("<h3>")[0], re.S)
                 if "<td" in r]
        miss = []
        for i, r in enumerate(orows, 1):
            cells = [c.strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            if len(cells) >= 7 and (not cells[0] or not cells[2] or not cells[6]):
                miss.append(i)
        chk("机构观点各行含机构、日期与原文途径", not miss,
            f"缺项行 {miss}" if miss else f"{len(orows)} 行齐备")


# ---------------------------------------------------------------- 8. 红线
def check_redlines(h):
    """目标价与买卖结论：论证部分禁止，外部观点辑录节及其配套来源行除外

    检查范围取"开头到辑录节之前"，而不是"全文去掉辑录节"。
    原因是数据来源表位于辑录节之后，其中会有辑录节的配套行（例如
    "机构观点与一致预期"一行的数值列写着他人的目标价）。若按后一种
    切法，这些合规的配套行会被判成违规。

    红线管的是论证部分：正文各节不得出现目标价、买卖建议与投资评级。
    """
    scope = h.split('id="digest"')[0] if 'id="digest"' in h else h

    pats = [
        (r"目标价[^\d]{0,5}\d+", "出现目标价"),
        (r"建议\s*(买入|卖出|增持|减持)", "出现买卖建议"),
        (r"评级[：:]\s*(买入|卖出|增持|减持|推荐)", "出现投资评级"),
    ]
    for pat, desc in pats:
        m = re.findall(pat, scope)
        chk(f"论证部分无{desc}", not m, f"{m[:3]}" if m else "")
    if 'id="digest"' in h:
        note("     辑录节及其在数据来源表中的配套行允许照录目标价，已排除在检索之外")


# ---------------------------------------------------------------- 主流程
def main():
    if len(sys.argv) < 2:
        print("用法: python validate-report.py <报告文件.html>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"文件不存在: {path}")
        return 1

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    h = path.read_text(encoding="utf-8")
    print(f"\n=== 研报自检: {path.name} ===\n")

    check_format(h)
    check_interaction(h)
    check_style(h)
    check_charts(h)
    check_bounds(h)
    check_sections(h)
    check_source_table(h)
    check_digest(h)
    check_redlines(h)

    for level, label, extra in LOG:
        if not level:
            print(label)
            continue
        print(f"  [{level}] {label}" + (f"  {extra}" if extra else ""))

    p, w, f = COUNTS["PASS"], COUNTS["WARN"], COUNTS["FAIL"]
    print(f"\n=== 汇总: {p} PASS | {w} WARN | {f} FAIL ===")
    print(f"文件字符数: {len(h)}")
    if f:
        print("存在 FAIL 项，须修复后再交付。")
        return 1
    if w:
        print("存在 WARN 项，请评估是否影响报告质量。")
    else:
        print("全部通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
