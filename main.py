import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from io import StringIO


MALAYSIA_DATA_URL = "https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv"
STATE_DATA_URL = "https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv"

CATEGORYARRAY = [
    "W.P. Putrajaya",
    "W.P. Labuan",
    "Terengganu",
    "Selangor",
    "Sarawak",
    "Sabah",
    "Pulau Pinang",
    "Perlis",
    "Perak",
    "Pahang",
    "Negeri Sembilan",
    "Melaka",
    "Kelantan",
    "Kedah",
    "Johor",
]


def fetch_csv(data_url: str) -> pd.DataFrame:
    r = requests.get(data_url)
    return pd.read_csv(StringIO(r.text))


def clean(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.set_index(["date", "state"])
        .loc[:, ["dose1_cumul", "dose2_cumul", "total_cumul"]]
        .sort_values(by="total_cumul", ascending=False)
        .sort_index(level="date", sort_remaining=False)
        .reset_index()
    )


def plot_cumulative_state(df: pd.DataFrame, outfile: str):
    fig = px.bar(
        state_data,
        x="state",
        y=["dose1_cumul", "dose2_cumul"],
        animation_frame="date",
        animation_group="state",
        labels={"value": "Total vaccinated", "state": "", "variable": "Dose Type"},
        title="Vaccination Count in Malaysia by State",
    )

    fig.write_html(outfile)


if __name__ == "__main__":
    state_data = fetch_csv(STATE_DATA_URL)
    state_data = clean(state_data)

    plot_cumulative_state(state_data, "index.html")
