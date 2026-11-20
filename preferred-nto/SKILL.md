---
name: preferred-nto
description: >
  Paramount Asphalt & Sealcoating — Preferred Materials NTO (Notice to Owner) Information Sheet.
  Use whenever Mitch needs a Preferred NTO, says "make the Preferred NTO", "NTO for this job"
  on a job whose plant is PREFERRED (Naples, Alico, Nokomis, etc.), or uploads a Preferred
  blank NTO. Uses Preferred's current form, Asphalt NTO Form Rev-10.06.26.
---

# Preferred Materials NTO Form — Fill Skill (Rev-10.06.26)

## OVERVIEW

Fill Preferred Materials' **Notice to Owner – Information Sheet**, form revision **Rev-10.06.26**.
Jennifer Neinast (NTO Specialist) sent this revision on 11/20/2026 as the form to use from now on.
Preferred said only one of their two files needs to be completed. We use the PDF. The XLSX
version is not used.

**Blank form (bundled):** `assets/PREFERRED_BLANK_NTO_FORM_Rev-10.06.26.pdf`
**Filler script (bundled):** `fill_preferred_nto.py`. Always use it. Don't re-measure coordinates.

**Retired, do not use:** `REV. 04.29.24`, the older "Working for? / Plat Book / Section / RGE"
layout, and any coordinate table from earlier versions of this skill. Those coordinates do not
line up with this form.

**Email completed form to:** pminoticetoowner@preferredmaterials.com
**Attach the Bond and/or NOC copy to the same email if we have it.** The new form asks for this
in its yellow banner.

**Paramount info (never ask Mitch):** Company = Paramount Asphalt & Sealcoating Corp. (filled automatically)

---

## FIELDS ON REV-10.06.26

| # | Section | `data` keys | Notes |
|---|---------|-------------|-------|
| Header | Account # / Company / Invoice # / PO / Date | `account`, `company`, `invoice`, `po`, `date` | PO = `EST #####`. Date = today. Leave Invoice # and Account # blank unless known. Leave **IDENTIFIER #** blank (Preferred's internal number). |
| 1 | Job Name / Address | `job_1`, `job_2`, `job_3` | `job_1` = "EST ##### Job Name", `job_2` = street, city, FL zip, `job_3` = county (or **DOT FIN# / Contract #** for FDOT jobs). |
| 2 | Entity we're working for | `working_for_1..3` | Name / address / "Tel: … Email: …" |
| 3 | General Contractor | `gc_1..3` | Fill only if a GC exists and differs from #2. Never guess. |
| 4 | Property Owner | `owner_1..3` | Owner of record. Always look it up (county appraiser / floridaparcels.com). Never use the GC or the management company. |
| 5 | Is this job BONDED? | `bonded` = `YES` / `NO` / `UNKNOWN` | Required. Use `UNKNOWN` if not confirmed. **Public owners** (county, city, school district, tribe, state) are often bonded, so ask Mitch before choosing `UNKNOWN` on those. |
| 6 | Bonding/Surety Company + BOND # | `bond_1..3` | Only if known. |
| 7 | NOC Instr# / Book/Page / County | `noc_1..3` | Only if known. |
| Material | Hot Mix Asphalt checkbox | `material` (default `asphalt`) | The X is drawn automatically. |
| Qty / Type / Pick up date | `qty_tons`, `mix_type`, `pickup_date` | The script adds **"Approx."** in front of tons. This revision has no pre-printed "aprx." label. Pickup date = **first paving day on the calendar**. |
| Plant | `plant_location` | e.g. `Preferred Materials - Naples`, `- Alico`, `- Nokomis` |

---

## WORKFLOW

1. Pull job info from the calendar event (JOB NAME, ADDRESS, COMPANY, CONTACT, PLANT ORDER, first DAY date).
2. Look up the property owner of record.
3. Ask Mitch about **Bonded** only for public-owner jobs. Otherwise use `UNKNOWN`.
4. Run the filler:

```python
import sys; sys.path.insert(0, "<this skill dir>")
from fill_preferred_nto import fill_preferred_nto

fill_preferred_nto({
    "po": "EST 28748", "date": "11/20/2026",
    "job_1": "EST 28748 Pro Realty and Development",
    "job_2": "483 E. Cowboy Way, Labelle, FL",
    "working_for_1": "Pro Realty and Development",
    "working_for_3": "Tel: 239-222-0516",
    "owner_1": "HENDRY COUNTY BOCC", "owner_2": "PO BOX 1760, Labelle, FL 33975",
    "bonded": "UNKNOWN",
    "qty_tons": "291.6", "mix_type": "SP9.5R", "pickup_date": "01/12/2027",
    "plant_location": "Preferred Materials - Alico",
}, "/mnt/user-data/outputs/EST28748_ProRealtyandDevelopment_PREFERRED_NTO_PREFERREDALICO.pdf")
```

5. Render page 1 to PNG and look at it before handing it over. Every value should sit on its
   underline. Long values shrink automatically.
6. Save the PDF to the NTO Drive folder and remind Mitch to email it to pminoticetoowner@preferredmaterials.com,
   with the Bond/NOC copy attached if available.

**If a job is rescheduled after its NTO was made:** regenerate the NTO with the new pickup date.
Don't leave a stale date on file.

---

## OUTPUT FILE NAMING

`EST[number]_[JobName]_PREFERRED_NTO_PREFERRED[PLANT].pdf`

Example: `EST28748_ProRealtyandDevelopment_PREFERRED_NTO_PREFERREDALICO.pdf`
