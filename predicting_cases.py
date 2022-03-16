'''
George Zhang
CSE 163 AD
Predicts new COVID cases in the United States given COVID data.
'''
import data_processing
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor


def parse_ml(cases, vacs=None):
    '''
    Given COVID cases data, returns training features, test features,
    training labels, and test labels. The features datasets contain
    "tot_cases", "POPESTIMATE2019", and "CENSUSAREA"
    (and "Series_Complete_Yes" if COVID vaccination data is provided).
    Also returns a label series that contains "new_case".

    '''
    if vacs is None:
        features = cases[['tot_cases', 'POPESTIMATE2019', 'CENSUSAREA']]
    else:
        features = cases.merge(vacs, on=['NAME', 'Date'])
        features = features[['tot_cases', 'POPESTIMATE2019',
                             'CENSUSAREA', 'Series_Complete_Yes']]
    labels = cases['new_case']
    return train_test_split(features, labels, test_size=0.2)


def predict_cases(cases, vacs):
    '''
    Given COVID cases and vaccination data make predictions with both
    decision tree regressors and neural networks regarding new
    cases using total cases, population, state area, and with and without
    the number of fully vaccinated individuals.
    '''
    tree = DecisionTreeRegressor()
    mlp = MLPRegressor(hidden_layer_sizes=(10), max_iter=200)
    tree_v = 0
    mlp_v = 0
    for i in range(100):
        features_train, features_test, \
            labels_train, labels_test = parse_ml(cases)
        features_train_v, features_test_v, \
            labels_train_v, labels_test_v = parse_ml(cases, vacs)
        tree.fit(features_train, labels_train)
        predictions = tree.predict(features_test)
        tree.fit(features_train_v, labels_train_v)
        predictions_v = tree.predict(features_test_v)
        if mean_squared_error(predictions_v, labels_test_v) \
                < mean_squared_error(predictions, labels_test):
            tree_v += 1
        mlp.fit(features_train, labels_train)
        score = mlp.score(features_test, labels_test)
        mlp.fit(features_train_v, labels_train_v)
        score_v = mlp.score(features_test_v, labels_test_v)
        if score_v > score:
            mlp_v += 1
        print('DecisionTreeRegressor performed better with vaccination data '
              + str(tree_v) + '/' + str(i + 1) + ' times')
        print('Neural Network performed better with vaccination data '
              + str(mlp_v) + '/' + str(i + 1) + ' times')


def main():
    '''
    Runs new COVID cases predictions with data from 2021-01-01 to
    2022-3-11.
    '''
    country = data_processing.import_country(
            'datasets/gz_2010_us_040_00_5m.json')
    population = data_processing.import_population(
            'datasets/nst-est2019-alldata.csv')
    state_data = country.merge(population, on='NAME', how='left')
    vacs = data_processing.import_vaccinations(
                    'datasets/COVID-19_Vaccinations_'
                    + 'in_the_United_States_Jurisdiction.csv',
                    state_data)
    cases = data_processing.import_cases(
                        'datasets/United_States_COVID-19_Cases_'
                        + 'and_Deaths_by_State_over_Time.csv',
                        state_data)
    cases = cases[['Date', 'NAME', 'tot_cases',
                   'POPESTIMATE2019', 'new_case', 'CENSUSAREA']]
    vacs = vacs[['Date', 'NAME', 'Series_Complete_Yes']]
    cases_time = (cases['Date'] >= '2021-01-01') & \
        (cases['Date'] <= '2022-3-11')
    cases_range = cases[cases_time]
    vacs_time = (vacs['Date'] >= '2021-01-01') & (vacs['Date'] <= '2022-3-11')
    vacs_range = vacs[vacs_time]
    predict_cases(cases_range, vacs_range)


if __name__ == '__main__':
    main()
