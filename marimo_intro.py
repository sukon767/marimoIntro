import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Create sliders
    """)
    return


@app.cell
def _(mo):
    parameters = mo.ui.dictionary(
        {
        "N": mo.ui.slider(start=1, stop=100, value = 10),
        "sigma": mo.ui.slider(start=0, stop=10, step = 0.1, value = 1),  
        "seed": mo.ui.slider(start=0, stop=100),
        "window size": mo.ui.slider(start=1, stop=100, value = 5)
        }
    )
    return (parameters,)


@app.cell
def _(parameters):
    parameters
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Compute all of our columns
    """)
    return


@app.cell
def _(np, parameters):
    rng = np.random.default_rng(parameters["seed"].value)
    return (rng,)


@app.cell
def _(parameters, pl, rng):
    delta = rng.normal(0, parameters["sigma"].value, parameters["N"].value)
    prices = pl.concat([pl.Series("prices", [100.0]), pl.Series("prices", delta).cum_sum() + 100])
    return (prices,)


@app.cell
def _(parameters, prices):
    wsz = min(len(prices), parameters["window size"].value)
    average = prices.rolling_mean(wsz, min_samples=1).alias("average")
    return (average,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Create the desired dataframe
    """)
    return


@app.cell
def _(average, parameters, pl, prices):
    df = pl.DataFrame().with_columns(pl.Series("t", range(parameters["N"].value+1)), prices, average)
    return (df,)


@app.cell
def _(df, mo):
    mo.md(f"""
    {mo.as_html(df)}
    """)
    return


@app.cell
def _(df, plt):
    fig, ax = plt.subplots()
    ax.plot(df["t"], df["prices"], label="Price")
    ax.plot(df["t"], df["average"], label="Moving Average")
    ax.set_title("Price/Moving Average Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price/Moving Average")
    ax.legend()
    ax.grid()

    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Compute and display chosen parameters and computed statistics
    """)
    return


@app.cell
def _(df):
    mx = df["prices"].max()
    mn = df["prices"].min()
    avg = df["prices"].mean()
    stddev = df["prices"].std()
    return avg, mn, mx, stddev


@app.cell
def _(avg, mn, mo, mx, parameters, stddev):
    mo.md(f"""
    # Summary

    ## Selected Parameters
    Number of observations: {parameters["N"].value}<br>
    Volatility: {parameters["sigma"].value}<br>
    Seed: {parameters["seed"].value}<br>
    Moving-average window size: {parameters["window size"].value}

    ##Computed Statistics
    Minimum price: {mn}<br>
    Maximum price: {mx}<br>
    Average price: {avg}<br>
    Standard deviation of the price changes: {stddev}<br>
    """)
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import polars as pl
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, pl, plt


if __name__ == "__main__":
    app.run()
