import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def prepare_data(modules, sub_modules, categories, results):
    """
    Prepare data for plotting from the given modules, sub-modules, categories, and results.

    Args:
    modules (list): List of module names.
    sub_modules (list): List of sub-module names.
    categories (list): List of category names.
    results (dict): Nested dictionary with results for each module, sub-module, and category.

    Returns:
    pd.DataFrame: DataFrame containing the prepared data.
    """
    data = []
    for module in modules:
        for sub_module in sub_modules:
            for category in categories:
                value = results[module][sub_module][categories.index(category)]
                data.append([module, sub_module, category, value])
    return pd.DataFrame(data, columns=['Module', 'Sub-Module', 'Category', 'Value'])

def plot_results(df, modules, sub_modules, categories, sample_length, output_filename):
    """
    Plot the results in a bar plot with specified configurations.

    Args:
    df (pd.DataFrame): DataFrame containing the data to plot.
    modules (list): List of module names.
    sub_modules (list): List of sub-module names.
    categories (list): List of category names.
    sample_length (str): Sample length to include in the title.
    output_filename (str): Filename to save the plot.
    """
    # Set the color palette with distinct colors
    palette = sns.color_palette("tab10", len(sub_modules))

    # Plot
    plt.figure(figsize=(14, 8))
    sns.set(style="whitegrid")

    # Create a barplot with thicker columns and distinct colors
    barplot = sns.catplot(
        data=df, x='Category', y='Value', hue='Sub-Module', col='Module', kind='bar',
        palette=palette, height=6, aspect=1, errorbar=None, dodge=True
    )

    # Add the numerical values on top of the bars
    for ax in barplot.axes.flat:
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f'{height * 100:.0f}%',  # Display as percentage with 2 decimal places
                            (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='center',
                            fontsize=12, color='black',
                            xytext=(0, 8),
                            textcoords='offset points')

    # Customize titles and labels for better presentation
    barplot.set_titles("{col_name}", size=20, weight='bold', y=1.00)  # Increased space above module titles
    barplot.set_axis_labels("", "Percentages", fontsize=20, weight='bold')
    barplot.set_xticklabels(rotation=0, horizontalalignment='center', fontsize=18)
    barplot.set_ylabels("Percentages", fontsize=18, weight='normal')

    # Set y-axis to percentage
    for ax in barplot.axes.flat:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x * 100:.0f}%'))
        ax.set_ylim(0, 1.15)  # Set y-axis limit to 105% to avoid bars touching the module titles

    # Remove the default legend
    barplot._legend.remove()

    # Adjust the layout to make room for the legend below
    plt.tight_layout(rect=[0, 0.15, 1, 0.85])  # leave more space at the top for the title

    # Add the legend below the plot
    handles, labels = barplot.axes[0][0].get_legend_handles_labels()
    barplot.fig.subplots_adjust(bottom=0.2, top=0.78)  # Adjust bottom and top space to fit legend and title
    barplot.fig.legend(handles=handles, labels=labels, loc='lower center', ncol=len(sub_modules), fontsize=20)

    # Add a general title above both charts
    plt.suptitle(f"Comparing Models with {sample_length}-Second Samples", fontsize=30, weight='bold', y=0.94)

    # Save the plot as an SVG and PNG file
    barplot.savefig(f"{output_filename}.svg", format="svg")
    barplot.savefig(f"{output_filename}.png", format="png")

    # Show the plot
    plt.show()

def main():

    # Sample data
    modules = ['VGGish', 'OpenL3']
    sub_modules = ['SVM', 'KNN', 'Random Forest']
    categories = ['Recall', 'Precision', 'Accuracy']
    # sample_length = '3'  # Example sample length
    #
    # # Example results (rows for modules, columns for sub-modules and categories)
    # results = {
    #     'VGGish': {
    #         'SVM': [0.84, 0.73, 0.95],
    #         'KNN': [0.02, 0.50, 0.89],
    #         'Random Forest': [0.60, 0.77, 0.93]
    #     },
    #     'OpenL3': {
    #         'SVM': [1.00, 1.00, 1.00],
    #         'KNN': [0.58, 0.83, 0.94],
    #         'Random Forest': [0.98, 0.99, 1.00]
    #     }
    # }

    sample_length = '5'  # Example sample length

    # Example results (rows for modules, columns for sub-modules and categories)
    results = {
        'VGGish': {
            'SVM': [0.73, 0.80, 0.96],
            'KNN': [0.07, 0.67, 0.92],
            'Random Forest': [0.41, 0.86, 0.94]
        },
        'OpenL3': {
            'SVM': [1.00, 1.00, 1.00],
            'KNN': [0.61, 0.86, 0.99],
            'Random Forest': [0.97, 1.00, 1.00]
        }
    }

    # Prepare data for plotting
    df = prepare_data(modules, sub_modules, categories, results)

    # Plot and save results
    plot_results(df, modules, sub_modules, categories, sample_length, "audio_embedding_results_for_5_sec")


if __name__ == "__main__":
    main()
