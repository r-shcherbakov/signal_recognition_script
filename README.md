## How to Run

To run:

    python3 ./run.py

## Program Description

This script measures the relationship between two datasets: measured signal and reference.
Script parameters is located in the `params.py` file. Jupyter notebook (`description.ipynb`) will guide you to using this script and give you additional description of the proposed method. At the `plots` folder you will find a visual representation of the script.

### Parameters Description

data_path : str, default: './data'
    The path of files.

measurement_file : str, default: 'MeasuredSignals.csv'
    The filename of measured signal.

reference_file : str, default: 'ReferenceSignal.csv'
    The filename of reference signal.

method : str, default: 'pearson'
    The required method of correlation.
    The following options are available:
    -- 'pearson' : standard correlation coefficient
    -- 'spearman' : Spearman rank correlation

families : list, default: pywt.wavelist()
    The required wavelet families. The default are built-in wavelet families of pywt framework.

probability : bool, default: False
    The method used to compute the probability of an uncorrelated system producing datasets that have a correlation.

alternative : str, default: ‘two-sided’
    Defines the alternative hypothesis. 
    The following options are available:
    -- ‘two-sided’: the correlation is nonzero
    -- ‘less’: the correlation is negative (less than zero)
    -- ‘greater’: the correlation is positive (greater than zero)

correlation_thr : float
    The minimum required correlation.

probability_thr : float
    The minimum required correlation probability.

stepsize : int, default: 20
    The minimum gap between correlated zones. For example, it is required at least 20 timesteps between correlated points to split it as separated correlation zones. 

## Program Return

This script returns the time-series index where measured signal is highly correlated with reference. 

