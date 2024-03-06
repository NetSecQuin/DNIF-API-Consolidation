import requests
import json
import time
import pandas as pd


# static variables
account_id = “<“ACCOUNT_ID>
API_TOKEN = “<“API_TOKEN>

# Function for the Query API
def get_task_id():
    url = f'https://ap1.dnif.cloud/{account_id}/wrk/api/job/invoke'
    headers = {
        'Token': API_TOKEN,
        'Content-Type': 'application/json'
    }
    payload = {
       "query_timezone": "Asia/Kolkata",
       "scope_id": "gotham",
       "job_type": "dql",
       "job_execution": "on-demand",
       #DQL query to be run
       "query": "_fetch * from event where $Stream=FIREWALL AND $StartTime=2024-02-21T10:42:00 AND $EndTime=2024-02-21T10:53:32 limit 10"
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # Extract task ID from the results and store it as a variable
    task_id = data.get('data', [])[0].get('id')
    return task_id

# Function for the status API to verify the query was successfully submitted
def check_task_status(task_id):
    url = f'https://ap1.dnif.cloud/{account_id}/wrk/api/dispatcher/task/state/{task_id}'
    headers = {'Token': API_TOKEN}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Function for the results API to retrieve the results
def get_task_result(task_id):
    url = f'https://ap1.dnif.cloud/{account_id}/wrk/api/dispatcher/task/result/{task_id}?pagesize=100&pageno=1'
    headers = {'Token': API_TOKEN}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Main function to verify that the first query ran successfully and completed prior to running the third API query to retrieve results
def main():
    # Get and store the task ID as a variable
    task_id = get_task_id()

    retries = 5
    retry_count = 0

    # Wait for query to finish and recheck status until it has completed
    while retry_count < retries:
        task_status = check_task_status(task_id)

        if task_status.get('status') == "success" and task_status.get('task_stage') == "EXECUTED" and task_status.get('task_state') == "SUCCESS":
            break
        else:
	# Sleep for 5 seconds in between each check - raise this for querying large data sets
            time.sleep(5)
            retry_count += 1

    # Endless retry protection, stops checking for a completed query after 5 checks
    if retry_count == retries:
        print("Task execution failed after 5 retries. Exiting...")
        return

    # Get task result and store it
    task_result = get_task_result(task_id)

    # Convert task result to DataFrame
    if 'result' in task_result:
        df = pd.DataFrame(task_result['result'])
        print(df)
    else:
        print("Error creating DataFrame, no data?")


# Execute the main function
if __name__ == "__main__":
    main()
