# finance_app/rules.py

# class FLAGS:
#     GREEN = 1
#     AMBER = 2
#     RED = 0
#     WHITE = 4  # Data missing
#
# def latest_financial_index(data: dict):
#     for index, financial in enumerate(data.get("financials")):
#         if financial.get("nature") == "STANDALONE":
#             return index
#     return 0
#
# def total_revenue(data: dict, financial_index):
#     financial = data.get("financials")[financial_index]
#     return financial.get("pnl", {}).get("lineItems", {}).get("net_revenue", 0)
#
# def total_borrowing(data: dict, financial_index):
#     financial = data.get("financials")[financial_index]
#     long_term = financial.get("bs", {}).get("lineItems", {}).get("long_term_borrowings", 0)
#     short_term = financial.get("bs", {}).get("lineItems", {}).get("short_term_borrowings", 0)
#     revenue = total_revenue(data, financial_index)
#     return (long_term + short_term) / revenue if revenue else 0
#
# def iscr(data: dict, financial_index):
#     financial = data.get("financials")[financial_index]
#     ebitda = financial.get("pnl", {}).get("lineItems", {}).get("profit_before_interest_and_tax", 0)
#     depreciation = financial.get("pnl", {}).get("lineItems", {}).get("depreciation", 0)
#     interest = financial.get("pnl", {}).get("lineItems", {}).get("interest", 1)
#     return (ebitda + depreciation + 1) / (interest + 1)
#
# def iscr_flag(data: dict, financial_index):
#     return FLAGS.GREEN if iscr(data, financial_index) >= 2 else FLAGS.RED
#
# def total_revenue_5cr_flag(data: dict, financial_index):
#     return FLAGS.GREEN if total_revenue(data, financial_index) >= 50_000_000 else FLAGS.RED
#
# def borrowing_to_revenue_flag(data: dict, financial_index):
#     return FLAGS.GREEN if total_borrowing(data, financial_index) <= 0.25 else FLAGS.AMBER












import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field


def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.

    This function accesses the "financials" list in the data dictionary at the specified index.
    It then retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data at the given index.

    This function sums the long-term and short-term borrowings from the balance sheet ("bs")
    section of the financial data. It then divides this sum by the total revenue, calculated
    by calling the total_revenue function.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The ratio of total borrowings to total revenue.
    """
    bs = data["financials"][financial_index]["bs"]
    long_term_borrowings = bs["liabilities"]["long_term_borrowings"]
    short_term_borrowings = bs["liabilities"]["short_term_borrowings"]
    total_borrowings = long_term_borrowings + short_term_borrowings

    revenue = total_revenue(data, financial_index)

    return total_borrowings / revenue if revenue != 0 else float("inf")


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    This function calculates the ISCR value by calling the iscr function and then assigns a flag color
    based on the ISCR value. If the ISCR value is greater than or equal to 2, it assigns a GREEN flag,
    otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    This function calculates the total revenue by calling the total_revenue function and then assigns
    a flag color based on the revenue amount. If the total revenue is greater than or equal to 50 million,
    it assigns a GREEN flag, otherwise, it assigns a RED flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    ISCR is a ratio that measures how well a company can cover its interest payments on outstanding debt.
    It is calculated as the sum of profit before interest and tax, and depreciation, increased by 1,
    divided by the sum of interest expenses increased by 1. The addition of 1 is to avoid division by zero.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    pnl = data["financials"][financial_index]["pnl"]["lineItems"]
    pbit = pnl["profit_before_interest_and_tax"]
    depreciation = pnl["depreciation"]
    interest = pnl["interest"]

    return (pbit + depreciation + 1) / (interest + 1)


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the total_borrowing
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    borrowing_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_ratio <= 0.25 else FLAGS.AMBER











