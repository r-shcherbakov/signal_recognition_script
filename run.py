import importlib
import numpy as np
import pandas as pd
import pprint
import pywt
from tqdm import tqdm
from scipy import stats
from termcolor import colored


PARAMS_NAME = 'params'


def get_params(params_name):
    '''
    Given a filename, assumes a matching params python module exists within
    the directory and attempts to import it.
    :param fileName: filename, used to guess the script params name.
    :return: params dictionary
    '''
    import_name = params_name
    print(f'Importing script params from {import_name}')
    try:
        script_params = importlib.import_module(import_name).SCRIPT_PARAMS
        #print('Model parameters:')
        #pprint.pprint(script_params, depth=2, sort_dicts=False)
        print()
    except ImportError:
        raise Exception(f'No script params exist for {params_name}!')
    return script_params


def get_data(data_path, measurement_file, reference_file):
    '''
    Given a filename of signal and reference, assumes data exists within
    the directory and attempts to read it.
    :param data_path: path of files.
    :param measurement_file: filename.
    :param reference_file: filename.
    :return: pandas DataFrame
    '''
    measurement_path = f'{data_path}/{measurement_file}'
    reference_path = f'{data_path}/{reference_file}'
    print(f'Importing data...')
    print()
    try:
        measurement = pd.read_csv(measurement_path)
        reference = pd.read_csv(reference_path)
    except:
        raise Exception(f'No data exist for {data_path}!')
    return measurement, reference


# This func eleminate the noise from measured signal
def madev(d, axis=None):
    ''' Mean absolute deviation of a signal '''
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


def wavelet_denoising(x, wavelet='db4', level=1):
    coeff = pywt.wavedec(x, wavelet, mode='per')
    sigma = (1/0.6745) * madev(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')


# Compute the correlation between the reference and denoised signal through moving window
def corr_func(signal, reference, method='pearson', families=pywt.wavelist(), 
              probability=False, alternative='two-sided'):
    
    length = len(signal)
    window = len(reference)
    df = pd.DataFrame(index=range(0,length-window))
    
    for wav in tqdm(families):
        try:
            filtered = wavelet_denoising(signal, wavelet=wav, level=1)
        except:
            pass
        
        rolling_r = []
        for i in range(0,(length-window)):
            if method == 'pearson':
                if probability:
                    correl = 1 - stats.pearsonr(filtered[i:i+window], reference)[1]
                else:
                    correl = stats.pearsonr(filtered[i:i+window], reference)[0]
            elif method == 'spearman':
                if probability:
                    try:
                        correl = stats.spearmanr(filtered[i:i+window], reference, alternative=alternative)[1]
                    except:
                        correl = 0
                else:
                    correl = stats.spearmanr(filtered[i:i+window], reference)[0]
            else:
                raise ValueError('Unexpected method')

            if np.isnan(correl):
                rolling_r.append(0)
            else: 
                rolling_r.append(correl)         

        df[f'{wav}'] = rolling_r 
    df['mean'] = df.mean(axis=1)
    return df


# Convert input data to array, split the indexes of highly correlated zones
def find_indexes(measurement, reference):
    print('Calculating the correlation...')
    print()
    for column in measurement.columns:
        signal = measurement[column].values
        window = len(reference)
        df = [f'correlation_{column}'] 
        df = corr_func(signal, reference, 
                       families=script_params['families'], 
                       probability=script_params['probability'])
        print()
        print(f'Correlation of ', colored(f'{column}', 'blue'), 'calculated!')
        print()

        if script_params['probability']:
            indexes = df['mean'][df['mean'] > script_params['probability_thr']].index
            print(f'The time-series index where', colored(f'{column}', 'blue'), 'is highly correlated with reference:')
            for timestep in consecutive(indexes):
                left_corner = timestep[0]
                right_corner = timestep[-1]
                print(f'from', colored(f'{left_corner}', 'blue', attrs=['bold', 'underline']), 
                'to', colored(f'{right_corner+window}', 'blue', attrs=['bold', 'underline']), 'timestep')
        else:
            indexes = df['mean'][df['mean'] > script_params['correlation_thr']].index
            print(f'The time-series index where', colored(f'{column}', 'blue'), 'is highly correlated with reference:')
            for timestep in consecutive(indexes):
                left_corner = timestep[0]
                right_corner = timestep[-1]
                print(f'from', colored(f'{left_corner}', 'blue', attrs=['bold', 'underline']), 
                'to', colored(f'{right_corner+window}', 'blue', attrs=['bold', 'underline']), 'timestep')  
        print()      


# Split the different correlation zones
def consecutive(data, stepsize=20):
    return np.split(data, np.where(np.diff(data) > stepsize)[0]+1)


script_params = get_params(PARAMS_NAME)
measurement, reference = get_data(script_params['data_path'],
                                  script_params['measurement_file'],
                                  script_params['reference_file'],
                                 )      


# Drop the NaN values and convert reference to array
reference = reference.drop(['Unnamed: 1', 'Unnamed: 2'], axis=1).dropna(axis=0)
reference = reference.SourceSignal.to_numpy()


# Print the time-series index where measured signal is highly correlated with reference.
find_indexes(measurement, reference)



  





