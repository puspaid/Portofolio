# Marketplace Store Viability Dashboard 2026

An interactive data analysis project built to answer one question: is it still worth
opening or continuing a store on a marketplace in 2026?

Built with Python and Streamlit, using two years of real transaction data from a home
and kitchenware store selling on Shopee.

## The business question

A small home and kitchenware store has been selling on Shopee since late 2023. Going
into 2026, with platform commissions rising and a new withholding tax about to kick in,
the owner needed a straight answer backed by actual numbers: keep going, or step back.

This dashboard answers that, along with the questions underneath it: which products
actually make money, where the demand is coming from, and what the cost structure looks
like once every fee and tax is accounted for.

## The data

Twenty thousand eight hundred forty-eight orders, placed between December 2023 and
November 2025, with 42 fields per order covering revenue, category, region, payment
method, shipping option, platform commission, and net profit under three different cost
scenarios. It also draws on reference tables for the 2026 Shopee, Tokopedia, TikTok and
Lazada fee structures, the new PPh22 withholding tax rule, and Indonesian e-commerce
market indicators from APJII, BPS and Bank Indonesia.

## The verdict

Viable, with conditions. The store is profitable, but the margin is thin and has been
shrinking. Under realistic reseller cost assumptions, cost of goods at 55% of the selling
price, two years of operation produced a net margin of 3.8%. Staying healthy from here
depends on three things: keeping cost of goods under roughly 45 to 50%, not leaning on
the current best-sellers (several of which lose money once shipping and platform costs
are counted in), and planning for higher 2026 platform commissions along with the new
0.5% PPh22 withholding tax, which this store's turnover already approaches.

## What the data shows

Order count is up 11% year over year, but revenue and average order value have both
gone down over the same period, meaning cheaper orders are replacing more valuable ones.
The three highest-volume categories all carry negative margins, while smaller, less
obvious categories are the ones actually turning a profit. The free-shipping subsidy the
store absorbs comes to about 21% of revenue, more than the platform's own commission.
Demand is heavily concentrated in Java, particularly Jabodetabek, West Java, Banten and
Central Java. And the store's 2024 turnover was already close to the Rp500 million
annual threshold that triggers automatic PPh22 withholding starting in August 2026.

## The dashboard

Six pages, each built around one question:

- Home: the overall viability verdict and headline numbers
- Monthly Trends: is performance improving or getting worse over time
- Category Breakdown: which products are actually profitable
- Regional Performance: where demand is concentrated
- Cost Structure: where the money goes, and how to cut the shipping subsidy
- Scenario Simulator: an interactive tool for testing your own cost assumptions

Live demo: add your Streamlit Community Cloud link here once deployed.

## Built with

Python, Streamlit, Pandas, Plotly.

## About this project

This was built as an end-to-end analysis: starting from raw transaction data, framing
the business question, building the financial model across three cost scenarios, and
shipping it as a deployed, interactive dashboard. Every chart on every page exists to
answer a specific question a store owner would actually ask, not to look impressive.

Puspa Ratih
edupuspa@gmail.com
https://linkedin.com/in/puspa-ratih-6a5a683b0
