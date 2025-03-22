import os
import pandas as pd

# Define the paths
input_directory = 'data/diff_units'
output_directory = 'data/diff_units_zerod'

# Make sure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        # Construct full file path
        input_file_path = os.path.join(input_directory, filename)
        
        # Read the CSV file
        df = pd.read_csv(input_file_path)
        
        # Subtract the first value (index 0) from each value in the columns
        df_zeroed = df.apply(lambda x: x - x.iloc[0])
        
        # Save the modified DataFrame to the output directory
        output_file_path = os.path.join(output_directory, filename)
        df_zeroed.to_csv(output_file_path, index=False)
        
        print(f"Processed and saved: {filename}")

print("All files processed and saved to 'diff_units_zerod'.")
