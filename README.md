# Mortgage Calculator

Transparent mortgage calculator
Are you considering getting a loan? Do you already have a loan? Do you want to know more about the logic behind your mortgage's calculation and have more metrics that tell you how much money (in totals) are you paying for your loan?

Then this calculator may be for you.

The transparent mortgage calculator script provides allows the user to model a mortgage and understand the credit costs associated with it.

In the following section, I introduce some basic concepts necessary to understand mortgage calculations and how banks handle them.

Please bear in mind that the script does not account for administrative fees that the user might have to pay to the bank for handling the mortgage or for the purchase of the property (land tax, register's or notary fees).

Mortgage key terms:
Interest rate:

Principal:

Mortgage logic:
Banks may use 2 types of logic for handling mortgages:

Fixed principal style: you decide to pay exactly 1,000 EUR of your debt every month, plus whatever interest is owed. As a result, your debt goes down by exactly 1,000 every month, your interest goes down too. In this model you pay off the principal faster because you are paying a flat amount of debt plus interest

Fixed Total Payment Style (The Mortgage Standard), also known as French Amortization System: You pay exactly 1,000 EUR every single month for 30 years. At the beginning, that 1,000 is mostly interest. As the years go by, the interest portion shrinks, and the principal portion grows to fill the gap.

This code uses the French Amortization System for handling the logic of the mortgage calculation
