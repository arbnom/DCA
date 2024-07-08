from datetime import datetime, timedelta
import pandas as pd

def dca_strategy(file_path, begin_date, end_date, period, buying_amount):
    # Load the CSV file
    eth_data = pd.read_csv(file_path)
    
    # Convert Date column to datetime
    eth_data['Date'] = pd.to_datetime(eth_data['Date'])
    
    # Filter data for the given date range
    mask = (eth_data['Date'] >= begin_date) & (eth_data['Date'] <= end_date)
    filtered_data = eth_data.loc[mask]
    
    # Initialize variables
    total_invested = 0
    total_eth_bought = 0
    current_price = filtered_data['Price'].iloc[-1]
    
    # Calculate DCA
    current_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date:
        # Find the price on the current date
        price_on_date = filtered_data.loc[filtered_data['Date'] == current_date, 'Price']
        
        if not price_on_date.empty:
            price = price_on_date.values[0]
            eth_bought = buying_amount / price
            total_eth_bought += eth_bought
            total_invested += buying_amount
        
        current_date += timedelta(days=period)
    
    # Calculate average bought price
    average_bought_price = total_invested / total_eth_bought
    
    # Calculate ROI
    roi = ((total_eth_bought * current_price) - total_invested) / total_invested * 100
    
    # Calculate the current value of the asset
    current_value = total_eth_bought * current_price
    
    return {
        'Total ETH Bought': total_eth_bought,
        'Average Bought Price': average_bought_price,
        'Current Price': current_price,
        'Total Paid USD': total_invested,
        'Current Value of Asset': current_value,
        'ROI': roi
    }

file_path = "add file path here"
result = dca_strategy(file_path, '2017-01-01', '2018-12-17', 7, 100)
print(result)
