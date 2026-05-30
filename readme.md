# 🏃‍♂️ Running Shoe Marketplace Liquidity Optimizer

A marketplace optimization tool that estimates how long second-hand running shoes may take to sell and provides actionable recommendations to reduce sale time.

## Project Overview

The idea originated from a common marketplace problem:

> Sellers often have no way to understand whether their listing is competitively priced or how long it may take to sell.

Most marketplace tools focus on predicting whether an item will sell.

This project instead focuses on a more practical question:

> How long will it take to sell, and what can I do to make it sell faster?

The application allows users to enter information about a running shoe listing, including brand, model, condition, price and number of photos.

The system then:

1. Estimates expected sale time
2. Identifies the most impactful action
3. Quantifies the time saved from applying that action

Example:

```text
Expected sale time:
2–3 weeks

Recommended action:
Reduce price by 20%

New estimate:
8–14 days

Save ~8 days
```

The project was designed as a marketplace product and analytics exercise rather than a pure machine learning project.

## Dataset

A synthetic dataset containing approximately 5,000 running shoe listings was created.

A real dataset would have been preferable, but publicly available marketplace datasets typically contain product information and prices without providing the actual time elapsed between listing publication and sale.

Since the project's objective was to predict time-to-sell, a synthetic environment was built to simulate marketplace behaviour.

The dataset includes:

* Brand
* Model
* Model year
* Condition
* Colour
* Size
* Original retail price
* Estimated market value
* Listing price
* Price gap versus market value
* Seller rating
* Seller reviews
* Number of photos
* Season
* Days to sell
* Sold / Unsold status

Current dataset statistics:

* Listings: ~5,000
* Sold rate: ~53.7%
* Average days to sell: ~18 days

## Synthetic Data Generation Logic

The dataset was generated using explicit marketplace assumptions rather than random values.

### Estimated Market Value

Each listing was assigned an estimated market value.

Market value was derived from:

* Original retail price
* Brand
* Model age
* Condition

The objective was to approximate what a typical buyer might consider a fair market value for a used running shoe.

This variable acts as the marketplace benchmark used throughout the project.

### Listing Price

Listings were then generated above or below the estimated market value.

The key metric is:

```text
price_gap_pct =
(listing_price - market_price)
/ market_price
```

Examples:

```text
Market value = €100
Listing price = €80

price_gap_pct = -20%
```

```text
Market value = €100
Listing price = €120

price_gap_pct = +20%
```

This became the strongest driver of sale speed.

### Condition Effects

Different item conditions were assigned different liquidity effects.

```text
New with tags     → +20%
New without tags  → +12%
Very good         → +6%
Good              → baseline
Fair              → -30%
```

The assumption is that buyers trust and value higher-condition products more.

### Brand Effects

Demand was adjusted based on brand popularity.

```text
Hoka              → +15%
On Running        → +15%
ASICS             → +10%
Nike              → +5%
Adidas            → +5%
New Balance       → +5%
Saucony           → +2%
Mizuno            → +2%
Brooks            → baseline
Other             → -25%
```

These values reflect perceived marketplace demand rather than objective product quality.

### Seasonality Effects

Running shoe demand varies throughout the year.

```text
March–May         → +15%
June–August       → +10%
September         → +15%
October–November  → -10%
December          → -5%
January           → -20%
February          → -15%
```

The dataset assumes stronger demand during periods when outdoor running activity is higher.

### Seller Reputation Effects

Seller trust was incorporated using review counts.

```text
0 reviews         → -25%
1–5 reviews       → -10%
6–20 reviews      → baseline
21–50 reviews     → +5%
51–100 reviews    → +8%
100+ reviews      → +10%
```

The assumption is that buyers are more willing to purchase from established sellers.

### Photo Effects

Listings with more photos receive a modest liquidity boost.

Additional photos improve buyer confidence, although the effect was designed to exhibit diminishing returns after roughly 8–10 photos.

### Assumptions Summary

| Variable              | Marketplace Assumption                      |
| --------------------- | ------------------------------------------- |
| Price vs Market Value | Lower-priced listings sell faster           |
| Condition             | Better condition increases buyer confidence |
| Brand                 | Popular brands attract more demand          |
| Photos                | More photos reduce buyer uncertainty        |
| Reviews               | Trusted sellers convert more easily         |
| Seasonality           | Running demand changes throughout the year  |

### Sale Time Generation

The target variable (`days_to_sell`) was generated using a weighted combination of marketplace effects.

Conceptually:

```text
days_to_sell ≈

Base Sale Time

- Pricing Effect
- Condition Effect
- Brand Effect
- Reputation Effect
- Photo Effect
- Seasonality Effect

+ Random Noise
```

A small amount of random variation was intentionally introduced to prevent the dataset from becoming perfectly deterministic and to create a more realistic marketplace environment.

## Target Variable

The model predicts:

```text
days_to_sell
```

Rather than predicting whether a listing will sell, the objective is to estimate the expected time required for a transaction to occur.

## Machine Learning Model

Model used:

```text
Random Forest Regressor
```

Target:

```text
days_to_sell
```

Performance:

```text
R² ≈ 0.78
```

This indicates that the model is able to explain approximately 78% of the variation in sale times within the synthetic dataset.

## What Drives Sale Speed?

After training, feature importance analysis produced the following results:

| Feature               | Importance |
| --------------------- | ---------- |
| price_gap_pct         | 59.6%      |
| market_price          | 10.1%      |
| photos_count          | 4.9%       |
| season_winter         | 3.9%       |
| seller_reviews        | 2.1%       |
| season_spring         | 2.0%       |
| original_retail_price | 1.9%       |
| listing_price         | 1.8%       |
| seller_rating         | 1.5%       |
| size                  | 1.3%       |

Key insight:

> Pricing relative to market value dominates all other variables.

This closely matches the assumptions used during dataset generation.

The model also identifies photo count, seller reputation and seasonality as meaningful but secondary marketplace signals.

Interestingly, brand, colour and city contribute very little to predictive performance.

This suggests that buyers primarily react to perceived value rather than cosmetic listing characteristics.

## Recommendation Engine

A key design decision was separating:

**Prediction variables**

from

**Recommendation variables**

The model uses many variables for prediction:

* Brand
* Season
* Reviews
* Condition
* Photos
* Price

However, recommendations are restricted to variables sellers can realistically modify.

Recommendations currently focus on:

* Price
* Photos

Variables such as brand, season and condition are intentionally excluded because they are either fixed or could encourage misleading listings.

## Product Logic

The application converts model outputs into user-friendly sale-time buckets.

Examples:

```text
1–3 days
4–7 days
8–14 days
2–3 weeks
3–4 weeks
1–2 months
2–3 months
3+ months
```

Instead of displaying:

```text
19.5 days
```

users see:

```text
2–3 weeks
```

which is more intuitive and better aligned with marketplace UX.

## Example Output

```text
Expected sale time:
2–3 weeks

Recommended action:
Reduce price by 20%

New estimate:
8–14 days

Save ~8 days
```

The goal is not simply prediction.

The goal is increasing marketplace liquidity by helping sellers make better listing decisions.

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* Random Forest Regressor
* Streamlit
* Joblib

## Future Improvements

Potential future enhancements include:

* Real marketplace data collection
* Market-value estimation model
* Listing description analysis
* Image quality scoring
* More advanced recommendation logic
* Dynamic pricing recommendations
* Marketplace-specific calibration

The long-term vision is to explore how marketplaces could proactively improve liquidity by helping sellers optimise listings before publication.
