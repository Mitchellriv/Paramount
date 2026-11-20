r"""
Fill the Preferred Materials "Notice to Owner - Information Sheet",
form revision Rev-10.06.26 (sent by Preferred's NTO desk on 2026-11-20).

The older form revisions (REV. 04.29.24 and the one before it) use a
different layout. Their coordinates do not work on this form. Don't reuse them.

The blank has no AcroForm fields. This script adds editable text widgets,
plus drawn X marks for the checkboxes (the boxes on the form are images,
not form fields).

Usage:
    from fill_preferred_nto import fill_preferred_nto
    fill_preferred_nto(data, "EST28748_ProRealty_PREFERRED_NTO_PREFERREDALICO.pdf")

Keys in `data` are all optional. Leave out or use '' for anything unknown.
Never guess Owner or GC.
  account, company (default Paramount), invoice, po, date
  job_1, job_2, job_3              1. Job name / address (DOT FIN# goes here if it's a DOT job)
  working_for_1..3                 2. Entity you are working for: name / address / contact & tel
  gc_1..3                          3. General Contractor: name / address / tel
  owner_1..3                       4. Property owner: name / address / tel
  bonded                           5. 'YES' | 'NO' | 'UNKNOWN'
  bond_1..3                        6. Bonding/surety company: name / address / tel, bond #
  noc_1..3                         7. NOC Instr# / Book/Page / County
  material                         'asphalt' (default) | 'concrete' | 'aggregate'
  qty_tons                         "Approx." is added automatically. This revision no
                                   longer has the pre-printed "aprx." label.
  mix_type, pickup_date, plant_location
"""
import os
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
BLANK_PATH = os.path.join(HERE, "assets", "PREFERRED_BLANK_NTO_FORM_Rev-10.06.26.pdf")
FORM_REV = "Rev-10.06.26"

# (x0, x1, underline_y). Every value sits on its underline. Measured from the
# vector lines in the Rev-10.06.26 blank. Points, top-left origin, page 612x792.
R = (341, 588)  # x-range of the right-hand answer lines, sections 1-7
FIELDS = {
    "account":        (141, 214, 125.0),
    "company":        (141, 571, 138.1),
    "invoice":        (66, 185, 150.5),
    "po":             (272, 381, 150.5),
    "date":           (456, 588, 150.5),
    "job_1": (*R, 176.3), "job_2": (*R, 190.0), "job_3": (*R, 203.6),
    "working_for_1": (*R, 228.8), "working_for_2": (*R, 242.5), "working_for_3": (*R, 256.2),
    "gc_1": (*R, 281.4), "gc_2": (*R, 295.1), "gc_3": (*R, 308.8),
    "owner_1": (*R, 334.0), "owner_2": (*R, 347.6), "owner_3": (*R, 361.3),
    "bond_1": (*R, 413.3), "bond_2": (*R, 427.0), "bond_3": (*R, 440.6),
    "noc_1": (*R, 465.8), "noc_2": (*R, 479.5), "noc_3": (*R, 493.2),
    "qty_tons":       (115, 185, 556.6),
    "mix_type":       (238, 339, 556.6),
    "pickup_date":    (456, 572, 556.6),
    "plant_location": (271, 455, 578.9),
}

# Checkbox centres (points). The boxes are embedded images, located by rendering
# at 8x and measuring each 7x7pt box.
CHECKBOXES = {
    "asphalt":   (56.1, 531.5),
    "concrete":  (178.9, 531.5),
    "aggregate": (333.3, 531.5),
    "YES":       (352.2, 383.2),
    "NO":        (400.2, 383.2),
    "UNKNOWN":   (444.3, 382.9),
}

DEFAULT_COMPANY = "Paramount Asphalt & Sealcoating Corp."


def _x(page, key, half=3.2):
    cx, cy = CHECKBOXES[key]
    for a, b in (((cx - half, cy - half), (cx + half, cy + half)),
                 ((cx + half, cy - half), (cx - half, cy + half))):
        page.draw_line(fitz.Point(*a), fitz.Point(*b), color=(0, 0, 0), width=1.1)


def fill_preferred_nto(data, output_path, blank_path=BLANK_PATH):
    data = dict(data)
    data.setdefault("company", DEFAULT_COMPANY)
    q = str(data.get("qty_tons", "")).strip()
    if q and not q.lower().startswith(("approx", "aprx")):
        data["qty_tons"] = "Approx. " + q

    doc = fitz.open(blank_path)
    page = doc[0]
    for key, (x0, x1, line_y) in FIELDS.items():
        value = str(data.get(key, "") or "").strip()
        if not value:
            continue
        w = fitz.Widget()
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.field_name = key
        w.field_value = value
        w.rect = fitz.Rect(x0, line_y - 11.5, x1, line_y - 0.5)
        # Shrink long values so they fit on their line instead of being clipped.
        tw = fitz.get_text_length(value, fontname="helv", fontsize=8)
        w.text_fontsize = 8 if tw <= (x1 - x0 - 4) else max(5, 8 * (x1 - x0 - 4) / tw)
        w.text_font = "Helv"
        w.border_width = 0
        w.fill_color = None
        w.border_color = None
        page.add_widget(w)

    _x(page, {"concrete": "concrete", "aggregate": "aggregate"}.get(
        str(data.get("material", "asphalt")).lower(), "asphalt"))
    bonded = str(data.get("bonded", "")).upper()
    if bonded in ("YES", "NO", "UNKNOWN"):
        _x(page, bonded)

    doc.save(output_path, garbage=3, deflate=True)
    doc.close()
    return output_path
