To run:

> python checks.py /path/to/responses/json > results
I.e.
> python checks.py data/modified/

See data/original for examples of task json.

data/original: Downloaded json from the 8 task examples.
data/modified: The 8 tasks in original modified to have some quality problems.

--------
I was not able to get an API call to get a single task json.
I.e. I tried

```
url = "https://api.scale.com/v1/tasks"
auth = HTTPBasicAuth('{{apikey}}', '') # No password
response = requests.request("GET", url, headers=headers, auth=auth)
print(response.text)
```

Which got back tasks but they did not have the type of tasks in the 8 examples.

I also tried /v1/task/<task_id> but got permission problems.

So I created a dataset of the 8 tasks.

But the code works at a task level.
