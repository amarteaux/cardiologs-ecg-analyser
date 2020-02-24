from datetime import datetime

import typer

from .cardiogram_analyser import CardiogramAnalyser

app = typer.Typer()


@app.command("ecg-analyse")
def ecg_analyze(
    file_path: str,
    start_date: datetime = typer.Option(
        None, help="Start time of recording"
    ),
):
    """
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
    """
    if not start_date:
        start_date = datetime.now()

    ecg_analyser = CardiogramAnalyser()
    ecg_analyser.load_dataset(file_path, start_date)
    min_time, min_value = ecg_analyser._compute_min_bpm()
    max_time, max_value = ecg_analyser._compute_max_bpm()

    typer.echo(
        """
    start_time of recording: {start_date}
    total of premature P wave: {p_total}
    total of premature QRS wave: {qrs_total}
    heartbeat:
    - mean: {mean_bpm} bpms
    - max: {max_value} bpms, time: {max_time}
    - min: {min_value} bpms, time: {min_value}
    """.format(
            start_date=start_date.isoformat(),
            p_total=ecg_analyser.total_of_premature_p_wave(),
            qrs_total=ecg_analyser.total_of_premature_qrs_wave(),
            mean_bpm=ecg_analyser._compute_mean_bpm(),
            max_value=max_value,
            max_time=max_time,
            min_value=min_value,
            min_time=min_time,
        )
    )


def main():
    app()
