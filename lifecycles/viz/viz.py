import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from lifecycles import utils
from lifecycles.algorithms.event_analysis import (
    analyze_flow,
    _event_weights_from_flow,
    events_all,
)
from lifecycles.algorithms.measures import event_typicality

__all__ = [
    "plot_flow",
    "plot_event_radar",
    "plot_event_radars",
    "typicality_distribution",
]


def _values_to_idx(links):  # , all_labels):
    df = links[["source", "target"]].copy()
    all_labels = sorted(list(set(links["source"].tolist() + links["target"].tolist())))

    df["source_ID"] = df["source"].apply(lambda x: all_labels.index(x))
    df["target_ID"] = df["target"].apply(lambda x: all_labels.index(x))
    df["value"] = links["value"]
    return df


def _color_links(links, color):
    res = []
    for _, row in links.iterrows():
        if row["source"] == row["target"]:
            res.append("rgba(0,0,0,0.0)")
        elif "X" in row["source"]:
            res.append("rgba(0,0,0,0.02)")
        else:
            res.append(color)
    return res


def _make_sankey(links, color, title, width=500, height=500, colors=None):
    links["color"] = _color_links(links, color=color)
    all_labels = sorted(list(set(links["source"].tolist() + links["target"].tolist())))
    all_x = [int(l.split("_")[0]) for l in all_labels]
    all_x = [(x - min(all_x)) / max(all_x) for x in all_x]
    all_x = [x * 0.8 + 0.1 for x in all_x]
    all_y = [0.5] * len(all_x)

    node_colors = []
    if isinstance(colors, list):
        for l in all_labels:
            if l in colors:
                node_colors.append("green")
            else:
                node_colors.append("lightgrey")

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=10,
                    thickness=15,
                    line=dict(color="darkgray", width=0.2),
                    label=all_labels,
                    x=all_x,
                    y=all_y,
                    color=node_colors,
                    hovertemplate="Group size: %{value}<extra></extra>",
                ),
                link=dict(
                    source=list(
                        (links["source_ID"])
                    ),  # indices correspond to labels, e.g. A1, A2, A1, B1, ...
                    target=list((links["target_ID"])),
                    value=list((links["value"])),
                    color=list((links["color"])),
                    label=list((links["value"])),
                ),
            )
        ]
    )

    # print(fig)
    fig.update_layout(
        font_size=10,
        width=width,
        height=height,
        title={"text": title, "font": {"size": 25}},  # Set the font size here
    )
    fig.show()


def _make_radar(values, categories, rescale, title="", color="green", ax=None):
    pi = 3.14159
    # number of variables
    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles.append(angles[0])  # to close the line
    values = values.copy()
    values.append(values[0])  # to close the line

    # Initialise the spider plot
    # ax = plt.subplot(4,4,row+1, polar=True, )
    if ax is None:
        ax = plt.subplot(
            111,
            polar=True,
        )

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    # plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.set_xticks(angles[:-1], categories, color="blue", size=10)
    # Draw ylabels
    ax.set_rlabel_position(10)
    ticks = list(np.linspace(0, 1, 5))

    ax.set_rticks(ticks, [str(v) for v in ticks], color="grey", size=9)
    ax.grid(True)

    plt.gcf().canvas.draw()

    angles_labels = np.rad2deg(angles)
    angles_labels = [360 - a for a in angles_labels]
    angles_labels = [180 + a if 90 < a < 270 else a for a in angles_labels]
    labels = []
    for label, angle in zip(ax.get_xticklabels(), angles_labels):
        x, y = label.get_position()
        lab = ax.text(
            x,
            y + 0.05,
            label.get_text(),
            transform=label.get_transform(),
            ha=label.get_ha(),
            va=label.get_va(),
            color="grey",
            size=11,
            fontdict={"variant": "small-caps"},
        )
        lab.set_rotation(angle)
        labels.append(lab)
    ax.set_xticklabels([])

    ax.plot(angles, values, color=color, linewidth=1.5, linestyle="solid")

    ax.fill(angles, values, color="red", alpha=0.0)
    if rescale:
        ax.set_rmax(max(values) + 0.1)
    else:
        ax.set_rmax(1)
    ax.set_rmin(0)
    if title != "":
        ax.set_title(title + "\n\n")
    return ax


def plot_flow(lc, node_focus=None, slice=None):
    """
    Plot the flow of a lifecycle

    Args:
        lc (_type_): the lifecycle
        node_focus (_type_, optional): plot only the flows involving this group. Defaults to None.
        slice (_type_, optional): plot only a slice of the lifecycle. Defaults to all.
    """
    if slice is not None:
        lc = lc.slice(*slice)
    links = []
    all_flows = lc.all_flows("+")
    sum_out = 0
    group_size = {}
    for name, flow in all_flows.items():
        nodes_group1 = lc.get_group(name)
        group_size[name] = len(nodes_group1)
        for name2, common in flow.items():
            if node_focus is not None:
                nodes_group2 = lc.get_group(name2)
                if node_focus not in nodes_group2 | nodes_group1:
                    continue
            link = (name, name2, len(common))
            links.append(link)
            sum_out += len(common)

    links_df = pd.DataFrame(links, columns=["source", "target", "value"])
    current_size_source = (
        links_df[["source", "value"]].groupby("source").sum().reset_index()
    )
    current_size_target = (
        links_df[["target", "value"]].groupby("target").sum().reset_index()
    )
    # join the two pd on group
    current_size = current_size_source.merge(
        current_size_target,
        left_on="source",
        right_on="target",
        suffixes=("_source", "_target"),
        how="outer",
    )
    # add column taking the non-null among source and target
    current_size["sourceTarget"] = current_size["source"].fillna(current_size["target"])
    current_size.fillna(0, inplace=True)
    # add a column with the max of source and target
    current_size["max"] = current_size[["value_source", "value_target"]].max(axis=1)
    current_size.set_index("sourceTarget", inplace=True)
    max_input_output = current_size.to_dict()["max"]

    # check the case of groups without a single link
    for name in lc.groups_ids():
        if name not in max_input_output:
            max_input_output[name] = 0

    for name, size in max_input_output.items():
        if size < group_size[name]:  # and (sum_out>0 or node_focus is not None):
            fake_size = group_size[name] - size
            links.append((name, name, fake_size))
    links_df = pd.DataFrame(links, columns=["source", "target", "value"])

    # replace set_name by X_set_name
    # all_labels = list(flow.keys()) + [set_name]
    links_df = _values_to_idx(links_df)

    groups_containing_node = None
    if node_focus is not None:
        groups_containing_node = [
            name for name in all_flows.keys() if node_focus in lc.get_group(name)
        ]

    # print(links)
    _make_sankey(
        links_df,
        color="lightblue",
        title="Flow",
        width=800,
        height=800,
        colors=groups_containing_node,
    )
    # check if fake link needed in target
    # if direction in ["-", "both"] and set_name[0]!="0":
    # if set_name[0]!="0":
    #     n_contributing = sum([len(intersect) for name, intersect in inflow.items()])
    #     if len(target_set) > n_contributing:
    #         fake_size = len(target_set) - n_contributing
    #         #links.append((set_name, set_name, fake_size))
    #         level = int(set_name.split("_")[0])
    #         source = str(level-1) + "_X_"+set_name.split("_")[1]
    #         links.append((source, set_name, fake_size))


def plot_event_radar(
    lc, set_name, direction, min_branch_size=1, rescale=True, color="green", ax=None
):
    data = analyze_flow(
        lc, set_name, direction=direction, min_branch_size=min_branch_size
    )
    a = {set_name: data}
    weights = _event_weights_from_flow(a, direction=direction)
    return _make_radar(
        list(weights[set_name].values()),
        list(weights[set_name].keys()),
        rescale=rescale,
        color=color,
        ax=ax,
    )


def plot_event_radars(lc, set_name, min_branch_size=1, colors=None):
    if colors is None:
        colors = ["green", "red"]
    plot_event_radar(
        lc,
        set_name,
        direction="-",
        min_branch_size=min_branch_size,
        color=colors[0],
        ax=plt.subplot(121, polar=True),
    )
    plot_event_radar(
        lc,
        set_name,
        direction="+",
        min_branch_size=min_branch_size,
        color=colors[1],
        ax=plt.subplot(122, polar=True),
    )
    plt.tight_layout()


def typicality_distribution(lc, direction, width=800, height=500, showlegend=True):
    events = events_all(lc)
    all_specificicities = []
    for group, event in events[direction].items():
        all_specificicities.append(event_typicality(event))
    df = pd.DataFrame(all_specificicities, columns=["event", "event_typicality"])
    # round to 1 decimal so that it works for the histogram
    df["event_typicality"] = df["event_typicality"].apply(lambda x: round(x, 1))
    # replace 1 by 0.99 so that it is included in the last bin
    df["event_typicality"] = df["event_typicality"].apply(
        lambda x: 0.99 if x == 1 else x
    )

    fig = go.Figure()
    for event in df["event"].unique():
        fig.add_trace(
            go.Histogram(
                x=df[df["event"] == event]["event_typicality"],
                name=event,
                opacity=0.75,
                xbins=dict(start=0, end=1.1, size=0.1),
            )
        )

    possible_values = (
        utils.forward_event_names()
        if direction == "+"
        else utils.backward_event_names()
    )

    categories_present = df["event"].unique()
    for category in possible_values:
        if category not in categories_present:
            fig.add_trace(
                go.Histogram(
                    x=[None],
                    name=category,
                    opacity=0.75,
                    xbins=dict(start=0, end=1.1, size=0.1),
                    showlegend=True,
                )
            )  # Empty histogram trace
    for trace in fig.data:
        trace.marker.color = utils.colormap()[trace.name]

    fig.update_layout(showlegend=showlegend)
    fig.update_layout(barmode="stack")

    fig.update_xaxes(range=[0, 1.01], tickvals=np.arange(0, 1.01, 0.1))
    # set figure size
    fig.update_layout(width=width, height=height, template="simple_white")

    return fig
