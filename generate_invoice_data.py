import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta
import os

# CONFIGURATION
n_total = 45514
n_customers = 400

# ROtype splits (adjusted to sum to 1.00)
split_counter = 0.57
split_resale = 0.2795
split_trailer = 0.129
split_truck = 0.0215

n_counter = int(n_total * split_counter)
n_resale = int(n_total * split_resale)
n_trailer = int(n_total * split_trailer)
n_truck = n_total - (n_counter + n_resale + n_trailer)  # Adjust for rounding

rotype_pool = (["COUNTER"] * n_counter +
               ["RESALE"] * n_resale +
               ["TRAILER"] * n_trailer +
               ["TRUCK"] * n_truck)
random.shuffle(rotype_pool)

locations = [
    ("New York", ["NY1", "NY2", "NY3", "NY4"]),
    ("Chicago", ["CH1", "CH2", "CH3", "CH4"]),
    ("Green Bay", ["GB1", "GB2", "GB3", "GB4"]),
    ("Los Angeles", ["LA1", "LA2", "LA3", "LA4"]),
    ("Dallas", ["DL1", "DL2", "DL3", "DL4"]),
    ("Boulder", ["BL1", "BL2", "BL3", "BL4"])
]
depts = [10, 20, 30, 40, 50]

def fake_cust_name():
    first = random.choice(["Acme", "Summit", "Evergreen", "Pioneer", "Liberty", "Unity", "Synergy",
                           "Paramount", "Keystone", "Aurora", "Sunset", "Stonegate", "Oakwood", "Sterling", "Goldstar"])
    last = random.choice(["Industries", "Logistics", "Corp", "Solutions", "Partners", "Systems", "Group",
                          "Transfer", "Associates", "Tucking", "Global", "Resources", "LLC", "Inc", "Truck Lines"])
    return f"{first} {last}"

def fake_cust_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.choice([5,6])))

def get_business_days(start, end):
    holidays = [
        "2022-01-01", "2022-05-30", "2022-07-04", "2022-09-05", "2022-11-24", "2022-12-26",
        "2023-01-02", "2023-05-29", "2023-07-04", "2023-09-04", "2023-11-23", "2023-12-25",
        "2024-01-01", "2024-05-27", "2024-07-04", "2024-09-02", "2024-11-28", "2024-12-25",
        "2025-01-01", "2025-05-26", "2025-07-04", "2025-09-01", "2025-11-27", "2025-12-25"
    ]
    holidays = [datetime.strptime(day, "%Y-%m-%d") for day in holidays]
    business_days = []
    current = start
    while current <= end:
        if current.weekday() < 5 and current not in holidays:
            business_days.append(current)
        current += timedelta(days=1)
    return business_days

def weighted_dates(business_days):
    by_month = {}
    for d in business_days:
        key = (d.year, d.month)
        by_month.setdefault(key, []).append(d)
    weighted = []
    for k, days in by_month.items():
        n = len(days)
        cutoff = days[-7:]
        rest = days[:-7]
        end_count = int(n * 0.38)
        normal_count = n - end_count
        weighted.extend(random.choices(cutoff, k=end_count))
        weighted.extend(random.choices(rest, k=normal_count))
    random.shuffle(weighted)
    return weighted

random.seed(42)
np.random.seed(42)

print("Generating business days...")
business_days = get_business_days(datetime(2022,1,1), datetime(2025,6,30))
print(f"Number of business days: {len(business_days)}")
weighted_days = weighted_dates(business_days)
print("Business days weighted.")

# 80/20 CUSTOMER ALLOCATION
top_count = int(n_customers * 0.2)
bot_count = n_customers - top_count
big_invoices = int(n_total * 0.8)
small_invoices = n_total - big_invoices

big_invoice_counts = np.random.multinomial(big_invoices, np.random.dirichlet(np.ones(top_count)))
small_invoice_counts = np.random.multinomial(small_invoices, np.random.dirichlet(np.ones(bot_count)))
invoice_counts = np.concatenate([big_invoice_counts, small_invoice_counts])

print(f"Generating {n_customers} customer profiles...")
customer_profiles = []
used_names = set()
used_ids = set()
for i in range(n_customers):
    attempts = 0
    while True:
        cname = fake_cust_name()
        if cname not in used_names:
            used_names.add(cname)
            break
        attempts += 1
        if attempts > 20:
            break

    attempts = 0
    while True:
        cid = fake_cust_no()
        if cid not in used_ids:
            used_ids.add(cid)
            break
        attempts += 1
        if attempts > 20:
            break

    # Assign customer-level persistent modifiers (updated as requested)
    profile = {
        "CustName": cname,
        "CustNo": cid,
        "is_big": i < top_count,
        "labor_gm_mod": np.random.normal(0, 0.08),   # More variance
        "parts_gm_mod": np.random.normal(0, 0.065),  # Less variance
        "efficiency_mod": np.random.normal(0, 0.2),  # More variance (applies as a percentage)
        "parts_bias": np.random.normal(0, 60),
        "resale_bias": np.random.normal(0, 0.11)
    }
    customer_profiles.append(profile)

    if i % 50 == 0:
        print(f"Generated {i} of {n_customers} customer profiles")

print("All customer profiles generated.")

print("Generating invoices...")
rows = []
inv_n = 100000
loc_whse_flat = [(l, w) for l, ws in locations for w in ws]

# KPI ranges for locations (these are base means, actual per-invoice can vary)
kpi_ranges = {
    "efficiency": {"low": (60, 90), "avg": (96, 105), "high": (109, 145)},
    "labor_gm": {"low": (0.48, 0.59), "avg": (0.62, 0.70), "high": (0.73, 0.85)},
    "parts_gm": {"low": (0.15, 0.25), "avg": (0.31, 0.39), "high": (0.41, 0.49)},
    "cycle": {"fast": (1, 4), "avg": (5, 7.5), "slow": (8, 30)}
}

loc_profile = {}
wh_profile = {}

for loc, whs in locations:
    eff_tier = np.random.choice(list(kpi_ranges["efficiency"].keys()))
    lab_gm_tier = np.random.choice(list(kpi_ranges["labor_gm"].keys()))
    parts_gm_tier = np.random.choice(list(kpi_ranges["parts_gm"].keys()))
    cycle_tier = np.random.choice(list(kpi_ranges["cycle"].keys()))
    loc_profile[loc] = {
        "efficiency": np.random.uniform(*kpi_ranges["efficiency"][eff_tier]),
        "labor_gm": np.random.uniform(*kpi_ranges["labor_gm"][lab_gm_tier]),
        "parts_gm": np.random.uniform(*kpi_ranges["parts_gm"][parts_gm_tier]),
        "cycle": np.random.uniform(*kpi_ranges["cycle"][cycle_tier])
    }
    for wh in whs:
        wh_profile[(loc, wh)] = {
            "efficiency": max(60, min(140, loc_profile[loc]["efficiency"] + np.random.normal(0, 13))),
            "labor_gm": min(0.91, max(0.33, loc_profile[loc]["labor_gm"] + np.random.normal(0, 0.06))),
            "parts_gm": min(0.61, max(0.09, loc_profile[loc]["parts_gm"] + np.random.normal(0, 0.07))),
            "cycle": max(1.2, loc_profile[loc]["cycle"] + np.random.normal(0, 2.1))
        }

print("All warehouse and location profiles generated.")

for i, prof in enumerate(customer_profiles):
    if i % 50 == 0:
        print(f"Generating invoices for customer {i} of {len(customer_profiles)}")
    n_cust_invoices = invoice_counts[i]
    whse_sample = random.choices(loc_whse_flat, k=n_cust_invoices)
    # Customer-level ROtype bias for job mix
    customer_rotype_bias = prof["resale_bias"]
    # Compute job mix per customer (respecting company-level splits, but allowing some individual swing)
    rotype_dist = np.array([
        split_counter - customer_rotype_bias,  # COUNTER
        split_resale + customer_rotype_bias,   # RESALE
        split_trailer + np.random.normal(0, 0.02),  # TRAILER, slight variation
        split_truck + np.random.normal(0, 0.005)    # TRUCK, slight variation
    ])
    # Normalize to sum to 1 (may slightly distort company-level ratio, but adds realism)
    rotype_dist = np.clip(rotype_dist, 0, 1)
    rotype_dist = rotype_dist / rotype_dist.sum()
    rotypes_for_customer = np.random.choice(
        ["COUNTER", "RESALE", "TRAILER", "TRUCK"],
        size=n_cust_invoices,
        p=rotype_dist
    )

    for idx in range(n_cust_invoices):
        loc, wh = whse_sample[idx]
        dept = random.choice(depts)
        rotype = rotypes_for_customer[idx]
        kpi = wh_profile[(loc, wh)]
        # Apply customer modifiers
        labor_gm_mod = prof["labor_gm_mod"]
        parts_gm_mod = prof["parts_gm_mod"]
        efficiency_mod = prof["efficiency_mod"]
        parts_bias = prof["parts_bias"]

        inv_date = random.choice(weighted_days)
        if rotype == "COUNTER":
            hours_worked = 0
            hours_billed = 0
            labor_worked = 0
            labor_billed = 0
            parts_cost = round(np.random.uniform(18 + parts_bias, 1100 + parts_bias), 2)
            row_parts_gm = np.clip(np.random.normal(kpi["parts_gm"] + parts_gm_mod, 0.10), 0.10, 0.60)
            parts_sales = round(parts_cost / (1 - row_parts_gm), 2)
        else:
            # Determine base labor rate and efficiency by ROtype
            if rotype == "RESALE" or rotype == "TRUCK":
                target_labor_rate = 175
                target_efficiency = 1.00
            elif rotype == "TRAILER":
                target_labor_rate = 120
                target_efficiency = 1.20
            else:
                target_labor_rate = 150
                target_efficiency = 1.00

            hours_worked = round(np.random.uniform(2.0, 6.9), 2)
            # Add customer and location efficiency
            actual_eff = target_efficiency + (kpi["efficiency"]/100 - 1.0) + efficiency_mod
            hours_billed = max(round(hours_worked * actual_eff, 2), 0.4)
            labor_worked = round(hours_worked * target_labor_rate, 2)
            row_labor_gm = np.clip(np.random.normal(kpi["labor_gm"] + labor_gm_mod, 0.07), 0.33, 0.91)
            labor_billed = round(labor_worked / (1 - row_labor_gm), 2)
            # Parts for repair jobs
            if rotype == "TRAILER":
                parts_cost = round(np.random.uniform(20 + parts_bias, 800 + parts_bias), 2)
            else:
                parts_cost = round(np.random.uniform(30 + parts_bias, 970 + parts_bias), 2)
            row_parts_gm = np.clip(np.random.normal(kpi["parts_gm"] + parts_gm_mod, 0.07), 0.09, 0.61)
            parts_sales = round(parts_cost / (1 - row_parts_gm), 2)

        cycle_days = round(np.clip(np.random.normal(kpi["cycle"], 2.5), 1.0, 15), 1)
        rows.append({
            "Location": loc, "Whse": wh, "InvoiceNo": inv_n,
            "InvDate": inv_date.strftime("%m/%d/%Y"),
            "CustNo": prof["CustNo"], "CustName": prof["CustName"],
            "ROtype": rotype, "Dept": dept,
            "HoursWorked": hours_worked, "HoursBilled": hours_billed,
            "LaborBilled$": labor_billed, "LaborWorked$": labor_worked,
            "PartsSales$": parts_sales, "PartsCost$": parts_cost, "InvCycleDays": cycle_days
        })
        inv_n += 1

print(f"All invoices generated. Total invoice rows: {len(rows)}")

df = pd.DataFrame(rows)
desired_order = [
    "Location", "Whse", "InvoiceNo", "InvDate", "CustNo", "CustName", "ROtype", "Dept",
    "HoursWorked", "HoursBilled",
    "LaborBilled$", "LaborWorked$", "PartsSales$", "PartsCost$", "InvCycleDays"
]
df = df[desired_order]

output_path = r"C:\Users\travi\Documents\anonymized_invoice_data.csv"
print(f"Saving file to {output_path} ...")
df.to_csv(output_path, index=False)
print(f"Finished. Invoice data CSV saved at: {output_path}")
