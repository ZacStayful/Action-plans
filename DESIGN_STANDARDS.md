# Stayful Action Plan — Design Standards

## Hero — LOCKED DESIGN (do not change)

Three zones, always in this order:

### Zone A — Top bar
- Logo in **white pill container**: `background:white; border-radius:10px; padding:6px 12px; img height:38px`
- Logo src: always base64-embedded from `Screenshot_20240625_at_09_57_03.png`
- Right: "Stayful" bold + "Short-Let Management" small-caps, 65% opacity
- `border-bottom: 1px solid rgba(255,255,255,0.12)`

### Zone B — Hero body
- Eyebrow: "Income Action Plan · Confidential"
- **Property address/description as the BIG headline** (32px, 800 weight) — never a generic title
- Location line with 📍 icon
- "Prepared exclusively for **[Name]** · [Date]"
- Three stat panels: Year 1 Net | Year 2+ Net | % uplift vs previous income

### Zone C — Pills strip
- `border-top: 1px solid rgba(255,255,255,0.1)`
- Pills: beds, property type, profile, key dates

### Hero CSS
```css
.hero {
  background: linear-gradient(140deg, #2a3f26 0%, #3d5c38 45%, #5d8156 100%);
  border-radius: 0 0 24px 24px;
  color: white;
  margin-bottom: 32px;
  overflow: hidden;
}
```

---

## Management Agreement Section — MANDATORY EVERY RUN

Always include both links as CTA cards:
- **Agreement PDF**: https://drive.google.com/file/d/1ct_Br_7XR69s6beyFfqHSnSPoRouKkG6/view?usp=sharing
- **Walkthrough Video**: https://www.loom.com/share/50756d81baf4426987cb5300ecbee951

---

## Setup Quote PDF — Non-overlapping header

The `right_block` in `stayful_quote_generator.py` MUST use separate rows with explicit heights:

```python
right_block = Table(
    [
        [Paragraph("SETUP QUOTE", ...)],   # row 0
        [Spacer(1, 3*mm)],                  # row 1 — gap
        [Paragraph(f"Ref: {ref}", ...)],    # row 2
        [Paragraph(f"Date: {date}", ...)],  # row 3
    ],
    colWidths=[W * 0.52],
    rowHeights=[12*mm, 3*mm, 6*mm, 6*mm],  # EXPLICIT — prevents overlap
)
```

**Never** combine Ref and Date into a single `Paragraph` — they will overlap.

---

## Constants

| Item | Value |
|------|-------|
| Management Agreement | https://drive.google.com/file/d/1ct_Br_7XR69s6beyFfqHSnSPoRouKkG6/view?usp=sharing |
| Walkthrough Video | https://www.loom.com/share/50756d81baf4426987cb5300ecbee951 |
| Brand colour | `#5d8156` |
| Hero gradient | `linear-gradient(140deg, #2a3f26 0%, #3d5c38 45%, #5d8156 100%)` |
| Body background | `#f0ede8` |
| Live URL pattern | `https://action-plans-theta.vercel.app/[slug]-action-plan.html` |
