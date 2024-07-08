from datetime import datetime, timedelta
import pandas as pd

def dca_strategy_roi(file_path, start_date, end_date, period, buying_amount, holding_period, sell_period_after_last_buy):
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
    current_date = start_date_dt
    
    while current_date + timedelta(days=holding_period + (sell_period_after_last_buy * period)) <= end_date_dt:
        begin_date = current_date
        last_buy_date = current_date + timedelta(days=holding_period - period)  # Adjusted to account for holding period
        sell_date = last_buy_date + timedelta(days=sell_period_after_last_buy * period)
        
        # Initialize DCA variables
        total_invested = 0
        total_eth_bought = 0
        
        # Calculate DCA
        dca_date = begin_date
        while dca_date <= last_buy_date:  # Changed to <= to include the last buy date
            price_on_date = filtered_data.loc[filtered_data['Date'] == dca_date, 'Price']
            
            if not price_on_date.empty:
                price = price_on_date.values[0]
                eth_bought = buying_amount / price
                total_eth_bought += eth_bought
                total_invested += buying_amount
            
            dca_date += timedelta(days=period)
        
        # Find the price on the sell date
        sell_price_on_date = filtered_data.loc[filtered_data['Date'] == sell_date, 'Price']
        if not sell_price_on_date.empty:
            sell_price = sell_price_on_date.values[0]
            current_value = total_eth_bought * sell_price
            
            # Calculate ROI for DCA
            roi = ((current_value - total_invested) / total_invested) * 100
            
            # Calculate ROI for buy-and-hold
            buy_hold_price = filtered_data.loc[filtered_data['Date'] == begin_date, 'Price']
            if not buy_hold_price.empty:
                initial_price = buy_hold_price.values[0]
                initial_eth_bought = total_invested / initial_price
                hold_value = initial_eth_bought * sell_price
                roi_hold = ((hold_value - total_invested) / total_invested) * 100
                
                results.append({
                    'Start Date': begin_date.strftime('%Y-%m-%d'),
                    'Last Buy Date': last_buy_date.strftime('%Y-%m-%d'),
                    'Sell Date': sell_date.strftime('%Y-%m-%d'),
                    'Total ETH Bought': total_eth_bought,
                    'Total Paid USD': total_invested,
                    'Current Value of DCA Asset': current_value,
                    'ROI': roi,
                    'Current Value of Hold Asset': hold_value,
                    'ROI Hold': roi_hold
                })
        
        current_date += timedelta(days=1)
    
    return results

# Parameters
file_path = 'C:\\Users\\omnar\\Documents\\DCA\\ETH-USD-Price-Daily.csv'  # Adjust the path as needed
start_date = '2023-01-01'
end_date = '2023-12-31'
period = 7  # weekly
buying_amount = 100  # Adjust the buying amount as needed
holding_period = 14 * 7  # 14 weeks
sell_period_after_last_buy = 1  # Adjust the sell period (1 means 15th week, 2 means 16th week, etc.)

# Execute
results = dca_strategy_roi(file_path, start_date, end_date, period, buying_amount, holding_period, sell_period_after_last_buy)

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
results_df.to_csv('dca_strategy_roi_analysis.csv', index=False)

# Print a few results for verification
print(results_df.head())
print(results_df.tail())
