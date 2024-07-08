from datetime import datetime, timedelta
import pandas as pd

def dca_sell_strategy(file_path, start_date, end_date, period, selling_amount, selling_duration, first_sell_periods_after_buy):
    # Load the CSV file
    eth_data = pd.read_csv(file_path)
    
    # Convert Date column to datetime
    eth_data['Date'] = pd.to_datetime(eth_data['Date'])
    
    # Filter data for the given date range
    mask = (eth_data['Date'] >= start_date) & (eth_data['Date'] <= end_date)
    filtered_data = eth_data.loc[mask]
    
    # Initialize variables
    results = []
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    initial_buy_date = start_date_dt

    while initial_buy_date + timedelta(days=(first_sell_periods_after_buy + selling_duration - 1) * period) <= end_date_dt:
        initial_price = filtered_data.loc[filtered_data['Date'] == initial_buy_date, 'Price'].values[0]
        total_eth_to_sell = selling_amount * selling_duration
        initial_buying_amount = total_eth_to_sell * initial_price
        
        total_eth_sold = 0
        total_retrieved_usd = 0
        
        # Calculate DCA Sell
        first_sell_date = initial_buy_date + timedelta(days=first_sell_periods_after_buy * period)
        current_date = first_sell_date
        last_sold_date = first_sell_date + timedelta(days=(selling_duration - 1) * period)

        while current_date <= last_sold_date:
            price_on_date = filtered_data.loc[filtered_data['Date'] == current_date, 'Price']
            
            if not price_on_date.empty:
                price = price_on_date.values[0]
                usd_income = selling_amount * price
                total_retrieved_usd += usd_income
                total_eth_sold += selling_amount
            
            current_date += timedelta(days=period)
        
        current_value = total_retrieved_usd  # For consistency with the buy strategy, we assume current value = total retrieved USD
        roi = ((total_retrieved_usd - initial_buying_amount) / initial_buying_amount) * 100

        results.append({
            'Start Date': initial_buy_date.strftime('%Y-%m-%d'),
            'First Sold Date': first_sell_date.strftime('%Y-%m-%d'),
            'Last Sold Date': last_sold_date.strftime('%Y-%m-%d'),
            'Total ETH Sold': total_eth_sold,
            'Total Retrieved USD': total_retrieved_usd,
            'Initial Investment': initial_buying_amount,
            'ROI': roi
        })

        initial_buy_date += timedelta(days=1)

    return results

# Parameters
file_path = 'C:\\Users\\omnar\\Documents\\DCA\\ETH-USD-Price-Daily.csv'  # Adjust the path as needed
start_date = '2023-01-01'
end_date = '2023-12-31'
period = 7  # weekly
selling_amount = 1  # Amount of ETH to sell every week
selling_duration = 14  # 14 weeks of selling duration
first_sell_periods_after_buy = 1  # Number of periods after buy before first sell

# Execute
results = dca_sell_strategy(file_path, start_date, end_date, period, selling_amount, selling_duration, first_sell_periods_after_buy)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
results_df.to_csv('dca_sell_strategy_analysis.csv', index=False)

# Print a few results for verification
print(results_df.head())
print(results_df.tail())
