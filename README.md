# Mortgage Calculator

Are you considering taking out a mortgage, or do you already have one and want to better understand how your monthly payments and interest costs are calculated?

This calculator allows users to model a mortgage, explore the relationship between principal and interest payments, and better understand the overall cost of their credit.

The calculator uses an API to retrieve the latest 6-month Euribor interest rate published by the European Central Bank (ECB), which is then combined with the bank's margin to calculate the applicable interest rate.

Please bear in mind that the calculator does not account for administrative or other additional costs that may be associated with a mortgage or property purchase, such as bank fees, land transfer tax, registration fees, or notary fees.


# How to use it?

## Use the app

**No installation or coding required.**

👉 [Open the Mortgage Calculator](https://mortgagecalculator-jvwftjucudgpltva6mytku.streamlit.app/)

##  Run locally 

#### Clone the repository and create a virtual environment
```bash
python -m venv .venv
```

#### Activate the virtual environment
```bash
source .venv/bin/activate
```

#### Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

#### Run the app 
```bash
streamlit run mortgage_app.py
```


## Mortgage key terms:

This section introduces some basic concepts necessary to understand mortgage calculations and the terminology used in the app. 

- Property Value: Total market or appraised value of the asset being purchased.

- Down Payment: Initial out-of-pocket cash contribution provided upfront by the buyer toward the purchase price.

- Loan Amount (Principal Original Balance): Total borrowed capital supplied by the lender. Combined with the down payment, it equals the total property value.

- Interest Rate: Percentage charged by the lender on the remaining principal balance, representing the annual cost of borrowing the funds.

- EURIBOR (Euro Interbank Offered Rate): Benchmark reference rate at which European banks lend funds to one another. Serves as the base index for variable-rate consumer loans in many European countries.

- Bank Margin (Spread): Constant markup percentage added by the bank on top of the base index (e.g., EURIBOR). In a fixed-rate mortgage, the entire interest rate is determined upfront by the bank.

- Combined Interest Rate (Effective Rate): Total interest rate charged on a variable mortgage, calculated as the sum of the base index (EURIBOR) and the bank margin ($\text{EURIBOR} + \text{Bank Margin}$). For a fixed mortgage, it equals the fixed rate agreed upon.

- Monthly Payment (Mortgage Installment): Scheduled amount paid to the lender each month, typically comprising both principal reduction and interest charges.

- Total Interest Cost: Aggregate amount paid in interest over the entire life of the loan until the mortgage is fully paid off.

- Principal: Outstanding amount of the borrowed loan balance at any given point, excluding accumulated interest and fees.

- Cumulative Interest: Total running sum of all interest payments made from the start of the loan up to a specific date or payment installment.

- Cumulative Principal: Total running sum of all principal payments applied toward reducing the original loan balance up to a specific date or payment installment.


## Mortgage logic:

Banks may use 2 types of logic for handling mortgages:

Fixed principal style: you decide to pay exactly 1,000 EUR of your debt every month, plus whatever interest is owed. As a result, your debt goes down by exactly 1,000 every month, your interest goes down too. In this model you pay off the principal faster because you are paying a flat amount of debt plus interest

Fixed Total Payment Style (The Mortgage Standard), also known as French Amortization System: You pay exactly 1,000 EUR every single month for 30 years. At the beginning, that 1,000 is mostly interest. As the years go by, the interest portion shrinks, as the debt decreases, and the principal portion grows to fill the gap.

This mortgage calculator uses the French Amortization System for handling the logic of the mortgage calculation.
