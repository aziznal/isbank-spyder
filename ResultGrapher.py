# TODO: set this up so it's a general grapher which scrapers inherit from when making their own graphers
import matplotlib.pyplot as plt
import os
import json
import re


# IDEA: show only points that have an absolute deviation of a pre-defined amount in a different color
# TODO: increase data density
# TODO: define what the grapher does in a monthly interval


class ResultGrapher:
    def __init__(self, results_folder_path="results/", time_interval="today",
                 selected_currency='USD'):
        """
        @param results_folder_path: <str> Absolute (or not) path to the results folder
        @param time_period: <str> "today" | "this_month"
        @param selected_currency: <str> Three letter currency code e.g 'USD'
        """
        self.result_folder_path = results_folder_path
        self.time_interval = time_interval
        self.selected_currency = selected_currency

        self.selling_rates = []
        self.buying_rates = []
        self.buy_sell_ratios = []
        self.timestamps = []

        self.__set_axes()

        if self.time_interval == "today":
            self.day, self.starting_date = self.__format_timestamps()

    def __set_axes(self):
        """
        Fills all axes with result data.
        """
        files = os.listdir(self.result_folder_path)

        # files weren't being loaded in proper order
        self.__sort_files(files)

        if len(files) == 0:
            raise Exception("There are no results to load")

        for file in files:
            buy_rate, sell_rate, timestamp = self.__load_result_file(file)
            self.buying_rates.append(buy_rate)
            self.selling_rates.append(sell_rate)
            self.buy_sell_ratios.append(round( 100 - (sell_rate / buy_rate) * 100, 4))
            self.timestamps.append(timestamp)

        self.__check_axes()  # make sure axes are same length

    def __compare_filenames(self, file1, file2):
        """
        compares the index of passed files
        """
        return int(file1.split('_')[1]) < int(file2.split('_')[1])

    def __sort_files(self, _list):
        """
        sorts file list using bubble sort
        """
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(_list) - 1):
                if self.__compare_filenames(_list[i + 1], _list[i]):
                    _list[i], _list[i + 1] = _list[i + 1], _list[i]
                    swapped = True

    def __load_result_file(self, file):

        with open(self.result_folder_path + "/" + file, 'r') as result_file_json:
            result_file = json.load(result_file_json)

            buy_rate = result_file[self.selected_currency]['buying']
            sell_rate = result_file[self.selected_currency]['selling']
            timestamp = result_file['timestamp']

            return buy_rate, sell_rate, timestamp

    def __check_axes(self):
        """
        test method to assert all axes have equal length
        """

        assert all([
            len(self.buying_rates) == len(self.selling_rates),
            len(self.buying_rates) == len(self.timestamps),
            len(self.buying_rates) == len(self.buy_sell_ratios)
        ]), "Warning! Axes length doesn't match!"

    def __format_timestamps(self):
        # each item is in this shape '2020-04-25 Saturday 18:34:47'
        formatted_timestamps = []

        day = self.timestamps[0].split(' ')[1]
        starting_date = self.timestamps[0].split(' ')[0]

        for item in self.timestamps:
            formatted_item = item.split(' ')[-1]    # formatted to HH:MM:SS
            formatted_timestamps.append(formatted_item)

        self.timestamps = formatted_timestamps

        return day, starting_date

    def __format_x_ticks(self, plot):
        # make the x-axis labels prettier
        for i, tick in enumerate(plot.get_xticklabels()):
            tick.set_rotation(-35)
            tick.set_fontsize(8)
            tick.set_fontweight("bold")
            tick.set_horizontalalignment("left")

            # hide every other tick
            if i % 2 != 0:
                tick.set_visible(False)

    def __annotate_plot(self, plot, current_index, y, x=None, color="black", bottom_offset=0):
        if x is None:
            x = self.timestamps
        plot.annotate(
                        y[current_index], (x[current_index], y[current_index]),
                        fontfamily="consolas",
                        fontsize="7",
                        fontweight="bold",
                        horizontalalignment="center",
                        xytext=(x[current_index], y[current_index] + bottom_offset),
                        rotation="15",
                        color=color
                                )

    def __format_rates_plot(self, plot):

        if self.time_interval == 'daily':
            plot.set_xlabel(f"Time")

        plot.set_ylabel('Rates in TL')

        plot.set_title(
            f"Buying and Selling Rates of USD\nDate is {self.day} {self.starting_date}")

        plot.legend()

        # for less out-of-bounds experiences
        plot.set_ylim(min(self.selling_rates) - 0.1, max(self.buying_rates) + 0.1)

        self.__format_x_ticks(plot)
        
        # show points with changed values in a different color
        for i in range(len(self.buying_rates)):

            # Show change in value in a different color
            if i != len(self.buying_rates) - 1:
                if self.buying_rates[i] != self.buying_rates[i + 1]:
                    self.__annotate_plot(plot, i, self.buying_rates, color="#eb7134", bottom_offset=0.02)
                    self.__annotate_plot(plot, i, self.selling_rates, color="#eb7134", bottom_offset=0.02)

                    continue    # to stop the value from getting redrawn
                
            self.__annotate_plot(plot, i, self.buying_rates, bottom_offset=0.02)
            self.__annotate_plot(plot, i, self.selling_rates, bottom_offset=0.02)

    def __format_ratios_plot(self, plot):
        plot.set_title("Difference of Buy Rate vs Sell Rate")
        
        plot.set_ylabel("Percentage %")

        # make the x-axis labels prettier
        self.__format_x_ticks(plot)

        # for less out-of-bounds experiences
        plot.set_ylim(min(self.buy_sell_ratios) - 1, max(self.buy_sell_ratios) + 1)

        # showing point value over each point in graph
        for i in range(len(self.buy_sell_ratios)):

            # show points with changed values in a different color
            if i != len(self.buy_sell_ratios) - 1:
                if self.buy_sell_ratios[i] != self.buy_sell_ratios[i + 1]:
                    self.__annotate_plot(plot, i, self.buy_sell_ratios, color="#eb7134", bottom_offset=0.06)

                    continue    # to stop the value from getting redrawn

            self.__annotate_plot(plot, i, self.buy_sell_ratios, bottom_offset=0.06)

    def create_graph(self, show=False, save=True, save_as=None):
        
        # TODO: add docs for this method

        # figure
        main_fig = plt.figure(figsize=(12, 7))

        # subplots  (2 rows x 1 col)
        rates_plot = main_fig.add_subplot(211)
        rates_ratio_plot = main_fig.add_subplot(212, sharex=rates_plot)

        # region rates_plot

        # Plot Buying Rates
        rates_plot.plot(self.timestamps, self.buying_rates, label="Buying Rate",
                 color="red", marker='o')

        # Plot Selling Rates
        rates_plot.plot(self.timestamps, self.selling_rates, label="Selling Rate",
                 color="blue", marker='o')

        self.__format_rates_plot(rates_plot)

        # endregion rates_plot

        # region rates_ratio_plot
        rates_ratio_plot.plot(self.timestamps, self.buy_sell_ratios,
                 color="green", marker='o', markerfacecolor='green')

        self.__format_ratios_plot(rates_ratio_plot)

        # endregion rates_ratio_plot
        
        plt.tight_layout(pad=2)
        
        if show:
            plt.show()

        if save:
            if self.time_interval == "today":

                if save_as is not None:
                    main_fig.savefig(save_as, dpi=300)
                else:
                    plt.savefig('graphing_results/' +
                                self.starting_date + '.png', dpi=300)

            return self.starting_date + '.png'


# grapher = ResultGrapher("results\\2020-04-30\\")

# grapher.create_graph(show=True, save=True, save_as='graphing_results\\test_fig2.png')


