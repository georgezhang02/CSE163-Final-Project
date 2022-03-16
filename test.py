'''
George Zhang
CSE 163 AD
Tests the importation of COVID data.
'''
import data_processing
from cse163_utils import assert_equals


def test_full_name():
    '''
    Tests the function full_name.
    '''
    assert_equals('Washington', data_processing.full_name('WA'))
    assert_equals(None, data_processing.full_name('test'))
    assert_equals(None, data_processing.full_name(''))


def test_import_population():
    '''
    Tests the function import_population.
    '''
    pop = data_processing.import_population('datasets/nst-est2019-alldata.csv')
    assert_equals(pop[pop['NAME'] == 'Washington']['POPESTIMATE2019'].item(),
                  7614893)
    assert_equals(pop[pop['NAME'] == 'California']['POPESTIMATE2019'].item(),
                  39512223)
    assert_equals(pop[pop['NAME'] == 'New York']['POPESTIMATE2019'].item(),
                  19453561)


def test_import_vaccinations():
    '''
    Tests the function import_vaccinations.
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
    wa = vacs[(vacs['NAME'] == 'Washington') & (vacs['Date'] == '2022-03-11')]
    fully_vaccinated = wa['Series_Complete_Yes'].item()
    pfizer = wa['Series_Complete_Pfizer'].item()
    moderna = wa['Series_Complete_Moderna'].item()
    jj = wa['Series_Complete_Janssen'].item()
    assert_equals(fully_vaccinated, 5461432)
    assert_equals(pfizer, 3122776)
    assert_equals(moderna, 1885282)
    assert_equals(jj, 449439)
    unknown = wa['Series_Complete_Unk_Manuf'].item()
    assert_equals(fully_vaccinated, pfizer + moderna + jj + unknown)


def test_import_cases():
    '''
    Tests the function import_cases.
    '''
    country = data_processing.import_country(
        'datasets/gz_2010_us_040_00_5m.json')
    population = data_processing.import_population(
        'datasets/nst-est2019-alldata.csv')
    state_data = country.merge(population, on='NAME', how='left')
    cases = data_processing.import_cases(
                    'datasets/United_States_COVID-19_Cases_'
                    + 'and_Deaths_by_State_over_Time.csv',
                    state_data)
    wa = cases[(cases['NAME'] == 'Washington') &
               (cases['Date'] == '2022-03-11')]
    total_cases = wa['tot_cases'].item()
    new_cases = wa['new_case'].item()
    assert_equals(total_cases, 1437914)
    assert_equals(new_cases, 1513)


def main():
    '''
    Runs all tests
    '''
    test_full_name()
    test_import_population()
    test_import_vaccinations()
    test_import_cases()


if __name__ == '__main__':
    main()
