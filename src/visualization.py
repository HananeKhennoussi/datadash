import matplotlib.pyplot as plt
import seaborn as sns

def plot_scatter(df, x_axis, y_axis):
    fig, ax = plt.subplots()
    ax.scatter(df[x_axis], df[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{y_axis} vs {x_axis}")
    return fig

def plot_histogram(df, column):
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=30, color="skyblue", edgecolor="black")
    ax.set_title(f"Distribution de {column}")
    return fig

def plot_correlation(df, numeric_cols):
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Matrice de corrélation")
    return fig

def plot_box(df, column):
    fig, ax = plt.subplots()
    sns.boxplot(y=df[column], ax=ax)
    ax.set_title(f"Boxplot de {column}")
    return fig

