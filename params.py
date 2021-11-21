SCRIPT_PARAMS = {
    'data_path': './data',
    'measurement_file': 'MeasuredSignals.csv',
    'reference_file': 'ReferenceSignal.csv',
    'method': 'pearson',
    'families': ['bior4.4', 'cgau8', 'cmor1.5-1.0', 'coif4', 'coif7', 'coif9', 'coif14', 'db8', 'fbsp1-1.5-1.0'],
    'probability': True,
    'alternative': 'two-sided',
    'correlation_thr': 0.5,
    'probability_thr': 0.995, 
    'stepsize': 80,
}
