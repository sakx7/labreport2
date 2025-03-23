import os
import pandas as pd

input_directory = 'data/diff_units'
output_directory = 'data/diff_units_zerod'

os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(input_file_path)
        df_zeroed = df.apply(lambda x: x - x.iloc[0])
        output_file_path = os.path.join(output_directory, filename)
        df_zeroed.to_csv(output_file_path, index=False)        
        print(f"Processed and saved: {filename}")

print("All files processed and saved to 'diff_units_zerod'.")
