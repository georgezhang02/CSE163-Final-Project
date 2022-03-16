'''
George Zhang
CSE 163 AD
Analyses the COVID cases and vaccinations in the United States.
'''
import data_processing
import matplotlib.pyplot as plt
import numpy as np


def plot_vaccinations(vacs):
    '''
    Given COVID vaccination data, plots the distribution of fully vaccinated
    individuals in the U.S.
    Also plots the distribution of vaccine made by each manufacturer
    (Janssen/J&J, Moderna, and Pfizer) and the most popular manufacturer.
    '''
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    vacs.plot(ax=axs[0, 1], column='Series_Complete_Pop_Pct', legend=True)
    axs[0, 1].set_title('Fully Vaccinated (%)')
    vacs['J_per'] = vacs['Series_Complete_Janssen'] / \
        vacs['POPESTIMATE2019'] * 100
    vacs['M_per'] = vacs['Series_Complete_Moderna'] / \
        vacs['POPESTIMATE2019'] * 100
    vacs['P_per'] = vacs['Series_Complete_Pfizer'] / \
        vacs['POPESTIMATE2019'] * 100
    vacs.plot(ax=axs[0, 0], column='J_per', legend=True)
    axs[0, 0].set_title('Fully Vaccinated by Janssen/J&J (%)')
    vacs.plot(ax=axs[1, 0], column='M_per', legend=True)
    axs[1, 0].set_title('Fully Vaccinated by Moderna (%)')
    vacs.plot(ax=axs[2, 0], column='P_per', legend=True)
    axs[2, 0].set_title('Fully Vaccinated by Pfizer (%)')
    vacs['max'] = vacs[['J_per', 'M_per', 'P_per']].max(axis=1)
    vacs[vacs['J_per'] == vacs['max']].plot(ax=axs[1, 1], color='#FF0000')
    vacs[vacs['M_per'] == vacs['max']].plot(ax=axs[1, 1], color='#00FF00')
    vacs[vacs['P_per'] == vacs['max']].plot(ax=axs[1, 1], color='#0000FF')
    axs[1, 1].set_title('Most Popular Vaccine Manufacturer (Blue = Pfizer)')
    axs[2, 1].axis('off')
    fig.savefig('outputs/vaccinations.png')


def plot_cases(cases, vacs, filename):
    '''
    Given COVID cases and vaccination data, plots the distribution of
    cases/population, deaths/population, mortality rate,
    transmission rate, and fully vaccinated percentage in the U.S.
    Save each plot as the given [filename].png in the outputs folder.
    '''
    cases = cases.dissolve(by='NAME', aggfunc='mean')
    cases['cases_per'] = cases['tot_cases'] / cases['POPESTIMATE2019'] * 100
    cases['deaths_per'] = cases['tot_death'] / cases['POPESTIMATE2019'] * 100
    cases['mortality'] = cases['tot_death'] / cases['tot_cases'] * 100
    cases['transmission'] = cases['new_case'] / cases['tot_cases'] * 100
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    cases.plot(ax=axs[0, 0], column='cases_per', legend=True)
    axs[0, 0].set_title('Cases per Population (%)')
    cases.plot(ax=axs[1, 0], column='deaths_per', legend=True)
    axs[1, 0].set_title('Deaths per Population (%)')
    cases.plot(ax=axs[2, 0], column='mortality', legend=True)
    axs[2, 0].set_title('Mortality Rate (%)')
    cases.plot(ax=axs[0, 1], column='transmission', legend=True)
    axs[0, 1].set_title('Transmission Rate (New / Total Cases) (%)')
    vacs.plot(ax=axs[1, 1], column='Series_Complete_Pop_Pct', legend=True)
    axs[1, 1].set_title('Fully Vaccinated (%)')
    axs[2, 1].axis('off')
    fig.savefig('outputs/' + filename + '.png')


def plot_stats(vacs, cases):
    '''
    Given COVID cases and vaccination data, plots the distribution of COVID
    statistics at different times
    (2 plots each for the alpha, delta, and omicron variant).
    '''
    start_date = ['2021-01-01', '2021-05-01', '2021-08-01',
                  '2021-10-01', '2021-12-01', '2022-03-01']
    output_name = ['2021-01-alpha1', '2021-05-alpha2', '2021-08-delta1',
                   '2021-10-delta2', '2021-12-omicron1', '2022-03-omicron2']
    for date, name in zip(start_date, output_name):
        cases_time = (cases['Date'] >= date) & \
            (cases['Date'] <= (date[0:-1] + '7'))
        cases_range = cases[cases_time]
        vacs_time = vacs['Date'] == date
        vacs_day = vacs[vacs_time]
        plot_cases(cases_range, vacs_day, name)


def plot_washington(cases):
    '''
    Given COVID cases data in Washington State, plots new cases against
    total cases at different time ranges on the logarithmic scale.
    '''
    x = cases[['Date', 'tot_cases']]
    y = cases[['Date', 'new_case']]
    time_range = ['2020-01-21', '2021-01-01', '2021-05-01', '2021-08-01',
                  '2021-10-01', '2021-12-01', '2022-03-11']
    colors = ['black', 'green', 'black', 'orange', 'black', 'red']
    label = [None, 'Vaccines', None, 'Delta', None, 'Omicron']
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for i in range(len(time_range) - 1):
        x_range = (x['Date'] >= time_range[i]) & \
             (x['Date'] < time_range[i + 1])
        x_part = np.log10(x[x_range]['tot_cases'])
        y_range = (y['Date'] >= time_range[i]) & \
            (y['Date'] < time_range[i + 1])
        y_part = np.log10(y[y_range]['new_case'])
        ax1.scatter(x_part, y_part, s=3, color=colors[i], label=label[i])
    plt.title('New Cases vs Total Cases in Washington State (Log 10)')
    plt.xlabel('Total Cases (Log 10)')
    plt.ylabel('New Cases (Log 10)')
    plt.legend(loc='upper left')
    plt.savefig('outputs/washington.png')


def main():
    '''
    Runs all analyses.
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
    recent_vacs = vacs[vacs['Date'] == '2022-03-11']
    plot_vaccinations(recent_vacs)
    plot_stats(vacs, cases)
    washington_cases = cases[cases['NAME'] == 'Washington']
    plot_washington(washington_cases)


if __name__ == '__main__':
    main()
