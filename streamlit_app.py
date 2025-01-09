import streamlit as st
import plotly.graph_objects as go
from matplotlib import colors
import numpy as np

nl = "\n"

data = dict()

data["node"] = dict()
data["link"] = dict()

node_keys = ["label", "color"]
for item in node_keys:
    data["node"][item] = list()

link_keys = ["source", "target", "value", "label", "color"]
for item in link_keys:
    data["link"][item] = list()

data["node"]["label"] = [
    "Applications",  # 0
    "Cold",  # 1
    "Referral",  # 2
    "Not Selected",  # 3
    "No Response",  # 4
    "Screening",  # 5
    "Interview",  # 6
    "Interview 2",  # 7
    "Interview 3+",  # 8
    "Offer",  # 9,
    "Invitation",  # 10
]
data["node"]["color"] = [
    "grey",
    "blue",
    "plum",
    "red",
    "steelblue",
    "teal",
    "darkseagreen",
    "seagreen",
    "seagreen",
    "forestgreen",
    "lawngreen",
]

total_apps = st.number_input("Number of Applications", value=0)

valid_pairs = [
    ("Applications", "Cold"),
    ("Applications", "Referral"),
    ("Cold", "Not Selected"),
    ("Referral", "Not Selected"),
    ("Cold", "No Response"),
    ("Referral", "No Response"),
    ("Cold", "Invitation"),
    ("Referral", "Invitation"),
    ("Invitation", "Screening"),
    ("Invitation", "Interview"),
    ("Screening", "Interview"),
    ("Screening", "Not Selected"),
    ("Interview", "Not Selected"),
    ("Interview", "Interview 2"),
    ("Interview", "Offer"),
    ("Interview 2", "Not Selected"),
    ("Interview 2", "Interview 3+"),
    ("Interview 2", "Offer"),
    ("Interview 3+", "Not Selected"),
    ("Interview 3+", "Offer"),
    # ("Not Selected", ""),
    # ("No Response", "")
]
pairs = []
nlabel = len(data["node"]["label"])

for pair in valid_pairs[:-2]:
    pair_idx = [
        pair,
        (data["node"]["label"].index(pair[0]), data["node"]["label"].index(pair[1])),
    ]
    pairs.append(pair_idx)
# st.write(pairs)
st.divider()
left, right = st.columns(2)
for pair in pairs:

    include_pair = left.checkbox(f"{pair[0][0]} --> {pair[0][1]}")
    if include_pair:
        pair_value = right.number_input(
            f"Number ({pair[0][0]}, {pair[0][1]}): ", value=0, max_value=total_apps
        )
        data["link"]["source"].append(pair[1][0])
        data["link"]["target"].append(pair[1][1])
        data["link"]["value"].append(pair_value)
        data["link"]["color"].append(data["node"]["color"][pair[1][1]])
    # cols = st.columns(2)
    # cols[0].divider()
    # cols[1].divider()
annotated_labels = [f"{data['node']['label'][0]} <br> ({total_apps})"]
# data["link"]["source"].append(data["node"]['label'].index("Not Selected"))
# data["link"]["target"].append(10)
# data["link"]["value"].append(1e-20)
# data["link"]["color"].append("white")
# data["link"]["source"].append(data["node"]['label'].index("No Response"))
# data["link"]["target"].append(10)
# data["link"]["value"].append(10e-10)
# data["link"]["color"].append("white")
for label in data["node"]["label"][1:]:
    idx = data["node"]["label"].index(label)
    total = 0
    for i, target in enumerate(data["link"]["target"]):
        if idx == target:
            total += data["link"]["value"][i]
    annotated_labels.append(
        f"{label} <br>     ({total}, {int(100 * np.round(total/total_apps, 2))}%)"
    )

fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=80,
                thickness=30,
                align="justify",
                line=dict(color="black", width=0.5),
                label=annotated_labels,  # data["node"]["label"],
                color=data["node"]["color"],
            ),
            link=dict(
                arrowlen=15,
                source=data["link"]["source"],
                target=data["link"]["target"],
                value=data["link"]["value"],
                color=[
                    f"rgba{colors.to_rgba(c, alpha=0.5)}" for c in data["link"]["color"]
                ],
            ),
        )
    ]
)

title_font_size = st.number_input(
    "Title Font Size:", value=28, min_value=8, max_value=40
)
font_size = st.number_input("Label Font Size:", value=22, min_value=8, max_value=40)
title_text = st.text_input("Plot Title:", value="Job Applications Sankey Diagram")
# fig_width = st.number_input("Figure Width:", value=750, step=50)
# fig_height = st.number_input("Figure Height:", value=450, step=50)
fig.update_layout(
    title_text=title_text,
    title_font_size=28,
    font_size=font_size,  # height=fig_height, width=fig_width
)

st.plotly_chart(fig)
