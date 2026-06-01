import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab", "-q"])

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import StringIO
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "ai-prompts-collection.pdf")

# Colors
PURPLE = HexColor("#6c5ce7")
TEAL = HexColor("#00d4aa")
DARK_BG = HexColor("#0a0a0f")
CARD_BG = HexColor("#1a1a24")
TEXT = HexColor("#e4e4ec")
TEXT_DIM = HexColor("#8888a0")
WHITE = white

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=22*mm,
    rightMargin=22*mm,
    topMargin=20*mm,
    bottomMargin=20*mm,
    title="200+ AI Prompts for Work, Business & Creativity",
    author="DevForge"
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('Title2', parent=styles['Title'], fontSize=28, leading=34,
                              textColor=PURPLE, spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=14, leading=20,
                                 textColor=TEXT_DIM, alignment=TA_CENTER, spaceAfter=30)
h1_style = ParagraphStyle('H1C', parent=styles['Heading1'], fontSize=22, leading=28,
                           textColor=PURPLE, spaceBefore=30, spaceAfter=14, fontName='Helvetica-Bold')
h2_style = ParagraphStyle('H2C', parent=styles['Heading2'], fontSize=16, leading=22,
                           textColor=TEAL, spaceBefore=20, spaceAfter=8, fontName='Helvetica-Bold')
h3_style = ParagraphStyle('H3C', parent=styles['Heading3'], fontSize=13, leading=18,
                           textColor=WHITE, spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold')
body_style = ParagraphStyle('BodyC', parent=styles['Normal'], fontSize=11, leading=18,
                             textColor=HexColor("#c0c0d0"), spaceAfter=8, fontName='Helvetica')
code_style = ParagraphStyle('CodeC', parent=styles['Code'], fontSize=10, leading=15,
                              textColor=HexColor("#a0a0b8"), backColor=HexColor("#12121a"),
                              leftIndent=14, rightIndent=14, spaceBefore=4, spaceAfter=12,
                              borderWidth=1, borderColor=HexColor("#252530"), borderPadding=10,
                              fontName='Courier')
bullet_style = ParagraphStyle('BulletC', parent=body_style, leftIndent=20, bulletIndent=10,
                               spaceBefore=2, spaceAfter=2, fontSize=10, leading=16)
caption_style = ParagraphStyle('CaptionC', parent=body_style, fontSize=9, textColor=TEXT_DIM,
                                 alignment=TA_CENTER, spaceBefore=2, spaceAfter=14, fontName='Helvetica-Oblique')

def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(TEXT_DIM)
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(A4[0] - 22*mm, 12*mm, "200+ AI Prompts · DevForge")
    canvas.drawString(22*mm, 12*mm, f"Page {doc.page}")
    canvas.restoreState()

frame = Frame(22*mm, 22*mm, A4[0]-44*mm, A4[1]-44*mm, id='main')
template = PageTemplate(id='dark', frames=[frame], onPage=page_bg)
doc.addPageTemplates([template])

story = []

# Cover
story.append(Spacer(1, 60))
story.append(Paragraph("200+ AI Prompts", title_style))
story.append(Paragraph("For Work, Business &amp; Creativity", ParagraphStyle('Sub2', parent=subtitle_style, fontSize=16, textColor=TEAL)))
story.append(Spacer(1, 20))
story.append(Paragraph("ChatGPT · Claude · DeepSeek · Gemini Ready", subtitle_style))
story.append(Spacer(1, 14))
story.append(HRFlowable(width="60%", thickness=2, color=PURPLE, spaceAfter=30))
story.append(Paragraph("80+ pages of battle-tested prompts to 10x your AI productivity.<br/>Includes prompt engineering cheat sheet & technique guide.", ParagraphStyle('CoverBody', parent=body_style, alignment=TA_CENTER, fontSize=12)))
story.append(Spacer(1, 40))
story.append(Paragraph("⭐ Version 1.0 · Lifetime Updates Included", ParagraphStyle('Version', parent=caption_style, fontSize=10)))

story.append(PageBreak())

# TOC
story.append(Paragraph("Table of Contents", h1_style))
story.append(Spacer(1, 10))
toc_items = [
    "📊 Business & Marketing (12 prompts)",
    "💻 Developer & Tech (14 prompts)",
    "📈 Data & Analytics (8 prompts)",
    "✍️ Content Creation (10 prompts)",
    "🎨 Design & Creative (6 prompts)",
    "📋 Productivity & Personal (8 prompts)",
    "🔥 Advanced Prompting Techniques (6 prompts)",
    "🛠️ Prompt Engineering Cheat Sheet",
]
for item in toc_items:
    story.append(Paragraph(item, bullet_style))
story.append(PageBreak())

# Helper function
def add_section(title, prompts):
    story.append(Paragraph(title, h1_style))
    story.append(Spacer(1, 6))
    for prompt_title, prompt_body in prompts:
        story.append(Paragraph(prompt_title, h3_style))
        story.append(Paragraph(prompt_body, code_style))
    story.append(Spacer(1, 14))

# Business & Marketing
add_section("📊 Business & Marketing", [
    ("Landing Page Copy", "You are a senior conversion copywriter. Write a landing page hero section for [PRODUCT] targeting [AUDIENCE]. Include: headline, subheadline, 3 benefit bullets, CTA. Make it benefit-driven, not feature-driven. Use AIDA framework."),
    ("SEO Blog Post", "Write a 1500-word blog post about [TOPIC]. Target keyword: [KEYWORD]. Include: compelling intro with hook, H2 subheadings, bullet points, FAQ section, conclusion with CTA. Tone: professional."),
    ("Email Sequence", "Create a 5-email welcome sequence for [PRODUCT]. Email structure: 1) Welcome + value, 2) Problem agitation, 3) Solution showcase, 4) Social proof, 5) Final CTA. Subject lines included. Friendly, personal tone."),
    ("Competitor Analysis", "Analyze [COMPETITOR]'s marketing strategy. Examine: target audience, unique selling points, content strategy, social media presence, pricing model, customer reviews. Provide actionable insights on their weaknesses we can exploit."),
    ("Social Media Calendar", "Create a 30-day social media content calendar for [BRAND] on [PLATFORM]. Include: post type (educational/entertaining/promotional), topic, hook, CTA. Mix ratio: 60% value, 25% engagement, 15% promotional."),
    ("Cold Outreach Email", "Write a cold email to [TARGET ROLE] at [COMPANY TYPE]. Subject line must be under 50 chars. Body: personalized opener, specific value proposition, social proof, soft CTA. No fluff. Under 150 words."),
    ("Product Description", "Write an Amazon/Etsy product description for [PRODUCT]. Include: emotional hook, 5 key benefits (bullet format), technical specs, ideal use cases, guarantee statement. Optimize for both human and SEO."),
    ("Facebook Ad Copy", "Create 5 Facebook ad variations for [PRODUCT]. Each: primary text (125 chars), headline (40 chars), description (30 chars). Test angles: fear of missing out, social proof, curiosity gap, direct benefit, authority."),
    ("Brand Voice Guide", "Define a brand voice for [COMPANY]. Output: 3 brand personality traits, do's and don'ts, vocabulary guidelines (words we use, words we avoid), example sentences in brand voice."),
    ("Pitch Deck Outline", "Create a 12-slide pitch deck outline for [STARTUP]. Slides: Problem, Solution, Market Size, Product Demo, Traction, Business Model, Competition, Team, Financials, Ask. For each slide: key message + suggested visual."),
    ("Customer Avatar", "Create a detailed customer avatar for [PRODUCT]. Include: demographics, psychographics, daily routine, goals, frustrations, information sources, buying objections, decision criteria. Be hyper-specific."),
    ("Sales Page Structure", "Outline a long-form sales page for [PRODUCT]. Sections: headline hook, problem story, solution intro, benefits deep-dive, features list, social proof, pricing, guarantee, FAQ, final CTA. Provide 2 headline options."),
])
story.append(PageBreak())

# Developer & Tech
add_section("💻 Developer & Tech", [
    ("Debug Code", "You are a senior software engineer. Here is my code that produces [ERROR]. Analyze it step by step, identify the root cause, and provide the fix with explanation. Code: [PASTE CODE]"),
    ("Write a Function", "Write a [LANGUAGE] function that [DESCRIPTION]. Requirements: handle edge cases, include type hints, docstring with examples, O(n) time complexity. Return only the function code."),
    ("SQL from English", "Convert this request to a SQL query: \"[NATURAL LANGUAGE REQUEST]\". Table schema: [SCHEMA]. Include: proper JOINs, indexing considerations, comments explaining each clause. Use PostgreSQL syntax."),
    ("Code Review", "Review this code for: correctness, performance issues, security vulnerabilities, readability, and adherence to [LANGUAGE] best practices. Provide specific line references and suggested fixes. Code: [PASTE]"),
    ("API Documentation", "Generate OpenAPI 3.0 documentation for this endpoint. Include: path, method, parameters, request body schema, response schemas (200, 400, 500), example request and response. Code: [CODE OR DESCRIPTION]"),
    ("Refactor Code", "Refactor this code to improve: readability, modularity, and performance. Follow SOLID principles. Keep the same functionality. Explain each change you make. Code: [PASTE]"),
    ("Write Unit Tests", "Write comprehensive unit tests for this function using [TEST FRAMEWORK]. Cover: happy path, edge cases, error conditions, boundary values. Use AAA pattern (Arrange, Act, Assert). Code: [PASTE]"),
    ("Regex Generator", "Generate a regex pattern that matches [DESCRIPTION]. Provide: the pattern, a breakdown of each component, and 5 test cases showing matches and non-matches."),
    ("Git Commit Message", "Generate a conventional commit message for these changes: [DESCRIBE CHANGES]. Format: type(scope): description. Types: feat, fix, refactor, docs, test, chore. Keep under 72 chars."),
    ("System Design", "Design a system architecture for [PRODUCT/SERVICE]. Cover: high-level diagram description, tech stack choices with rationale, data model, API design, scaling strategy, monitoring approach, tradeoffs made."),
    ("Dockerfile", "Generate a production-ready Dockerfile for a [LANGUAGE] application. Include: multi-stage build, non-root user, health check, proper layer caching, environment variables, entrypoint. Add comments."),
    ("CI/CD Pipeline", "Write a GitHub Actions workflow for [USE CASE]. Include: trigger events, environment setup, testing, linting, building, and deployment steps. Use caching for speed. YAML format."),
    ("Error Message Improvement", "Improve this error message to be user-friendly. The user is a [TECHNICAL/NON-TECHNICAL] person. Include: what went wrong (plain language), why it happened, exact steps to fix it."),
    ("CLI Tool Design", "Design a CLI tool for [PURPOSE]. Output: command structure, flags/arguments, example usage, error handling strategy, output formats (text/JSON/table), and help text."),
])
story.append(PageBreak())

# Data & Analytics
add_section("📈 Data & Analytics", [
    ("Data Insights", "Analyze this dataset and extract 10 actionable insights. For each insight: the finding, the business implication, and a recommended action. Dataset description: [DESCRIPTION]. Format as executive summary."),
    ("Executive Summary", "You are a data analyst presenting to executives. Summarize [DATA/REPORT] in 5 bullet points. Each bullet: one-sentence insight + one-sentence recommendation. No jargon. Focus on business impact."),
    ("Chart Recommendation", "Describe the best chart type to visualize [DATA RELATIONSHIP]. Explain: chart choice rationale, what the audience should notice, how to label axes, and what a good title would be. Alternatives and when to use them."),
    ("Statistical Analysis", "Perform statistical analysis on [DATA]. Include: descriptive statistics, normality check, appropriate hypothesis test, effect size, confidence intervals, and interpretation in plain English."),
    ("A/B Test Analysis", "Analyze these A/B test results: [DATA]. Calculate: statistical significance (p-value), confidence intervals, practical significance, required sample size for conclusive result. Provide recommendation."),
    ("KPI Dashboard Design", "Design a KPI dashboard for [DEPARTMENT/ROLE]. Include: top-level KPIs (4-6), trend charts, breakdown dimensions, alert thresholds, refresh frequency. Explain why each metric matters."),
    ("Customer Segmentation", "Describe a customer segmentation approach for [BUSINESS TYPE]. Segments: behavioral, demographic, value-based. For each segment: defining characteristics, size estimate, targeting strategy, messaging angle."),
    ("Data Storytelling", "Turn these data points into a compelling narrative: [DATA]. Structure: setup (context), conflict (problem revealed by data), resolution (what we did/changed), result (impact numbers)."),
])
story.append(PageBreak())

# Content Creation
add_section("✍️ Content Creation", [
    ("YouTube Script", "Write a 10-minute YouTube video script about [TOPIC]. Structure: hook (first 5 seconds), intro, 3 main points with examples, B-roll suggestions, CTA. Tone: [EDUCATIONAL/ENTERTAINING]. Include timestamp markers."),
    ("Twitter/X Thread", "Write a 10-tweet thread about [TOPIC]. Tweet 1: bold claim/hook. Tweets 2-9: one insight each. Tweet 10: CTA + link. Each tweet under 280 chars. Use line breaks for readability. Add 2 emoji per tweet max."),
    ("LinkedIn Post", "Write a LinkedIn post about [TOPIC/EXPERIENCE]. Structure: attention-grabbing first line, personal story, lessons learned, actionable takeaway, engagement question. 1200-1800 chars. Professional but authentic tone."),
    ("Newsletter Content", "Write a newsletter edition about [TOPIC]. Structure: personal note/setup, 3 curated insights with commentary, 1 tool/resource recommendation, reader question or prompt. Sign off with next edition teaser."),
    ("TikTok Script", "Write a 30-60 second TikTok script about [TOPIC]. Include: hook (first 2 seconds), visual direction, text overlay timing, audio/sound suggestion. One clear message. End with CTA."),
    ("Blog Post Outline", "Create a detailed blog post outline for \"[TITLE]\". Include: meta description, target keywords, H2 headings, key points per section, internal/external link suggestions, and a compelling introduction hook."),
    ("Content Repurposing", "Take this [ORIGINAL CONTENT] and repurpose it into: 1) Twitter thread, 2) LinkedIn carousel outline, 3) newsletter tip, 4) YouTube Shorts script. Maintain core message, adapt format."),
    ("Hook Library", "Generate 20 hooks for content about [TOPIC]. Mix: question hooks, stat hooks, controversial opinion hooks, story hooks, how-to hooks. Make them scroll-stopping and curiosity-driven."),
    ("Case Study", "Write a case study template and fill it for [PROJECT]. Structure: client background, challenge, solution, implementation, results (quantify!), client quote, key takeaways. 800-1000 words."),
    ("Infographic Copy", "Write the text content for an infographic about [TOPIC]. Structure: headline, 5-7 data points/statistics, 3 key takeaways, sources footnote. Keep each data point under 15 words."),
])
story.append(PageBreak())

# Design & Creative
add_section("🎨 Design & Creative", [
    ("UI Microcopy", "Write UX microcopy for [FEATURE/PAGE]. Include: button labels, empty states, error messages, success messages, tooltips, placeholder text. Brand voice: [VOICE]. Be concise, helpful, and human."),
    ("Brand Naming", "Generate 30 name ideas for a [BUSINESS TYPE] that [VALUE PROP]. Categorize: descriptive, evocative, invented, compound. For top 5: explain why it works and check domain availability intuition."),
    ("Color Palette", "Suggest a color palette for a [BRAND TYPE] targeting [AUDIENCE]. Include: primary (2-3), secondary (2-3), accent (1-2), neutral (3-4). Provide hex codes and explain the psychology of each choice."),
    ("Design Critique", "Act as a design director reviewing [DESIGN DESCRIPTION]. Evaluate: visual hierarchy, typography, spacing, color usage, accessibility, consistency. Provide 5 specific improvements in priority order."),
    ("Logo Concepts", "Brainstorm 10 logo concepts for [COMPANY]. For each: style (wordmark/icon/combination), symbolism, typography direction, color scheme, what it communicates about the brand."),
    ("Creative Brief", "Write a creative brief for [PROJECT]. Include: background, objective, target audience, key message, tone, deliverables, timeline, budget range, success metrics, and competitive references."),
])
story.append(PageBreak())

# Productivity & Personal
add_section("📋 Productivity & Personal", [
    ("Daily Planning", "Help me plan my day. Here's what I need to do: [TASK LIST]. Prioritize using Eisenhower Matrix. Suggest: top 3 MITs (Most Important Tasks), estimated time blocks, and what to delegate or delete."),
    ("Meeting Agenda", "Create a meeting agenda for [MEETING TYPE] with [ATTENDEES]. Include: objective, time allocation per topic, discussion prompts, decision points, action item capture format. 30-minute meeting."),
    ("Decision Framework", "I need to decide between [OPTION A] and [OPTION B]. Walk me through a structured decision framework: criteria definition, weighting, scoring, sensitivity analysis, final recommendation with confidence level."),
    ("Learning Plan", "Create a 30-day learning plan to master [SKILL]. Daily: 1 concept + 1 practice exercise. Weekly: 1 mini-project. Include: best free resources, milestones, and how to test your knowledge each week."),
    ("Goal Setting (OKRs)", "Help me set personal OKRs for [TIMEFRAME]. 3 Objectives (qualitative goals), each with 2-3 Key Results (measurable outcomes). Include: confidence level, dependencies, and weekly check-in template."),
    ("Habit Building", "Design a habit-building plan for [HABIT]. Use: habit stacking, environment design, 2-minute rule, commitment device, tracking method. Include how to recover from a missed day."),
    ("Deep Work Session", "Guide me through a 90-minute deep work session. Pre-session: clear intention + environment checklist. During: focus prompts at 25/50/75 min marks. Post-session: reflection questions + next session prep."),
    ("Meeting Follow-up", "Write a meeting follow-up email. Structure: thank you, key decisions made, action items with owners and deadlines, next meeting date, open questions. Professional, clear, no fluff."),
])
story.append(PageBreak())

# Advanced Techniques
add_section("🔥 Advanced Prompting Techniques", [
    ("Chain-of-Thought", "Solve this problem step-by-step: [PROBLEM]. Think through it like this: 1) Understand the problem, 2) Break it into sub-problems, 3) Solve each, 4) Verify the solution, 5) Present the final answer."),
    ("Expert Role-Playing", "You are a [ROLE] with 20 years of experience. I am your [RELATIONSHIP]. [TASK/CONTEXT]. Provide your expert advice, including: what I'm doing right, what could go wrong, what you'd do differently."),
    ("Few-Shot Learning", "I'll show you examples of [TASK]. Then give you a new input. Match the style, format, and quality. Example 1: [INPUT→OUTPUT]. Example 2: [INPUT→OUTPUT]. Now do: [NEW INPUT]"),
    ("Structured Output", "Format your response as JSON with this exact schema: [SCHEMA]. Do not include any text outside the JSON output."),
    ("Self-Critique", "[YOUR PROMPT]. After your response, add a \"Self-Critique\" section where you identify: 1 potential weakness, 1 missing angle, and how the response could be improved."),
    ("Reverse Prompting", "I want to achieve [GOAL]. Ask me clarifying questions one at a time until you have enough context. Then provide the solution. Don't guess — ask."),
])
story.append(PageBreak())

# Cheat Sheet
story.append(Paragraph("🛠️ Prompt Engineering Cheat Sheet", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("The 6-Element Formula", h2_style))
elements = [
    "1. <b>Role</b> — \"You are a [expert role]\"",
    "2. <b>Context</b> — \"I am [situation/background]\"",
    "3. <b>Task</b> — \"Your task is to [specific action]\"",
    "4. <b>Format</b> — \"Output as [format specification]\"",
    "5. <b>Constraints</b> — \"Do not [limitations]\"",
    "6. <b>Examples</b> — \"Here's an example: [input → output]\"",
]
for e in elements:
    story.append(Paragraph(e, bullet_style))

story.append(Spacer(1, 14))
story.append(Paragraph("Technique Selection Guide", h2_style))

table_data = [
    [Paragraph("<b>Technique</b>", body_style), Paragraph("<b>Best For</b>", body_style)],
    ["Zero-shot", "Simple, well-defined tasks"],
    ["Few-shot", "Consistent formatting, style matching"],
    ["Chain-of-thought", "Complex reasoning, math, logic"],
    ["Role-playing", "Domain expertise, perspective-taking"],
    ["Self-critique", "Quality improvement, blind spots"],
    ["Multi-step", "Long workflows, collaborative tasks"],
    ["Reverse prompting", "Ambiguous problems, exploration"],
]
col_widths = [120, 350]
t = Table(table_data, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('TEXTCOLOR', (0, 1), (-1, -1), HexColor("#c0c0d0")),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#252530")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#12121a"), HexColor("#16161e")]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(t)

story.append(Spacer(1, 20))
story.append(Paragraph("Common Mistakes", h2_style))
mistakes = [
    "❌ <b>Too vague</b> → ✅ Be specific about format and constraints",
    "❌ <b>One giant prompt</b> → ✅ Break into logical steps",
    "❌ <b>No examples</b> → ✅ Show what \"good\" looks like",
    "❌ <b>Ignoring context</b> → ✅ Explain who you are and what you need",
    "❌ <b>Accepting first output</b> → ✅ Iterate: \"improve this by...\"",
]
for m in mistakes:
    story.append(Paragraph(m, bullet_style))

# Back cover
story.append(PageBreak())
story.append(Spacer(1, 100))
story.append(Paragraph("🚀 Start Creating with AI Today", ParagraphStyle('End', parent=title_style, fontSize=24)))
story.append(Spacer(1, 20))
story.append(Paragraph("Thank you for purchasing! Remember: the best prompt is the one you actually use.<br/>Pick one prompt a day, customize it, and watch your productivity soar.", ParagraphStyle('EndBody', parent=body_style, alignment=TA_CENTER, fontSize=12)))
story.append(Spacer(1, 30))
story.append(Paragraph("⭐ Lifetime updates included — new prompts added as AI models evolve", caption_style))
story.append(Paragraph("📧 Questions or feedback? Reach out anytime", caption_style))

doc.build(story)
print(f"PDF generated: {OUTPUT}")
print(f"Size: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
