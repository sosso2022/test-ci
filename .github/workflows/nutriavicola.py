import time
import argparse
import json
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as tls
from funciones_ioa import ioa as ioa

from plotly.offline import plot
from plotly.subplots import make_subplots


"""
    When generating functions consider good programming practices, 
    use python type hints to describe the type of variable 
    you expect to revisit and return within the function.  
    Use the following functions as a guide for constructing your own. 
"""


def to_html(list_data: list, company: str, farm: str) -> str:

    html_result = """
<!DOCTYPE html>
<html>
    <head>
        
        <link rel="shortcut icon" href="http://www.iconj.com/ico/p/1/p14r1u145y.ico" type="image/x-icon" />
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <meta charset="UTF-8">
        <style type="text/css">
            h3 {text-align: left;font-family: Helvetica Neue;}
            h4 {text-align: left;font-family: Helvetica Neue;}
            h5 {text-align: left;font-family: Helvetica Neue; color: gray; }
            h6 {text-align: center;font-family: Helvetica Neue; color: gray; }
            table { margin-left: auto;margin-right: auto;width:'20%'}
            table, th, td {border: 1px solid black;border-collapse: collapse;}
            th, td {padding: 5px;text-align: center;font-family: Helvetica Neue;font-size: 90%;}
            table tbody tr:hover {background-color: #dddddd;}
            .wide {width: 90%; }
            .text{margin-left: 5%;margin-right: 5%;}
            .container{padding-bottom:3%;}
            .title{text-align: center;font-family: Helvetica Neue;}
            
        </style>
    </head>
    <body style="margin-left:12%;margin-right:12%;margin-top:3%;margin-bottom:3%;padding-left:3%;padding-right:3%;padding-top:3%;
    box-shadow: 0 5px 9px 0 rgba(0, 0, 0, 0.5), 0 6px 20px 0 rgba(0, 0, 0, 0.19);border-radius:10px">
    """

    html_result += '<img src="data:image/png;base64,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" alt="asimetrix-full" alt="Asimetrix">'
    html_result += '<div class="container">'
    html_result += (
        "<h2 class=title><strong> %s </strong></h2>\n" % "H2Okuo Reporting"
    )
    html_result += (
        f"<h3 class=title><strong> {company} - {farm} </strong></h3>\n"
    )
    html_result += (
        "<h4 class=title><strong> %s </strong></h4>\n"
        % time.strftime("%d-%m-%Y")
    )
    html_result += '<div class="container">'
    html_result += "</div>"

    for i in list_data:

        if i["title"] != None:
            html_result += "<h3><strong> %s </strong></h3>\n" % i["title"]
        if i["subtitle"] != None:
            html_result += "<h4><strong> %s </strong></h4>\n" % i["subtitle"]
        if i["text"] != None:
            html_result += '<h5 class="text"> %s </h5>\n' % i["text"]

        if i["type"] == "Table":
            html_result += i["values"].to_html(
                classes="wide", escape=False, index=False
            )
        elif i["type"] == "Graph":
            aPlot = plot(
                i["values"],
                config={"displayModeBar": False},
                show_link=False,
                include_plotlyjs=False,
                output_type="div",
            )
            html_result += aPlot
        else:
            html_result += (
                "<h3><strong> %s </strong></h3>\n" % "Ningun tipo coincide"
            )

        html_result += '<div class="container">'
        html_result += "</div>"

    html_result += '<div style="text-align: center">'
    html_result += "<h6>??Quieres saber mas?</h6>"
    html_result += (
        '<a href="https://app.asimetrix.co/auth/login" rel="noopener" style="text-decoration:underline;color:#0068a5" target="_blank"><h6>%s</h6></a>\n'
        % '<strong> <font color="#0068a5">www.asimetrix.co </font></strong>'
    )
    html_result += '<div class="container">'
    html_result += """
    </body>
</html>
"""
    return html_result


def get_sensors(company: str, farm: str) -> pd.DataFrame:

    df_sensors = ioa._get_devices_in_company_mongo(company, "pH")
    df_sensors["noGalpon"] = df_sensors["barnName"].apply(
        lambda x: x.split("|")[-1]
    )
    df_sensors = df_sensors[df_sensors.farmName == farm]
    df_sensors["House"] = df_sensors["barnName"].apply(
        lambda x: x.split("|")[-1]
    )
    df_sensors["sensor"] = df_sensors["kind"]
    return df_sensors


def get_sensor_data(
    df_sensors: pd.DataFrame, ini_date: datetime, end_date: datetime
) -> pd.DataFrame:

    df = pd.DataFrame()

    for _, row in df_sensors.iterrows():
        temp = ioa.get_sensor_values(
            row["raw_id"], ini_date, end_date, period="1H"
        )
        temp.rename(
            columns={"value": row["sensor"].split("|")[-1]}, inplace=True
        )
        df = pd.concat([df, temp])

    return df


def process_data(
    df: pd.DataFrame,
    min_standard: float = 5.5,
    max_standard: float = 6.5,
    months: dict = {},
) -> pd.DataFrame:

    if not months:
        months = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

    df["time"] = df.timestamp.apply(lambda x: datetime.fromtimestamp(x / 1000))
    df.set_index("time", inplace=True)
    df = (
        pd.DataFrame(df.drop(columns=["timestamp"]).stack())
        .reset_index()
        .rename(columns={0: "pH", "level_1": "Sensor"})
    )

    df = df[df.time <= np.datetime64("2022-02-11 12:00:00")]

    df["pH"] = pd.to_numeric(df["pH"])

    df["date"] = df["time"].dt.date

    df["hour"] = df["time"].dt.hour
    df["Sensor"] = "pH"
    df["House"] = "Planta"
    df["sensor"] = "pH"
    df["sensors"] = "Planta - pH"
    df["min_standard"] = min_standard
    df["max_standard"] = max_standard
    df["confort_pH"] = [
        True if x <= y and y <= z else False
        for x, y, z in zip(df["min_standard"], df.pH, df["max_standard"])
    ]

    df["programa"] = [
        "Antes"
        if x <= datetime.strptime("2021-07-08", "%Y-%m-%d")
        else "Despu??s"
        for x in df["time"]
    ]

    df.sort_values(["time"], inplace=True)

    df["month"] = pd.DatetimeIndex(df["date"]).month
    df["month_year"] = df["time"].dt.to_period("M")
    df["month"].replace(months, inplace=True)
    df = df[df.hour < 20]
    df = df[df.hour >= 5]

    return df


def plot_daily_ph(
    df: pd.DataFrame,
    sensor_list: List,
    min_alert: float = 4.5,
    max_alert: float = 7,
) -> go.Figure:

    fig = tls.make_subplots(
        rows=1, cols=1, shared_xaxes=True, print_grid=False
    )

    df = df.sort_values(["time"])
    df["min_alert"] = min_alert
    df["max_alert"] = max_alert
    for i in sensor_list:
        fig.add_trace(
            go.Scatter(
                x=df[df["sensors"] == i].time,
                y=df[df["sensors"] == i]["pH"],
                mode="lines",
                connectgaps=False,
                legendgroup="H" + i,
                hovertemplate="pH: %{y:.2f}" + "<br>Fecha y hora: %{x}",
                name="" + i,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["min_alert"],
            mode="lines",
            name="pH alerta",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            showlegend=False,
            legendgroup="alerta",
            hovertemplate="pH alerta min: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["max_alert"],
            mode="lines",
            name="pH alerta",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            fill="tonexty",
            legendgroup="alerta",
            fillcolor="rgba(255,69,0, 0.13)",
            hovertemplate="pH alerta max: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["min_standard"],
            mode="lines",
            name="pH ??ptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            showlegend=False,
            legendgroup="optimo",
            hovertemplate="pH m??nimo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["max_standard"],
            mode="lines",
            name="pH ??ptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            fill="tonexty",
            legendgroup="optimo",
            fillcolor="rgba(0, 177, 106, 0.13)",
            hovertemplate="pH m??ximo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )

    fig.update_layout(
        width=850,
        title="pH Diario entre las 5 a.m. y las 8 p.m.",
        xaxis_title="Fecha",
        yaxis_title="pH",
        legend_title="Sensores",
    )

    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig


def plot_std_ph(df: pd.DataFrame, sensor_list: List) -> go.Figure:
    daypH = df.groupby(["sensors"]).agg({"pH": ["mean", "std"]}).reset_index()
    daypH.columns = ["_".join(x) for x in daypH.columns.ravel()]
    daypH.rename(
        columns={"sensors_": "sensors", "time_": "time"}, inplace=True
    )

    data = [
        go.Scatter(
            x=df[df["sensors"] == i].sort_values("time").time,
            y=df[df["sensors"] == i].sort_values("time").pH.diff(),
            mode="lines",
            name=i,
            hovertemplate="Variaci??n de pH: %{y:.2f}"
            + "<br>Fecha y hora: %{x}",
            legendgroup=i,
        )
        for i in sensor_list
    ]
    layout = go.Layout(
        title="Variaci??n pH Planta",
        xaxis=dict(title="Fecha"),
        width=850,
        yaxis=dict(title="Delta pH"),
        legend={"traceorder": "normal"},
    )
    fig = go.Figure(data=data, layout=layout)

    fig.add_trace(
        go.Scatter(
            x=df[df["sensors"] == sensor_list[0]].sort_values("time").time,
            y=[-2 * daypH.pH_std.mean()]
            * df[df.sensors == sensor_list[0]].shape[0],
            mode="lines",
            name="2 desviaciones estandar",
            legendgroup="optimo",
            showlegend=False,
            opacity=0.5,
            line=dict(dash="dash"),
            line_color="rgba(0,150,136 ,0.4)",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[df["sensors"] == sensor_list[0]].sort_values("time").time,
            y=[2 * daypH.pH_std.mean()]
            * df[df.sensors == sensor_list[0]].shape[0],
            mode="lines",
            name="2 desviaciones estandar",
            opacity=0.4,
            legendgroup="optimo",
            line=dict(dash="dash"),
            line_color="rgba(0,150,136 ,0.4)",
            fill="tonexty",
            fillcolor="rgba(0, 177, 106, 0.15)",
        )
    )
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig


def plot_hourly_ph(df: pd.DataFrame) -> go.Figure:
    df_ph = (
        df.groupby(["hour", "sensors"])
        .agg({"pH": ["mean", "std"]})
        .reset_index()
    )
    df_ph = df_ph.set_axis(
        ["hour", "sensors", "mean", "std"], axis=1, inplace=False
    )

    df["min_standard"] = 5.5
    df["max_standard"] = 6.5
    df["min_alert"] = 5
    df["max_alert"] = 7

    fig = tls.make_subplots(
        rows=1, cols=1, shared_xaxes=True, print_grid=False
    )
    df_ph = df_ph.sort_values(["hour"])
    for i in df.sensors.unique():
        fig.add_trace(
            go.Scatter(
                x=df_ph[df_ph["sensors"] == i].hour,
                y=df_ph[df_ph["sensors"] == i]["mean"],
                mode="lines",
                legendgroup="H" + i,
                name="" + i,
                hovertemplate="temp promedio: %{y:.2f}" + "<br>Fecha: %{x}",
            )
        )

    fig.update_layout(legend_traceorder="reversed")
    fig.update_layout(
        width=850,
        title="ph por horas",
        xaxis_title="horas",
        yaxis_title="pH",
        legend_title="sensores",
    )
    fig.add_vline(
        x="2021-8-13", line_width=3, line_dash="dash", line_color="green"
    )
    fig.add_vline(
        x="2021-9-13", line_width=3, line_dash="dash", line_color="yellow"
    )
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    fig.add_trace(
        go.Scatter(
            x=df_ph.hour,
            y=df_ph["mean"] + df_ph["std"],
            mode="lines",
            line=dict(width=1),
            showlegend=False,
            line_color="rgba(0, 177, 106, 0.5)",
            legendgroup="std",
            hovertemplate="pH: %{y:.2f}" + "<br>Fecha y hora: %{x}",
            name="Desviaci??n estandar",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_ph.hour,
            y=df_ph["mean"] - df_ph["std"],
            mode="lines",
            line=dict(width=1),
            fill="tonexty",
            legendgroup="std",
            fillcolor="rgba(0, 177, 106, 0.18)",
            line_color="rgba(0, 177, 106, 0.5)",
            hovertemplate="pH: %{y:.2f}" + "<br>Fecha y hora: %{x}",
            name="desvest max",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["min_alert"],
            mode="lines",
            name="pH alerta",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            showlegend=False,
            legendgroup="alerta",
            hovertemplate="pH alerta min: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["max_alert"],
            mode="lines",
            name="pH alerta",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            fill="tonexty",
            legendgroup="alerta",
            fillcolor="rgba(255,69,0, 0.13)",
            hovertemplate="pH alerta max: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["min_standard"],
            mode="lines",
            name="pH ??ptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            showlegend=False,
            legendgroup="optimo",
            hovertemplate="pH m??nimo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["max_standard"],
            mode="lines",
            name="pH ??ptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            fill="tonexty",
            legendgroup="optimo",
            fillcolor="rgba(0, 177, 106, 0.13)",
            hovertemplate="pH m??ximo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )

    return fig


def plot_average_ph(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month

    df_ph = df[df.time <= np.datetime64("2022-02-11 12:00:00")]
    df_ph = (
        df_ph.groupby(["date", "year", "sensors"])
        .agg({"pH": ["mean", "std", "max", "mean"]})
        .reset_index()
    )
    df_ph = df_ph.set_axis(
        ["date", "year", "sensors", "mean", "std", "max", "mean"],
        axis=1,
        inplace=False,
    )
    dias = df_ph.year.count()
    df_ph = (
        df.groupby(["year", "sensors"])
        .agg({"pH": ["mean", "std", "max", "mean"]})
        .reset_index()
    )
    df_ph = df_ph.set_axis(
        ["year", "sensors", "mean", "std", "max", "mean"],
        axis=1,
        inplace=False,
    )

    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=df_ph.iloc[0][2],
            number={"prefix": "pH "},
            delta={"position": "top", "reference": 6},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )

    fig.update_layout(
        paper_bgcolor="lightgray",
        title="Valor de pH promedio de " + str(dias) + " d??as.",
        width=400,
        height=400,
    )

    return fig


def plot_ideal_ph(df: pd.DataFrame, sensor_list: List) -> go.Figure:
    fig = go.Figure()
    df_ph = df.copy()

    df_ph["confortpH"] = [
        True if x <= y and y <= z else False
        for x, y, z in zip(
            df_ph["min_standard"], df_ph.pH, df_ph["max_standard"]
        )
    ]
    df_pHAntes = df_ph[df_ph.programa == "Antes"]
    idealpHAntes = {}
    for i in sensor_list:
        idealpHAntes["pH_ideal_cliente" + str(i) + "-antes"] = (
            np.sum(df_pHAntes[df_pHAntes.sensors == i]["confortpH"])
            * 100
            / df_pHAntes[df_pHAntes.sensors == i].shape[0]
        )

    df_pHDespues = df_ph[df_ph.programa == "Despu??s"]
    idealpHDespues = {}
    for i in sensor_list:
        idealpHDespues["pH_ideal_cliente" + str(i) + "-despues"] = (
            np.sum(df_pHDespues[df_pHDespues.sensors == i]["confortpH"])
            * 100
            / df_pHDespues[df_pHDespues.sensors == i].shape[0]
        )
    ##############
    # Esta secci??n se repite en la siguiente funci??n
    comfortph = []
    for i in df_ph.sensors.unique():
        for w in df_ph.date.unique():
            df_ph4WB = df_ph[(df_ph.date == w) & (df_ph.sensors == i)]
            idealT4B = {}

            d = {
                "sensors": i,
                "confPorph": np.sum(
                    df_ph4WB[df_ph4WB.sensors == i]["confortpH"]
                )
                * 100
                / df_ph4WB[df_ph4WB.sensors == i].shape[0],
                "fecha": str(w),
                "programa": [
                    np.nan
                    if len(df_ph4WB.sensors.unique()) == 0
                    else df_ph4WB.programa.unique()[0]
                ][0],
            }

            comfortph.append(d)

    comfortph = pd.DataFrame(comfortph)
    comfortph = comfortph.dropna()
    # fin secci??n repetida
    #######
    fig = make_subplots(
        rows=1,
        cols=1,
        specs=[[{"type": "domain"}]],
        horizontal_spacing=0.1,
        vertical_spacing=0.1,
    )

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            number={"suffix": "%"},
            value=idealpHDespues["pH_ideal_clientePlanta - pH-despues"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": "Porcentaje dentro del pH ??ptimo",
                "font": {"size": 16},
            },
            gauge={
                "axis": {"range": [None, 100]},
                "bar": {"color": "darkblue"},
            },
        ),
        row=1,
        col=1,
    )

    fig.update_layout(
        height=500,
        width=600,
        title_text="Porcentaje del tiempo en el rango de pH ideal (5.5 - 6.5)",
        showlegend=True,
    )

    return fig


def plot_ph_in_time_range(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    df_ph = df.copy()

    #########
    # Esta secci??n se repite en la funci??n anterior, hay que extraerla y hacerla funcional
    comfortph = []
    for i in df_ph.sensors.unique():
        for w in df_ph.date.unique():
            df_ph4WB = df_ph[(df_ph.date == w) & (df_ph.sensors == i)]
            idealT4B = {}

            d = {
                "sensors": i,
                "confPorph": np.sum(
                    df_ph4WB[df_ph4WB.sensors == i]["confortpH"]
                )
                * 100
                / df_ph4WB[df_ph4WB.sensors == i].shape[0],
                "fecha": str(w),
                "programa": [
                    np.nan
                    if len(df_ph4WB.sensors.unique()) == 0
                    else df_ph4WB.programa.unique()[0]
                ][0],
            }

            comfortph.append(d)

    comfortph = pd.DataFrame(comfortph)
    comfortph = comfortph.dropna()
    # fin de la secci??n repetida
    ##########
    comfortph = comfortph.sort_values(["fecha"])
    fig = px.line(
        comfortph,
        x="fecha",
        y="confPorph",
        title="Tiempo entre 5.5 y 6.5 de pH (%) ",
        color="sensors",
        height=400,
        width=800,
        # Depende de los lotes
        # category_orders={"idLote": listaGalpones},
        labels={
            "week": "Fecha",
            "confPorph": "Tiempo (%)",
            "sensors": "Galpones",
        },
    )
    fig.update_yaxes(range=[0, 100])
    fig.add_shape(
        type="line",
        line_color="green",
        line_width=3,
        opacity=0.5,
        line_dash="dot",
        x0=0,
        x1=1,
        xref="paper",
        y0=80,
        y1=80,
        yref="y",
        name="Objetivo",
    )
    fig.update_layout(legend=dict(orientation="v", y=1.05))
    fig.show(
        config={
            "modeBarButtonsToAdd": [
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
            ]
        }
    )

    return fig


def plot_monthly_ph(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    df_ph = df.copy()

    df_ph["month"] = pd.DatetimeIndex(df_ph["date"]).month
    df_ph["month_year"] = df_ph["time"].dt.to_period("M")
    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }
    df_ph["month"].replace(meses, inplace=True)

    fig.add_trace(
        go.Box(
            x=df_ph.month,
            y=df_ph["pH"],
            boxmean=True,
            showlegend=False,
            boxpoints="suspectedoutliers",
            marker_size=0.00001,
            jitter=0.3,
        )
    )

    fig.update_layout(
        width=800,
        title="pH cada mes",
        xaxis_title="Meses",
        yaxis_title="pH",
        legend_title="",
    )

    fig.add_shape(
        type="rect",
        x0="Julio",
        y0=4.5,
        x1="Diciembre",
        y1=5.5,
        line=dict(
            dash="dot",
            color="rgba(0, 177, 106, 0.50)",
            width=2,
        ),
    )

    fig.update_xaxes(
        categoryorder="array",
        categoryarray=[
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ],
    )

    return fig

def parser_config()-> dict:

    config_parser = argparse.ArgumentParser(
        prog="Report Generator",
        description="Generate the report pass the parameter values from lambda script",
    )

    config_parser.add_argument(
        "-pf",
        "--parameters_file",
        help="File with the report parameters",
        required=True,
    )

    args = config_parser.parse_args()

    return args

def main():

    args = parser_config()

    json_file_name = ""
    if args.parameters_file is not None:
        if ".json" in args.parameters_file:
            json_file_name = args.parameters_file

    json_dict = json.load(open(json_file_name))


    company = json_dict["company"]
    farm = json_dict["farm"]
    report_name =  json_dict["report_name"][0]
    
    ini_date = json_dict["start_date"]
    ini_date = datetime.strptime(ini_date, "%Y-%m-%d")
    
    end_date = json_dict["end_date"]
    
    min_standard = json_dict["params"]["min_standard"]
    max_standard = json_dict["params"]["max_standard"]
    min_alert = json_dict["params"]["min_alert"]
    max_alert = json_dict["params"]["max_alert"]

    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    pio.templates.default = "plotly_white"
    

    farm = "Huevos Oro"
    company = "NUTRIAVICOLA"

    current_date = time.strftime("%d-%m-%y")

    df_sensors = get_sensors(company, farm)

    df = get_sensor_data(df_sensors, ini_date, end_date)

    df = process_data(df, max_standard=max_standard, min_standard=min_standard)

    df_mean = df.groupby(["time", "date", "sensors"]).mean().reset_index()
    sensor_list = df_mean.sensors.unique()

    list_data = list()

    ##
    # Plotly graph daily pH
    ##

    fig = plot_daily_ph(
        df,
        sensor_list,
        min_alert=min_alert,
        max_alert=max_alert,
    )

    text = "Muestra los valores de pH entre las 5 a.m. y las 8 p.m. as?? como el rango optimo."

    data = {
        "values": fig,
        "title": "Niveles de pH",
        "subtitle": None,
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    ##
    # Plotly graph standard deviation pH
    ##

    fig = plot_std_ph(df, sensor_list)

    text = ""

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Variaci??n pH Planta",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    ##
    # Plotly graph hourly pH
    ##

    fig = plot_hourly_ph(df)

    text = ""

    data = {
        "values": fig,
        "title": None,
        "subtitle": "pH por horas",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    ##
    # Plotly graph average ph
    ##

    fig = plot_average_ph(df)

    text = "Este es el valor promedio de pH. El valor verde indica cuantos puntos de pH de diferencia hay contra el objetivo (pH 6)."

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Promedio de pH general",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    ##
    # Plotly graph ideal ph
    ##

    fig = plot_ideal_ph(df, sensor_list)

    text = ""

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Tiempo (%) del pH dentro de los niveles optimos",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    ##
    # Plotly graph ph in time range (DEPENDE DE LOTES)
    ##

    # fig = plot_ph_in_time_range(df, sensor_list)

    text = "Porcentaje de cumplimiento del pH cada d??a"

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Tiempo (%) del pH dentro de los niveles optimos",
        "text": text,
        "type": "Graph",
    }

    ##
    # plotly graph montly ph
    ##

    fig = plot_monthly_ph(df)

    text = ""

    data = {
        "values": fig,
        "title": None,
        "subtitle": None,
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    html_doc = to_html(list_data, company=company, farm=farm)

    with open(
        report_name+ " " + current_date + ".html", "w"
    ) as f:
        f.write(html_doc)


# Define and use the main python function.
if __name__ == "__main__":
    main()