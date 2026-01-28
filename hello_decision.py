import csv

DATA_PATH = "data/sales.csv"


def load_sales(path):
    """
    Reads a CSV file and returns a list of rows.
    Each row is a small dictionary: {"month": "...", "sales_eur": number}
    """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reads the header: month,sales_eur
        for r in reader:
            rows.append({"month": r["month"], "sales_eur": int(r["sales_eur"])})
    return rows


def main():
    rows = load_sales(DATA_PATH)

    # Extract sales and months into simple lists (easier to compute)
    sales = [r["sales_eur"] for r in rows]
    months = [r["month"] for r in rows]

    # Executive metrics
    total_sales = sum(sales)
    avg_sales = total_sales / len(sales)

    best_idx = sales.index(max(sales))
    worst_idx = sales.index(min(sales))

    # Month-over-month change (last month vs previous)
    mom_change = sales[-1] - sales[-2]
    mom_pct = (mom_change / sales[-2]) * 100

    print("=== LDIA – Week 1 Executive Snapshot ===")
    print(f"Total sales: €{total_sales:,}")
    print(f"Average monthly sales: €{avg_sales:,.0f}")
    print(f"Best month: {months[best_idx]} (€{sales[best_idx]:,})")
    print(f"Worst month: {months[worst_idx]} (€{sales[worst_idx]:,})")
    print(f"Last MoM change: €{mom_change:,} ({mom_pct:.1f}%)")


if __name__ == "__main__":
    main()
