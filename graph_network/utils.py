import pandas as pd
import numpy as np
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network


def save_as_json(pandas_dataframe, file_name):
    """
    Save a pandas DataFrame to a JSON file with the current date appended to the filename.

    Args:
    pandas_dataframe (pd.DataFrame): The DataFrame to save.
    file_name (str): The base name of the file to save.
    """
    import datetime

    date_info = datetime.datetime.now().strftime("%d-%m-%y")
    pandas_dataframe.to_json(f"{file_name}_{date_info}.json", orient="records")


# def rgba_to_hex(rgba):
#     """Hilfsfunktion, die RGBA zu einem Hex-Farbcode konvertiert."""
#     # Stellen Sie sicher, dass die RGBA-Liste korrekt ist
#     try:
#         if isinstance(rgba, (list, tuple)) and len(rgba) == 4:
#             return "#{:02x}{:02x}{:02x}".format(
#                 int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)
#             )
#     except TypeError:
#         pass  # Wenn ein Fehler auftritt, wird Grau zurückgegeben.
#     return "#2e2e2e"


# def convert_rgba_to_hex(df, columns):
#     for column in columns:
#         if column in df.columns:
#             df[column] = df[column].apply(
#                 lambda x: (
#                     rgba_to_hex(x)
#                     if isinstance(x, (list, tuple)) and len(x) == 4
#                     else "#2e2e2e"
#                 )
#             )
#         else:
#             print(f"Warnung: Die Spalte '{column}' existiert nicht im DataFrame.")
#     return df


# cluster_data_with_matrix = convert_rgba_to_hex(cluster_data_with_matrix, ['color_cluster', 'color_cluster-db', 'color_cluster-h', 'color_scc_id', 'color_wcc_id', 'color_louvain_id', 'color_tf-idf_kmeans'])


def get_graph_from_matrix_customized_color(matrix_df, color_col="color"):
    import networkx as nx
    from pyvis.network import Network

    G = nx.DiGraph()
    for idx, row in matrix_df.iterrows():
        G.add_node(row["url"], color=row[color_col], size=120)
        start_node = row["url"]
        for column in matrix_df.columns:
            if matrix_df.loc[idx, column] == True:
                end_node = column
                G.add_edge(start_node, end_node, color="#87edec")

    N = Network(
        height="1500px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True,
        notebook=False,
    )
    N.barnes_hut(
        gravity=-80000,
        central_gravity=0.3,
        spring_length=250,
        spring_strength=0.001,
        damping=0.09,
        overlap=0,
    )
    N.from_nx(G)

    N.show_buttons()

    for node in N.nodes:
        node_id = node["id"]
        node["color"] = G.nodes[node_id].get("color", "gray")
    #     node["title"] = "    Neighbors:<br>" + "<br>".join(neighbor_map[node[""]])

    return G, N


# def get_graph_from_cluster_data(matrix_df, cluster_data, cluster_id_col):
#     color_col = f"color_{cluster_id_col}"
#     cluster_matrix = pd.merge(
#         matrix_df,
#         cluster_data[["url", cluster_id_col, color_col]],
#         how="left",
#         on=["url"],
#     )
#     cluster_matrix = convert_rgba_to_hex(cluster_matrix, [color_col])
#     return get_graph_from_matrix_customer_color(cluster_matrix, color_col)


def get_graph_from_cluster_data_without_color(matrix_df, cluster_data, cluster_id_col):
    color_col = f"color_{cluster_id_col}"
    cluster_matrix = pd.merge(
        matrix_df,
        cluster_data[["url", cluster_id_col, color_col]],
        how="left",
        on=["url"],
    )
    return get_graph_from_matrix_customer_color(cluster_matrix, color_col)


def append_cluster_color(df, cluster_col, specific_colors):
    import matplotlib.colors as mcolors

    cluster_sizes = df[cluster_col].value_counts().sort_index()
    cmap = plt.get_cmap("hsv")
    num_of_clusters = len(cluster_sizes)

    generic_colors = [
        cmap(i / (num_of_clusters - len(specific_colors)))
        for i in range(num_of_clusters - len(specific_colors))
    ]
    generic_colors = [mcolors.to_hex(color) for color in generic_colors]

    color_mapping = {}
    generic_color_index = 0
    for cluster_id in cluster_sizes.index:
        if cluster_id in specific_colors:
            color_mapping[cluster_id] = specific_colors[cluster_id]
        else:
            color_mapping[cluster_id] = generic_colors[generic_color_index]
            generic_color_index += 1
    df[f"color_{cluster_col}"] = df[cluster_col].apply(lambda x: color_mapping[x])


def get_cluster_plot(pandas_df, cluster_col):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    color_col = f"color_{cluster_col}"
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        pandas_df["negative"],
        pandas_df["neutral"],
        pandas_df["positive"],
        c=pandas_df[color_col],
    )
    ax.set_xlabel("Negative")
    ax.set_ylabel("Neutral")
    ax.set_zlabel("Positive")
    ax.set_box_aspect(aspect=None, zoom=0.95)
    plt.show()


# def get_correlation_df_per_cluster(df, cluster_col):
#     coefficient_names = ["negative", "neutral", "positive"]

#     std_dev = df.groupby(cluster_col)[coefficient_names].std()
#     usable_values = std_dev[(std_dev["neutral"].notnull()) & (std_dev["neutral"] != 0)]
#     pages = df[df[cluster_col].isin(usable_values.index)][
#         [cluster_col, "negative", "neutral", "positive"]
#     ].shape[0]
#     print(
#         "Number of Clusters that we can calculate the correlation:",
#         usable_values.shape[0],
#         "\n containing:",
#         pages,
#         "Pages/Nodes.",
#     )

#     mean_coeffs = (
#         df[df[cluster_col].isin(usable_values.index)]
#         .groupby(cluster_col)[coefficient_names]
#         .mean()
#         .reset_index()
#     )

#     correlation_matrix_per_cluster = (
#         df[df[cluster_col].isin(usable_values.index)][
#             [cluster_col, "negative", "neutral", "positive"]
#         ]
#         .groupby(cluster_col)[coefficient_names]
#         .corr()
#     )

#     for name in coefficient_names:
#         mean_coeffs.rename(columns={name: f"avgc_{name}"}, inplace=True)
#     correlation_of_mean_sentiment_per_cluster = mean_coeffs[
#         ["avgc_negative", "avgc_neutral", "avgc_positive"]
#     ].corr()

#     return correlation_of_mean_sentiment_per_cluster, correlation_matrix_per_cluster


def get_usable_clusters(df, cluster_col, coefficient_names):
    std_dev = df.groupby(cluster_col)[coefficient_names].std()
    return std_dev[(std_dev["neutral"].notnull()) & (std_dev["neutral"] != 0)]


def get_cluster_overview(df, cluster_col):
    coefficient_names = ["negative", "neutral", "positive"]
    usable_values = get_usable_clusters(df, cluster_col, coefficient_names)
    pages = df[df[cluster_col].isin(usable_values.index)][
        [cluster_col, "negative", "neutral", "positive"]
    ].shape[0]
    print(
        "Number of Clusters that we can calculate the correlation:",
        usable_values.shape[0],
        "\n containing:",
        pages,
        "Pages/Nodes.",
    )
    cluster_sizes = (
        df[df[cluster_col].isin(usable_values.index)].groupby(cluster_col).size()
    )

    mean_coeffs = (
        df[df[cluster_col].isin(usable_values.index)]
        .groupby(cluster_col)[coefficient_names]
        .mean()
    )
    mean_coeffs[f"{cluster_col[:-3]}_size"] = cluster_sizes
    mean_coeffs.rename(
        columns={name: f"avg_{name[:3]}" for name in coefficient_names}, inplace=True
    )
    ndf = (
        pd.merge(
            mean_coeffs.reset_index(),
            df[[cluster_col, f"color_{cluster_col}"]].drop_duplicates(),
            on=cluster_col,
            how="left",
        )
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return ndf[
        [
            cluster_col,
            "avg_neg",
            "avg_neu",
            "avg_pos",
            f"{cluster_col[:-3]}_size",
            f"color_{cluster_col}",
        ]
    ].sort_values(f"{cluster_col[:-3]}_size", ascending=False)


def append_mean_coefficients_per_cluster(df, cluster_col):
    coefficient_names = ["negative", "neutral", "positive"]
    usable_values = get_usable_clusters(df, cluster_col, coefficient_names)
    cluster_sizes = df[cluster_col].value_counts()
    large_clusters = cluster_sizes[cluster_sizes >= 10].index
    mean_coeffs = (
        df[
            (df[cluster_col].isin(usable_values.index))
            & (df[cluster_col].isin(large_clusters))
        ]
        .groupby(cluster_col)[coefficient_names]
        .mean()
        .reset_index()
    )
    mean_coeffs.rename(
        columns={name: f"avg_cluster_{name[:3]}" for name in coefficient_names},
        inplace=True,
    )
    df = pd.merge(df, mean_coeffs, on=cluster_col, how="left")

    return df


def get_mean_sentiment_corr(df, cluster_col):
    print(
        "Num of Pages for Analysis:\n",
        append_mean_coefficients_per_cluster(df, cluster_col)
        .dropna(subset=["avg_cluster_neu"])
        .shape[0],
    )
    print(
        "Num of Clusters for Analysis:\n",
        append_mean_coefficients_per_cluster(df, cluster_col)
        .dropna(subset=["avg_cluster_neu"])[cluster_col]
        .value_counts()
        .shape[0],
    )
    return append_mean_coefficients_per_cluster(df, cluster_col)[
        [
            "negative",
            "neutral",
            "positive",
            "avg_cluster_neg",
            "avg_cluster_neu",
            "avg_cluster_pos",
        ]
    ].corr()[["negative", "neutral", "positive"]][3:6]
