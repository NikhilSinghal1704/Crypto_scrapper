import requests
import pandas as pd
import json

# Function to get the JSON data from the API
def get_data(job_id):
    url = f"http://127.0.0.1:8000/api/taskmanager/scraping_status/{job_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

# Function to convert JSON to Excel
def json_to_excel(data, output_file):
    tasks = data['tasks']
    df_list = []

    for task in tasks:
        coin = task['coin']
        output = task['output']
        
        # Flatten the nested JSON and add coin name
        flattened_data = {'coin': coin}
        flattened_data.update(flatten_json(output))
        
        # Convert the dictionary to DataFrame and append to the list
        df_list.append(pd.DataFrame([flattened_data]))

    # Concatenate all DataFrames
    final_df = pd.concat(df_list, ignore_index=True)
    
    # Write the DataFrame to Excel
    final_df.to_excel(output_file, index=False)

# Helper function to flatten nested JSON
def flatten_json(nested_json, parent_key='', sep='_'):
    items = []
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Main function
def main():
    job_id = input("Enter the Job ID: ")
    output_file = "output.xlsx"
    
    try:
        # Get the data from the API
        data = get_data(job_id)
        
        # Convert JSON data to Excel
        json_to_excel(data, output_file)
        
        print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

