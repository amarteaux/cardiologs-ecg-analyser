
# content
This cli tools compute metrics from a ECG dataset

# develop
run during development:
```
poetry run ecg-analyse RECORD_PATH --start-date ""
```

# build wheel package
```
poetry install
poetry build
```
# usage
```
Usage: ecg-analyse [OPTIONS] FILE_PATH

  Analyze the given csv recording of ECG to display stats on it.

  :param file_path: path of the recording
  :param start_date: starting datetime of the recording

  :output:
     start_time of recording: {start_date}
     total of premature P wave: {p_total}
     total of premature QRS wave: {qrs_total}
     heartbeat:
     - mean: {mean_bpm} bpms
     - max: {max_value} bpms, time: {max_time}
       - min: {min_value} bpms, time: {min_value}

Options:
  --start-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  Start time of recording
  --help                          Show this message and exit.
```
