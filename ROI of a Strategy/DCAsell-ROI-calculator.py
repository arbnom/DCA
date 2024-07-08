from datetime import datetime, timedelta
import pandas as pd

def dca_sell_strategy(file_path, begin_date, end_date, period, selling_amount):
    # Load the CSV file
    eth_data = pd.read_csv(file_path)
    
    # Convert Date column to datetime
    eth_data['Date'] = pd.to_datetime(eth_data['Date'])
    
    # Filter data for the given date range
    mask = (eth_data['Date'] >= begin_date) & (eth_data['Date'] <= end_date)
    filtered_data = eth_data.loc[mask]
    
    # Initialize variables
    total_eth_sold = 0
    total_usd_income = 0
    initial_price = filtered_data['Price'].iloc[0]
    current_price = filtered_data['Price'].iloc[-1]
    
    # Calculate DCA Sell
    current_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date:
        # Find the price on the current date
        price_on_date = filtered_data.loc[filtered_data['Date'] == current_date, 'Price']
        
        if not price_on_date.empty:
            price = price_on_date.values[0]
            usd_income = selling_amount * price
            total_usd_income += usd_income
            total_eth_sold += selling_amount
        
        current_date += timedelta(days=period)
    
    # Calculate average sold price
    average_sold_price = total_usd_income / total_eth_sold
    
    # Calculate the current value of the retrieved USD in terms of ETH
    current_value_of_retrieved_usd_in_eth = total_usd_income / current_price
    
    # Calculate ROI based on the total USD income and the initial value of the sold ETH
    initial_investment_value = total_eth_sold * initial_price
    roi = ((total_usd_income - initial_investment_value) / initial_investment_value) * 100
    
    return {
        'Total ETH Sold': total_eth_sold,
        'Average Sold Price': average_sold_price,
        'Total USDC Income': total_usd_income,
        'Initial Price': initial_price,
        'Current Price': current_price,
        'Current Value of Retrieved USD in ETH': current_value_of_retrieved_usd_in_eth,
        'ROI': roi
    }

file_path = "add file path here"
result = dca_sell_strategy(file_path, '2022-01-01', '2022-12-31', 7, 4.9245)
print(result)
