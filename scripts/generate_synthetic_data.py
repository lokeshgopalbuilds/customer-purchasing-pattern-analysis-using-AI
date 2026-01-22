import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Groceries",
    "Home",
    "Books",
    "Beauty",
    "Sports",
]

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "UPI",
    "Cash",
]

TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
REGIONS = ["North", "South", "East", "West", "Central"]
DEVICES = ["Mobile", "Desktop", "Tablet"]
GENDERS = ["Male", "Female", "Other"]


def generate_dates(n_rows: int, rng: np.random.Generator):
    start = datetime(2019, 1, 1)
    # Up to end of 2025
    max_days = (datetime(2025, 12, 31) - start).days
    signup_offsets = rng.integers(0, max_days, size=n_rows)
    signup_dates = np.array([start + timedelta(days=int(d)) for d in signup_offsets])

    # Last purchase is after signup by 0-730 days, clipped at end of 2025
    last_offsets = rng.integers(0, 730, size=n_rows)
    last_purchase_dates = signup_dates + np.array(
        [timedelta(days=int(d)) for d in last_offsets]
    )
    end_date = datetime(2025, 12, 31)
    last_purchase_dates = np.minimum(
        last_purchase_dates, np.array([end_date] * n_rows, dtype=object)
    )

    return signup_dates, last_purchase_dates


def generate_data(n_rows: int = 15000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    customer_id = np.arange(1, n_rows + 1)
    age = rng.integers(18, 81, size=n_rows)
    gender = rng.choice(GENDERS, size=n_rows, p=[0.49, 0.49, 0.02])
    region = rng.choice(REGIONS, size=n_rows, p=[0.22, 0.20, 0.19, 0.19, 0.20])
    device = rng.choice(DEVICES, size=n_rows, p=[0.65, 0.3, 0.05])

    signup_date, last_purchase_date = generate_dates(n_rows, rng)

    # Tenure in days, min 1
    tenure_days = np.maximum(
        (last_purchase_date - signup_date).astype("timedelta64[D]").astype(int), 1
    )

    # Base purchase intensity influenced by tenure and age (slightly)
    base_lambda = np.clip(tenure_days / 120 + (age - 35) / 200, 0.2, 8.0)
    purchase_count = rng.poisson(base_lambda)
    purchase_count = np.clip(purchase_count, 0, 100)

    # Preferred category distribution
    preferred_category = rng.choice(
        CATEGORIES,
        size=n_rows,
        p=[0.20, 0.18, 0.22, 0.12, 0.10, 0.10, 0.08],
    )

    # Loyalty tier influenced by purchase_count
    tier_probs = np.clip(
        np.stack(
            [
                0.55 - purchase_count / 200,  # Bronze
                0.30 + purchase_count / 300,  # Silver
                0.12 + purchase_count / 400,  # Gold
                0.03 + purchase_count / 600,  # Platinum
            ]
        , axis=1),
        0.01,
        0.9,
    )
    tier_probs = tier_probs / tier_probs.sum(axis=1, keepdims=True)
    loyalty_tier = np.array([
        TIERS[rng.choice(len(TIERS), p=prob)] for prob in tier_probs
    ])

    # Avg order value via log-normal, adjusted by category and tier
    category_factor = np.array([
        {
            "Electronics": 2.2,
            "Clothing": 1.0,
            "Groceries": 0.6,
            "Home": 1.4,
            "Books": 0.7,
            "Beauty": 0.9,
            "Sports": 1.2,
        }[c]
        for c in preferred_category
    ])

    tier_factor = np.array([
        {"Bronze": 0.9, "Silver": 1.0, "Gold": 1.15, "Platinum": 1.3}[t]
        for t in loyalty_tier
    ])

    avg_order_value = np.round(
        np.exp(rng.normal(loc=3.8, scale=0.55, size=n_rows)) * category_factor * tier_factor,
        2,
    )

    # Coupon usage percentage from Beta distribution, influenced by device
    device_factor = np.array([
        {"Mobile": 0.6, "Desktop": 0.4, "Tablet": 0.5}[d] for d in device
    ])
    coupon_used_pct = np.clip(rng.beta(a=2 + device_factor, b=5, size=n_rows), 0, 0.95)

    # Payment method
    payment_method = rng.choice(
        PAYMENT_METHODS,
        size=n_rows,
        p=[0.48, 0.22, 0.18, 0.10, 0.02],
    )

    # Total spent derived from count * avg value with noise
    spend_noise = rng.normal(1.0, 0.15, size=n_rows)
    total_spent = np.round(purchase_count * avg_order_value * spend_noise, 2)

    # Recency as days since last purchase (as of 2025-12-31)
    reference_date = np.datetime64("2025-12-31")
    recency_days = np.maximum(
        (reference_date - last_purchase_date.astype("datetime64[D]")).astype(int), 0
    )

    # Churn probability increases with recency and decreases with tier
    tier_churn_factor = np.array([
        {"Bronze": 1.0, "Silver": 0.9, "Gold": 0.75, "Platinum": 0.6}[t]
        for t in loyalty_tier
    ])
    churn_prob = np.clip(0.05 + (recency_days / 365) * 0.6 * tier_churn_factor, 0.01, 0.95)
    churned = (rng.random(n_rows) < churn_prob).astype(int)

    df = pd.DataFrame(
        {
            "customer_id": customer_id,
            "age": age,
            "gender": gender,
            "region": region,
            "device": device,
            "signup_date": signup_date,
            "last_purchase_date": last_purchase_date,
            "purchase_count": purchase_count,
            "preferred_category": preferred_category,
            "loyalty_tier": loyalty_tier,
            "avg_order_value": avg_order_value,
            "coupon_used_pct": np.round(coupon_used_pct, 3),
            "payment_method": payment_method,
            "total_spent": total_spent,
            "recency_days": recency_days,
            "churned": churned,
        }
    )

    # Ensure types
    df["signup_date"] = pd.to_datetime(df["signup_date"]).dt.date
    df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"]).dt.date

    return df


def main():
    out_path = Path("data/raw/synthetic_customers.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_data(n_rows=15000, random_state=42)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
