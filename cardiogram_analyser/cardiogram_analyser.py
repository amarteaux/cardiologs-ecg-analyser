from datetime import datetime

import pandas as pd


class CardiogramAnalyser:
    """
    Load ECG dataset and compute several metrics from it.

    - dataset: retreived dataset and added computed metrics.
    - bpms: heartbeat in bpms computed from dataset.
    """

    def _init_(self):
        self.dataset = None
        self.bpms = None

    def load_dataset(self, file_path: str, start_time: datetime) -> None:
        """
        Load a dataset to analyze.
        :param file_path: a path to the record

        dataset format:
        - Wave type: P, QRS, T or INV (invalid)
        - Wave onset: Start of the wave in ms
        - Wave offset: End of the wave in ms
        - Optionally, a list of wave tags
        """
        self.dataset = pd.read_csv(
            file_path, names=["type", "onset", "offset", "tag"]
        )
        self.start_time = start_time
        self._compute_peak_wave()
        self._compute_bpms()

    def _compute_bpms(self) -> None:
        """
        compute heartbeat in bpm.

        the bpms are compute from QRS peak_time.
        we caculate the delta between (QRS_peak_time+1) - QRS_peak_time.
        """
        rr_list = self.dataset[self.dataset.type == "QRS"].peak_time.diff()
        self.dataset["heartbeat"] = 60 / rr_list.dt.total_seconds()
        self.bpms = self.dataset[~self.dataset.heartbeat.isna()].heartbeat

    def _compute_peak_wave(self) -> None:
        """
        Compute the peak_wave of all waves.

        peak_time equals mean between onset and offset
        add all peak_time to dataset
        """
        col_limits = ["onset", "offset"]
        ms_peak_time = self.dataset[col_limits].mean(axis=1)
        self.dataset["peak_time"] = pd.to_timedelta(ms_peak_time, unit="ms")

    def _compute_max_bpm(self) -> tuple:
        """
        Find the max heartbeat on the recording.

        :return tuple(datetime, float):
        the max recorded heartbeat in bpms.
        """
        time = self.dataset.loc[self.bpms.idxmax()].peak_time + self.start_time
        max_bpm = self.bpms.max()
        return (time, max_bpm)

    def _compute_min_bpm(self) -> tuple:
        """
        Find the min heartbeat on the recording.

        :return tuple(datetime, float):
        the min recorded heartbeat in bpms.
        """
        time = self.dataset.loc[self.bpms.idxmin()].peak_time + self.start_time
        min_bpm = self.bpms.min()
        return (time, min_bpm)

    def _compute_mean_bpm(self) -> float:
        """
        Compute the mean of heartbeat in bpms

        :return float:
        The mean of heartbeat in bpms
        """
        return self.bpms.mean()

    def total_of_premature_p_wave(self) -> int:
        """
        Compute the total of premature P waves.

        :return int:
        The total of premature P waves.
        """
        is_premature = self.dataset.tag == "premature"
        is_p_wave = self.dataset.type == "P"

        return len(self.dataset[is_premature & is_p_wave].index)

    def total_of_premature_qrs_wave(self) -> int:
        """
        Compute the totalt of premature QRS waves.

        :return int:
        The total of premature QRS waves
        """
        is_premature = self.dataset.tag == "premature"
        is_qrs_wave = self.dataset.type == "QRS"

        return len(self.dataset[is_premature & is_qrs_wave].index)
