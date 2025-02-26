# coding = 'utf-8'
import numpy as np
import pandas as pd
import time

import target_encoding

def target_mean_v1(data, y_name, x_name):
    result = np.zeros(data.shape[0])
    for i in range(data.shape[0]):
        groupby_result = data[data.index != i].groupby([x_name], as_index=False).agg(['mean', 'count'])
        result[i] = groupby_result.loc[groupby_result.index == data.loc[i, x_name], (y_name, 'mean')]
    return result


def target_mean_v2(data, y_name, x_name):
    result = np.zeros(data.shape[0])
    value_dict = dict()
    count_dict = dict()
    for i in range(data.shape[0]):
        if data.loc[i, x_name] not in value_dict.keys():
            value_dict[data.loc[i, x_name]] = data.loc[i, y_name]
            count_dict[data.loc[i, x_name]] = 1
        else:
            value_dict[data.loc[i, x_name]] += data.loc[i, y_name]
            count_dict[data.loc[i, x_name]] += 1
    for i in range(data.shape[0]):
        result[i] = (value_dict[data.loc[i, x_name]] - data.loc[i, y_name]) / (count_dict[data.loc[i, x_name]] - 1)
    return result


def main():
    y = np.random.randint(2, size=(5000, 1))
    x = np.random.randint(10, size=(5000, 1))
    data = pd.DataFrame(np.concatenate([y, x], axis=1), columns=['y', 'x'])
    
#    start_v1 = time.time()
#    result_1 = target_mean_v1(data, 'y', 'x')
#    end_v1 = time.time()

    start_v2 = time.time()
    result_2 = target_mean_v2(data, 'y', 'x')
    end_v2 = time.time()

    start_v3 = time.time()
    result_3 = target_encoding.target_mean_v3(data, 'y', 'x')
    end_v3 = time.time()

#    print(f'time of v1: {end_v1 - start_v1}')
    print(f'time of v2: {end_v2 - start_v2}')
    print(f'time of v3: {end_v3 - start_v3}')

    #result_2 = target_mean_v2(data, 'y', 'x')
    #diff = np.linalg.norm(result_1 - result_2)
    #print(diff)


if __name__ == '__main__':
    main()
