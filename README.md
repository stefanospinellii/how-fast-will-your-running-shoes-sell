# 🏃‍♂️ Running Shoe Marketplace Liquidity Optimizer

**Live demo:** https://how-fast-will-your-running-shoes-sell-2n9cvszw5fdfzh4yzelhmu.streamlit.app/

A marketplace optimization tool that estimates how long a second-hand running shoe listing may take to sell, and recommends actionable steps to sell faster.

---

## In Plain English

You are selling a pair of Hoka Clifton 9 on a second-hand marketplace.

You set the price at €120. You have uploaded 4 photos.

This tool tells you:

> Expected sale time: 2–3 weeks
>
> Lower your price to €100 → New estimate: 8–14 days (~9 days faster)
>
> Add 4 more photos → New estimate: 2–3 weeks (~3 days faster)

The goal is not just prediction. The goal is giving sellers a concrete action to increase the speed at which their listing converts.

---

## Problem

Sellers on second-hand marketplaces have no way to know:

- Whether their listing is competitively priced
- How long it may realistically take to sell
- What they can do to sell faster

Most existing tools focus on price suggestion. This project focuses on a different and more actionable question:

> Given my listing as it is today, how long will it take to sell — and what should I change?

---

## Dataset

A synthetic dataset of 5,000 running shoe listings was created.

A real dataset would have been preferable. However, publicly available marketplace datasets typically contain listing information and final prices, but do not include the time elapsed between publication and sale. Since `days_to_sell` is the target variable, a synthetic dataset was the only viable approach without access to proprietary transaction data.

The dataset was generated using explicit marketplace assumptions, not random values. Each assumption reflects observed behavior in C2C marketplaces such as Vinted, Subito and Wallapop.

### Dataset statistics

| Metric | Value |
|---|---|
| Total listings | 5,000 |
| Sold listings | ~2,500 (50%) |
| Unsold listings | ~2,500 (50%) |
| Average days to sell | ~18 days |
| Median days to sell | ~18 days |

> Note: the regression model is trained exclusively on the ~2,500 sold listings, since only sold listings have an observed `days_to_sell` value.

---

## How Market Price Was Estimated

Each listing was assigned an estimated market value — the price a typical buyer might consider fair for a used running shoe in that condition.

Market price was derived from the original retail price using a condition-based discount:

```
market_price = retail_price × condition_discount
```

Condition discounts were defined as ranges. For each listing, a value was drawn uniformly at random within the range using `random.uniform(low, high)`.

| Condition | Discount range | Example (€150 retail) |
|---|---|---|
| New with tags | 80–90% | €120–€135 |
| New without tags | 65–80% | €97–€120 |
| Very good | 50–65% | €75–€97 |
| Good | 35–50% | €52–€75 |
| Fair | 18–32% | €27–€48 |

These ranges were defined based on qualitative observation of second-hand marketplace pricing. With real transaction data, they could be calibrated precisely.

---

## How Listing Price Was Generated

Each seller was then assigned a listing price relative to the market price.

```
price_gap_pct = (listing_price - market_price) / market_price
```

Seller behavior was modeled as skewed toward overpricing, which reflects real marketplace dynamics where many sellers anchor to retail price rather than market value.

| Price gap | Share of listings |
|---|---|
| -30% below market | 6% |
| -20% below market | 10% |
| -10% below market | 15% |
| At market | 14% |
| +10% above market | 18% |
| +20% above market | 17% |
| +30% above market | 10% |
| +40% above market | 6% |
| +55% above market | 4% |

---

## How Days to Sell Was Generated

The target variable `days_to_sell` was generated using a weighted combination of marketplace effects.

### Step 1 — Liquidity score

Each listing was assigned a liquidity score based on seven drivers:

```
liquidity_score =
    brand_effect
  + condition_effect
  + season_effect
  + photo_effect
  + seller_rating_effect
  + seller_reviews_effect
  + price_gap_effect
  + small_random_noise
```

### Step 2 — Days to sell

Days to sell was then derived from the liquidity score:

```
days_to_sell =
    base_days (20)
  - brand_effect     × 12
  - condition_effect × 8
  - season_effect    × 6
  - photo_effect     × 6
  - price_gap_effect × 5
  + noise (normal distribution, σ = 1.5)
```

A small amount of random noise was added intentionally to prevent the dataset from being perfectly deterministic.

---

## Driver Effects

### Price vs market value (strongest driver)

| Price gap | Liquidity effect |
|---|---|
| 30% below market | +1.50 |
| 20% below market | +1.10 |
| 10% below market | +0.70 |
| At market | +0.20 |
| 10% above market | -0.50 |
| 20% above market | -1.00 |
| 30% above market | -1.40 |
| 40%+ above market | -1.80 |

### Condition

| Condition | Liquidity effect |
|---|---|
| New with tags | +0.60 |
| New without tags | +0.35 |
| Very good | +0.15 |
| Good | baseline |
| Fair | -0.70 |

### Brand

| Brand | Liquidity effect |
|---|---|
| Hoka | +0.50 |
| On Running | +0.50 |
| ASICS | +0.30 |
| Nike | +0.10 |
| Adidas | +0.10 |
| New Balance | +0.10 |
| Saucony | baseline |
| Mizuno | baseline |
| Brooks | -0.20 |
| Other | -0.80 |

### Season

| Period | Liquidity effect |
|---|---|
| March–May | +0.60 |
| September | +0.60 |
| June–August | +0.35 |
| October–November | -0.30 |
| December | -0.20 |
| February | -0.55 |
| January | -0.80 |

### Photos

```
photo_effect = (photos_count - 6) × 0.10
```

At 1 photo: -0.50. At 12 photos: +0.60. Linear and monotonic.

### Seller rating

| Rating | Liquidity effect |
|---|---|
| 4.9–5.0 | +0.25 |
| 4.7–4.9 | +0.12 |
| 4.5–4.7 | baseline |
| 4.0–4.5 | -0.30 |
| Below 4.0 | -0.65 |

### Seller reviews

| Reviews | Liquidity effect |
|---|---|
| 0 | -0.65 |
| 1–5 | -0.30 |
| 6–20 | baseline |
| 21–50 | +0.15 |
| 51–100 | +0.25 |
| 100+ | +0.35 |

---

## Machine Learning Model

### Model

```
Random Forest Regressor
n_estimators = 150
random_state = 42
```

Random Forest was chosen because it handles mixed feature types (numeric and categorical) without requiring feature scaling, is robust to the moderate noise present in synthetic data, and produces interpretable feature importances.

### Target variable

```
days_to_sell
```

Predicting days to sell (regression) was preferred over predicting sold/not sold (classification) because it produces a more actionable output for the seller.

### Training data

The model was trained exclusively on sold listings (~2,500 rows). Unsold listings do not have an observed `days_to_sell` and cannot be used for regression.

A two-stage approach (first classify sold/not sold, then regress on days) would be a natural extension with real data.

### Performance

| Metric | Value |
|---|---|
| R² | ~0.78 |
| MAE | ~2.5 days |

> Important: R² = 0.78 on a synthetic dataset should be interpreted carefully. The model was trained and tested on data generated by the same logic it is learning from, which inflates performance compared to what would be observed on real marketplace data. With real transaction data, R² would likely be lower but the model would generalise to genuine seller behavior.

### Feature importance (top 10)

| Feature | Importance |
|---|---|
| price_gap_pct | 60.4% |
| condition_Fair | 5.6% |
| photos_count | 5.0% |
| season_Winter | 4.0% |
| brand_Other | 3.5% |
| seller_reviews | 2.2% |
| season_Spring | 1.7% |
| seller_rating | 1.5% |
| size_eu | 1.4% |
| season_Autumn | 1.1% |

Price gap dominates because it was designed as the strongest driver in the dataset. This reflects real marketplace behavior: perceived value relative to alternatives is the primary conversion driver.

---

## Recommendation Engine

A key design decision was separating prediction variables from recommendation variables.

The model uses all available features for prediction. However, recommendations are restricted to variables a seller can realistically change after publication:

- **Price** — the most impactful lever
- **Photos** — actionable and measurable

Variables such as brand, condition and season are excluded from recommendations because they are either fixed or could encourage misleading listings.

### How the price recommendation works

The engine uses binary search to find the minimum price reduction required to achieve a 40% reduction in expected sale time:

```
target_days = current_prediction × 0.60

binary_search(price):
    find lowest price where model predicts ≤ target_days
```

This avoids a fixed percentage reduction and instead finds the price that is actually model-optimal for each specific listing.

---

## Product Logic

Model output is converted into human-readable sale time buckets:

| Days | Label |
|---|---|
| ≤ 3 | 1–3 days |
| ≤ 7 | 4–7 days |
| ≤ 14 | 8–14 days |
| ≤ 21 | 2–3 weeks |
| ≤ 30 | 3–4 weeks |
| ≤ 60 | 1–2 months |
| ≤ 90 | 2–3 months |
| > 90 | 3+ months |

Displaying `2–3 weeks` instead of `19.5 days` is a deliberate UX decision. Precise day counts create false confidence in a model that is inherently probabilistic.

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn (Random Forest Regressor)
- Streamlit
- Joblib

---

## Future Improvements

- Real marketplace data collection via scraping or API
- Two-stage model: classify sold/not sold, then regress on days
- Market value estimation model calibrated on real prices
- Listing title and description quality scoring
- Image quality analysis
- Marketplace-specific calibration (Vinted vs Subito vs Wallapop)
- Dynamic pricing target by desired sale speed
