import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def prepare_data(audio_files, metrics, results):
    """
    Prepare data for plotting from the given audio files, metrics, and results.

    Args:
    audio_files (list): List of audio file descriptions.
    metrics (list): List of metric names.
    results (dict): Dictionary with results for each audio file and metric.

    Returns:
    pd.DataFrame: DataFrame containing the prepared data.
    """
    data = []
    for audio_file in audio_files:
        for metric in metrics:
            value = results[audio_file][metrics.index(metric)]
            data.append([audio_file, metric, value])
    return pd.DataFrame(data, columns=['Audio File', 'Metric', 'Value'])

def plot_results(df, audio_files, metrics, sample_length, output_filename):
    """
    Plot the results in a bar plot with specified configurations.

    Args:
    df (pd.DataFrame): DataFrame containing the data to plot.
    audio_files (list): List of audio file descriptions.
    metrics (list): List of metric names.
    sample_length (str): Sample length to include in the title.
    output_filename (str): Filename to save the plot.
    """
    # Set the color palette with distinct colors
    palette = sns.color_palette("tab10", len(audio_files))

    # Plot
    plt.figure(figsize=(14, 8))
    sns.set(style="whitegrid")

    # Create a barplot with thicker columns and distinct colors
    barplot = sns.catplot(
        data=df, x='Metric', y='Value', hue='Audio File', kind='bar',
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
    barplot.set_axis_labels("", "Percentages", fontsize=20, weight='bold')
    barplot.set_xticklabels(rotation=0, horizontalalignment='center', fontsize=18)
    barplot.set_ylabels("Percentages", fontsize=18, weight='normal')

    # Set y-axis to percentage
    for ax in barplot.axes.flat:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x * 100:.0f}%'))
        ax.set_ylim(0, 1.15)  # Set y-axis limit to 115% to avoid bars touching the top

    # Remove the default legend
    barplot._legend.remove()

    # Adjust the layout to make room for the legend below
    plt.tight_layout(rect=[0, 0.15, 1, 0.85])  # leave more space at the top for the title

    # Add the legend below the plot
    handles, labels = barplot.axes[0][0].get_legend_handles_labels()
    barplot.fig.subplots_adjust(bottom=0.2, top=0.85)  # Adjust bottom and top space to fit legend and title
    barplot.fig.legend(handles=handles, labels=labels, loc='lower center', ncol=len(audio_files), fontsize=16)

    # Add a general title above the chart
    plt.suptitle(f"Performance Metrics for {sample_length}-Second Audio Samples", fontsize=20, weight='bold', y=0.94)

    # Save the plot as an SVG and PNG file
    barplot.savefig(f"{output_filename}.svg", format="svg")
    barplot.savefig(f"{output_filename}.png", format="png")

    # Show the plot
    plt.show()

def main():

    # Sample data
    audio_files = ['Radio Show', 'Podcast 1', 'Podcast 2']
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    sample_length = '3'  # Example sample length

    # Example results (rows for audio files, columns for metrics)
    results = {
        'Radio Show': [0.74, 0.66, 0.38, 0.48],
        'Podcast 1': [0.69, 0.46, 0.95, 0.62],
        'Podcast 2': [0.77, 0.38, 0.91, 0.54]
    }

    # Prepare data for plotting
    df = prepare_data(audio_files, metrics, results)

    # Plot and save results
    plot_results(df, audio_files, metrics, sample_length, "audio_file_metrics_for_3_sec")


if __name__ == "__main__":
    main()
