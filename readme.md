# 🏃‍♂️ How fast will your running shoes sell?

A simple marketplace optimization tool that estimates how long second-hand running shoes may take to sell and provides recommendations to reduce sale time.

The idea came from a common marketplace problem: sellers often have no way to understand whether their listing is competitively priced or how long it may take to sell.

Instead of predicting whether a product will sell, this project focuses on a more useful question:

**How long will it take to sell, and what can I do to make it sell faster?**

The application allows users to enter information about their running shoes, including brand, model, condition, price and number of photos. It then estimates the expected sale time and suggests actions that could improve listing liquidity.

One example is reducing the listing price. The tool shows how a lower price could reduce the expected sale time and highlights the potential time saved.

A synthetic dataset of 5,000 running shoe listings was created for this project.

A real dataset would have been preferable, but publicly available marketplace datasets typically include product information and prices without providing the actual time between listing publication and sale. Since the project's objective was to predict time-to-sell, a synthetic dataset was generated to create a realistic testing environment.

The dataset includes variables such as:

* Brand
* Model
* Model year
* Condition
* Size
* Original retail price
* Estimated market price
* Listing price
* Seller rating
* Seller reviews
* Number of photos
* Season
* Days to sell

The data generation process was designed around a simple marketplace assumption:

**Listings priced below market value tend to sell faster.**

Additional factors such as condition, seller reputation, seasonality and photo count were also included to simulate realistic marketplace behaviour.

A Random Forest Regressor was trained to predict the target variable:

`days_to_sell`

The resulting model achieved an R² of approximately 0.78 on the synthetic dataset, indicating that it was able to explain a substantial portion of the variation in sale times.

This project was built primarily as a product and analytics exercise rather than a pure machine learning project. The goal was to explore how a marketplace could increase liquidity by providing sellers with actionable recommendations instead of simple prediction scores.

Tech stack:

* Python
* Pandas
* Scikit-Learn
* Streamlit
* Random Forest

Future improvements include collecting real marketplace data, incorporating listing descriptions and image quality metrics, and expanding the recommendation engine beyond pricing suggestions.
