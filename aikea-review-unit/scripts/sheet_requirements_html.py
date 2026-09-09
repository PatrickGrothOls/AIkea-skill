"""Scope: Render standalone sheet diagrams with traceable panel IDs and dimensions."""

from html import escape


class SheetRequirementsHtml:
    def render(self, report: dict) -> str:
        stock = report["stock"]
        cards = "".join(self._group(group, stock) for group in report["groups"])
        notes = "".join(f"<li>{escape(note)}</li>" for note in report["assumptions"])
        missing = "".join(f"<li>{escape(path)}</li>" for path in report["oversized_part_paths"])
        heading = "Placed sheets" if missing else "Estimated sheets"
        return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIkea sheet requirements</title><style>
body{{font:16px system-ui;background:#f5f3ee;color:#242c29;margin:24px auto;padding:0 20px;max-width:1200px}}
h1{{font-size:32px}}.sheets{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:24px}}
article{{background:white;padding:18px;border:1px solid #dadbd3;border-radius:8px}}
svg{{width:100%;max-height:540px}}table{{border-collapse:collapse;width:100%;font-size:12px}}
td,th{{text-align:left;border-bottom:1px solid #eee;padding:5px;overflow-wrap:anywhere}}
.note{{padding:16px;background:#ede7d6}}small{{color:#546059}}summary{{cursor:pointer}}
</style><h1>{heading}: {report['sheet_count']}</h1>
<p>{stock['width_mm']:g} × {stock['height_mm']:g} mm · {report['part_count']} panels ·
{stock['edge_margin_mm']:g} mm edge margin · {stock['part_gap_mm']:g} mm spacing ·
90° rotation {'allowed' if stock['allow_rotation'] else 'disabled'}</p>
<div class="note"><strong>{escape(report['status'].title())}</strong><ul>{notes}</ul></div>
{'<h2>Parts that do not fit</h2><ul>' + missing + '</ul>' if missing else ''}
{cards}<p><small>Bounding rectangles show reserved stock, not CNC toolpaths. Open each part list for full source paths.</small></p></html>"""

    def _group(self, group, stock):
        material = escape(group["material_id"] or "Material unspecified")
        cards = "".join(self._sheet(sheet, stock) for sheet in group["sheets"])
        return (f"<h2>{group['thickness_mm']:g} mm — {material}</h2>"
                f"<p>{group['sheet_count']} sheets · {group['part_count']} panels</p>"
                f'<div class="sheets">{cards}</div>')

    def _sheet(self, sheet, stock):
        shapes, rows = [], []
        for index, item in enumerate(sheet["placements"], start=1):
            x, y = item["x_mm"], item["y_mm"]
            width, height = item["width_mm"], item["height_mm"]
            path = escape(item["part"]["path"])
            color = f"hsl({(index * 47) % 360} 30% 80%)"
            shapes.append(f'<g><title>{path}: {width:g} × {height:g} mm</title>'
                          f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}" stroke="#52655b"/>'
                          f'<text x="{x + width / 2}" y="{y + height / 2}" text-anchor="middle" dominant-baseline="middle" font-size="28">{index}</text></g>')
            rows.append(f"<tr><td>{index}</td><td>{path}</td><td>{width:g} × {height:g}</td></tr>")
        return (f"<article><h3>Sheet {sheet['index']}</h3><p>{sheet['rectangle_utilization']:.1%} rectangle coverage</p>"
                f'<svg role="img" aria-label="Sheet {sheet["index"]} panel layout" viewBox="0 0 {stock["width_mm"]} {stock["height_mm"]}">'
                '<rect width="100%" height="100%" fill="#f4e6c8"/>' + "".join(shapes) + '</svg>'
                '<details><summary>Part list</summary><table><tr><th>ID</th><th>Part</th><th>mm</th></tr>'
                + "".join(rows) + '</table></details></article>')
