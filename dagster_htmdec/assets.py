from dagster import asset
from pandas import DataFrame, read_html, get_dummies
from sklearn.linear_model import LinearRegression as Regression


@asset
def country_stats() -> DataFrame:
    df = read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]
    df.columns = [
        "country",
        "continent",
        "subregion",
        "pop_20220701",
        "pop_20230701",
        "pop_change",
    ]
    df["pop_change"] = df["pop_change"].str.replace("−", "-")
    df["pop_change"] = df["pop_change"].str.rstrip("%").astype("float")
    return df


@asset
def change_model(country_stats: DataFrame) -> Regression:
    data = country_stats.dropna(subset=["pop_change"])
    dummies = get_dummies(data[["continent"]])
    return Regression().fit(dummies, data["pop_change"])


@asset
def continent_stats(country_stats: DataFrame, change_model: Regression) -> DataFrame:
    result = country_stats.groupby("continent").sum()
    result["pop_change_factor"] = change_model.coef_
    return result
