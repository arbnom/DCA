import cryptocompare
import pandas as pd
import datetime as dt

# Define the date range
start_date = dt.datetime(2017, 1, 1)
end_date = dt.datetime(2017, 11, 11)

# Convert end date to Unix timestamp
end_timestamp = int(end_date.timestamp())

# Fetch historical data
eth_data = cryptocompare.get_historical_price_day('ETH', currency='USD', limit=310, toTs=end_timestamp)

# Convert to DataFrame
df = pd.DataFrame(eth_data)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)

# Save to CSV
df.to_csv('eth_usd_price_data.csv')

# Display the DataFrame
print(df)
