import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from lifecycles.flow_analysis import analyze_flow, event_weights


def _values_to_idx(links, all_labels):
    df = links[["source", "target"]].copy()
    df = df.applymap(lambda x: all_labels.index(x))
    df["value"] = links["value"]
    return df


def _color_links(links, color):
    res = []
    for _, row in links.iterrows():
        if row["source"] == row["target"]:
            res.append("white")
        else:
            res.append(color)
    return res


def _make_sankey(links, color, title):
    links["color"] = _color_links(links, color=color)
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=30,
                    thickness=15,
                    line=dict(color="grey", width=0.5),
                    # label=all_labels,
                    color="lightgrey",
                ),
                link=dict(
                    source=list(
                        reversed(links["source"])
                    ),  # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=list(reversed(links["target"])),
                    value=list(reversed(links["value"])),
                    color=list(reversed(links["color"])),
                ),
            )
        ]
    )

    fig.update_layout(
        font_size=10,
        width=500,
        height=500,
        title={"text": title, "font": {"size": 25}},  # Set the font size here
    )
    fig.show()


def _make_radar(values, categories, title="", color="green", ax=None):
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
    # angles = [-a for a in angles]
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
            size=8,
            fontdict={"variant": "small-caps"},
        )
        lab.set_rotation(angle)
        labels.append(lab)
    ax.set_xticklabels([])

    ax.plot(angles, values, color=color, linewidth=1.5, linestyle="solid")

    ax.fill(angles, values, color="red", alpha=0.0)

    ax.set_rmax(1)
    ax.set_rmin(0)
    if title != "":
        ax.set_title(title + "\n\n")
    return ax


def plot_set_flow(
    lc,
    set_name,
    direction="both",
    precomputed_past=None,
    precomputed_future=None,
    min_branch_size=1,
    color="lightblue",
    title=None,
):
    """

    TODO: color according to element attribute
    """
    target_set = lc.get_set(set_name)
    inflow = (
        precomputed_past[set_name]
        if precomputed_past
        else lc.get_set_flow(set_name, direction="-", min_branch_size=min_branch_size)
    )
    outflow = (
        precomputed_future[set_name]
        if precomputed_future
        else lc.get_set_flow(set_name, direction="+", min_branch_size=min_branch_size)
    )
    if direction == "-":
        flow = inflow
    elif direction == "+":
        flow = outflow
    elif direction == "both":
        flow = inflow.copy()
        flow.update(outflow)
    else:
        raise ValueError("direction not in ['-', '+', 'both']")

    all_labels = list(flow.keys()) + [set_name]

    links = []
    for name, common in flow.items():
        l = sorted([name, set_name])
        link = (l[0], l[1], len(common))
        links.append(link)

        # check if fake link needed
        tmp = lc.get_set(name)
        if len(tmp) > len(common):
            fake_size = len(tmp) - len(common)
            links.append((name, name, fake_size))

    # check if fake link needed in target
    if direction in ["-", "both"]:
        n_contributing = sum([len(intersect) for name, intersect in inflow.items()])
        if len(target_set) > n_contributing:
            fake_size = len(target_set) - n_contributing
            links.append((set_name, set_name, fake_size))

    if direction in ["+", "both"]:
        n_spread = sum([len(intersect) for name, intersect in outflow.items()])

        if len(target_set) > n_spread:
            fake_size = len(target_set) - n_spread
            links.append((set_name, set_name, fake_size))

    links = pd.DataFrame(links, columns=["source", "target", "value"])
    links = _values_to_idx(links, all_labels)

    _make_sankey(links, color=color, title=title)


def plot_event_radar(
    lc, set_name, direction, min_branch_size=1, color="green", ax=None
):
    data = analyze_flow(
        lc, set_name, direction=direction, min_branch_size=min_branch_size
    )
    a = {set_name: data}
    weights = event_weights(a, direction=direction)
    return _make_radar(
        list(weights[set_name].values()),
        list(weights[set_name].keys()),
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
