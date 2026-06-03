# Running Shoe Marketplace Liquidity Optimizer

Live demo: https://how-fast-will-your-running-shoes-sell-2n9cvszw5fdfzh4yzelhmu.streamlit.app/

This is a marketplace optimization tool that estimates how long a second-hand running shoe listing may take to sell, and recommends actionable steps to sell faster.

## Project Overview

The idea originated from a common marketplace problem:

> Sellers often have no way to understand whether their listing is competitively priced or how long it may take to sell.

Most marketplace tools focus on predicting whether an item will sell.

This project instead focuses on a more practical question:

> How long will it take to sell, and what can I do to make it sell faster?

The project evolved from a machine learning experiment into a product-design exercise.

The initial goal was to predict time-to-sell using a Random Forest model trained on a synthetic marketplace dataset. During development, however, the project shifted focus toward creating a recommendation engine capable of delivering intuitive and actionable feedback to users.

The final application combines marketplace simulation, machine learning insights and product design principles to help sellers optimise their listings.

The system then:

1. Estimates expected sale time
2. Simulates potential listing improvements
3. Quantifies the expected reduction in sale time
4. Helps sellers optimise their listing through iterative recommendations

Example:

```text
Expected sale time:
2–3 weeks

Suggested action:
Lower price to €96

New estimate:
8–14 days

Potential improvement:
~8 days faster
```

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

* Listings: 5,000
* Sold rate: 53.7%
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

### Seasonality Effects

```text
March–May         → +15%
June–August       → +10%
September         → +15%
October–November  → -10%
December          → -5%
January           → -20%
February          → -15%
```

### Seller Reputation Effects

```text
0 reviews         → -25%
1–5 reviews       → -10%
6–20 reviews      → baseline
21–50 reviews     → +5%
51–100 reviews    → +8%
100+ reviews      → +10%
```

### Photo Effects

Listings with more photos receive a modest liquidity boost.

Additional photos improve buyer confidence, although the effect exhibits diminishing returns after roughly 8–10 photos.

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

## Machine Learning Model

A Random Forest Regressor was trained to predict:

```text
days_to_sell
```

using the synthetic marketplace dataset.

Performance:

```text
R² ≈ 0.78
```

The model successfully captured the relationships embedded in the synthetic marketplace environment and was used to validate the dataset generation logic.

More importantly, it helped identify which variables had the greatest impact on marketplace liquidity.

The machine learning phase provided confidence that the synthetic marketplace assumptions were internally consistent and produced realistic behaviour.

## What Drives Sale Speed?

Feature importance analysis showed that pricing relative to market value is by far the strongest predictor of sale speed.

The most influential variables include:

* Price gap versus market value (`price_gap_pct`)
* Number of photos
* Seller reviews
* Seller rating
* Seasonality

Condition and brand also contribute to predictions, although their impact is significantly smaller than pricing.

### Key Insight

> Pricing relative to market value dominates all other variables.

This result closely matches the assumptions used during dataset generation and reflects a common marketplace dynamic: buyers primarily respond to perceived value relative to competing listings.

Secondary signals such as seller reputation, photo count and seasonality also influence sale speed, but to a much smaller degree.

Interestingly, many listing characteristics contribute relatively little once pricing is taken into account, suggesting that competitive pricing is the primary driver of marketplace liquidity.

## From Machine Learning to Product Design

One of the most interesting outcomes of the project was discovering the difference between building an accurate model and building a useful product.

Although the Random Forest achieved strong predictive performance, directly exposing model predictions in the web application often produced recommendations that felt less intuitive to users.

To better understand the underlying marketplace dynamics, a simplified linear regression was fitted using the two most actionable listing variables:

* Price relative to market value (`price_gap_pct`)
* Number of photos

The resulting relationship was:

```text
days_to_sell ≈
19.7
+ 26.2 × price_gap_pct
− 0.46 × photos_count

After training the Random Forest model and analysing feature importance, we observed that two variables consistently dominated the prediction of sale speed:

- Price relative to market value (`price_gap_pct`)
- Number of photos (`photos_count`)

To better understand their relationship with sale time, we fitted a separate linear regression model using only these two variables and the sold listings in the dataset.

The regression estimated the coefficients directly from the data and produced:

- Intercept = 19.7
- price_gap_pct coefficient = 26.2
- photos_count coefficient = -0.46

These values represent the average relationship observed in the synthetic marketplace:

- A listing priced 10% above market value is expected to take roughly 2.6 additional days to sell.
- Each additional photo reduces expected sale time by approximately 0.5 days.

The purpose of this simplified model was not to outperform the Random Forest. Instead, it provided an interpretable approximation of the marketplace dynamics discovered during the machine learning phase, making it suitable for generating transparent user-facing recommendations.
```

This simplified model achieved:

```text
R² ≈ 0.58
```

While less accurate than the Random Forest, it captured most of the marketplace behaviour using only two interpretable variables.

This analysis revealed something important: although the Random Forest explained more variance, the simpler formula produced recommendations that were easier to understand and behaved more intuitively in extreme pricing scenarios.

As a result, the project evolved from a prediction exercise into a marketplace optimisation tool.

The machine learning model was ultimately used to:

* Validate the synthetic dataset
* Quantify the drivers of liquidity
* Inform product design decisions

The final recommendation engine then translated those insights into a simpler and more actionable user experience.

This mirrors a common real-world product challenge: the most accurate model is not always the best user experience.

## Product Logic

The deployed application uses a transparent formula-based recommendation engine derived from the analysis performed during the machine learning phase.

### Recommendation Formula

The recommendation engine is based on the linear regression fitted on the sold listings:

```text
days_to_sell = 19.7 + (26.2 × price_gap_pct) - (0.46 × photos_count)
```

Where:

```text
price_gap_pct = (listing_price - market_price) / market_price
```

This formula was derived directly from the data rather than manually specified.

The regression produced the following coefficients:

| Component     | Value | Meaning                                                     |
| ------------- | ----- | ----------------------------------------------------------- |
| Intercept     | 19.7  | Baseline sale time                                          |
| price_gap_pct | +26.2 | Each 10% above market adds approximately 2.6 days           |
| photos_count  | -0.46 | Each additional photo reduces sale time by roughly 0.5 days |

The linear regression achieved an R² of 0.58, meaning that pricing and photos alone explain approximately 58% of the variation in sale times.

This result reinforces the central insight of the project:

> Pricing is the dominant driver of marketplace liquidity.

### Why a Formula Instead of the Model

The Random Forest was extremely valuable for validating marketplace assumptions and identifying the key drivers of sale speed.

However, when translated into user-facing recommendations, the simpler formula produced more consistent and interpretable behaviour.

The final application therefore prioritises transparency and usability while remaining grounded in the patterns discovered during the machine learning phase.

### How Recommendations Work

When a user requests an estimate, the application:

1. Estimates the current sale time using the formula
2. Simulates a 20% price reduction
3. If the projected improvement is 2 or more days, suggests the lower price
4. Recalculates the expected sale time at the new price

Because the recommendation is generated from an interpretable formula, users can repeatedly test lower prices and immediately understand the trade-off between price and expected selling speed.

Sale times are displayed as user-friendly ranges rather than raw numbers.

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

## Example Output

```text
Expected sale time:
2–3 weeks

Suggested action:
Lower price to €96

New estimate:
8–14 days

Potential improvement:
~8 days faster
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

## Key Learnings

This project highlighted three important lessons:

* Building a predictive model and building a useful product are different challenges
* Pricing relative to market value is the dominant driver of marketplace liquidity
* Machine learning can be valuable even when the final product uses a simpler decision engine

The final outcome was not simply a machine learning model, but a marketplace optimisation tool informed by data, validated through modelling and refined through product design.

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
