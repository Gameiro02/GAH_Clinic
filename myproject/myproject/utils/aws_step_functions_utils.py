import boto3
import json
import time

def start_execution(state_machine_arn, input_data):
    sfn_client = boto3.client("stepfunctions")
    return sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_data)
    )

# Not used because we are using poll_execution_status instead
def get_execution_response(execution_arn):
    sfn_client = boto3.client("stepfunctions")
    time.sleep(1) # Sleep to wait for execution to complete
    return sfn_client.describe_execution(executionArn=execution_arn)

def poll_execution_status(execution_arn, max_wait_time=30, initial_inverval=1, backkof_rate=1.5):
    """
    Polls the execution status of an AWS Step Function execution until it completes.

    Parameters:
        execution_arn (str): The ARN of the execution to poll.
        max_wait_time (int): Maximum total wait time in seconds before giving up.
        initial_interval (int): Initial interval in seconds between polls.
        backoff_rate (float): Rate at which the polling interval increases after each poll.

    Returns:
        dict: The final state of the execution.
    """
    sfn_client = boto3.client("stepfunctions")
    
    elapsed_time = 0
    interval = initial_inverval
    
    while elapsed_time < max_wait_time:
        response = sfn_client.describe_execution(executionArn=execution_arn)
        status = response["status"]
        
        if status == "SUCCEEDED" or status == "FAILED" or status == "TIMED_OUT":
            return response
        
        time.sleep(interval)
        elapsed_time += interval
        interval *= backkof_rate
        
    raise TimeoutError(f"Execution did not complete within {max_wait_time} seconds.")

def fetch_execution_history(execution_arn):
    sfn_client = boto3.client("stepfunctions")
    return sfn_client.get_execution_history(
        executionArn=execution_arn,
        reverseOrder=True
    )
    
def parse_error_from_history(history_response):
    last_event = history_response["events"][0]
    if 'executionFailedEventDetails' in last_event:
        error_info = last_event['executionFailedEventDetails']
        return error_info.get('error', 'Unknown error')
    return 'Unknown error'