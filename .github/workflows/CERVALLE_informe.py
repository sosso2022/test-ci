# # Flujos de producto CERVALLE
# Python packages
import time
import argparse
import json
import pandas as pd
from datetime import datetime
from funciones_ioa import ioa as ioa

# Graph Modules
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot


def date_to_spanish_month(date):
    """
    Convert a date to spanish month.
    """
    months = {
        1: "En",
        2: "Feb",
        3: "Mar",
        4: "Abr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dic",
    }
    # dateList = date.tolist()

    return "{}-{}-{}".format(date.day, months[date.month], date.year)


def daily_graph(df_water2: pd.DataFrame(), listaGalpones) -> dict:
    fig = go.Figure()

    inhiProm = (
        df_water2.groupby(["date"])
        .agg({"kilos": ["sum", "max", "min", "std", "median", "mean"]})
        .reset_index()
    )
    inhiProm.columns = ["_".join(x) for x in inhiProm.columns.ravel()]
    inhiProm.rename(
        columns={"Sensor_": "Sensor", "date_": "date"}, inplace=True
    )
    inhiProm = inhiProm.sort_values(["date"])

    df_water2["date"] = df_water2.apply(
        lambda x: date_to_spanish_month(x["date"]), axis=1
    )

    for i in listaGalpones:
        fig.add_trace(
            go.Scatter(
                x=df_water2[df_water2["Sensor"] == i].date,
                y=df_water2[df_water2["Sensor"] == i]["kilos"],
                mode="lines",
                visible=True,
                legendgroup="H" + i,
                hovertemplate="Kilos: %{y:.2f}" + "<br>Fecha: %{x}",
                name="" + i,
            )
        )
    fig.update_xaxes(tickformat="%d-%b-%Y")

    # fig.update_yaxes(showspikes=True)

    fig.update_layout(
        width=800,
        title="Consumo diario de Inhisalm",
        xaxis_title="Fecha",
        yaxis_title="Kilos de Inhisalm",
        legend_title="Lineas",
    )
    fig.show()

    t = "Entrega los valores de consumo de Inhisalm cada dia en kilogramos (densidad: 1.3 )"
    data = {
        "values": fig,
        "title": "Consumo de Inhisalm",
        "subtitle": "Diario",
        "text": t,
        "type": "Graph",
    }

    return data


def get_sensor_data(
    df_sensors: pd.DataFrame, ini_date: datetime, end_date: datetime
) -> pd.DataFrame:
    df = pd.DataFrame()

    for _, row in df_sensors.iterrows():
        temp = ioa.get_sensor_values(
            row["raw_id"], ini_date, end_date, period="1H"
        )  # Period '' (no agg) , '1H' , '1D'
        temp.rename(
            columns={"value": row["sensor"].split("|")[-1]}, inplace=True
        )
        df = pd.concat([df, temp])

    return df


def process_data(
    df: pd.DataFrame,
    min_standard: float = 5.5,
    max_standard: float = 6.0,
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
    df["pH"] = pd.to_numeric(df["pH"])

    df["date"] = df["time"].dt.date
    df["date"].dt.strftime("%b")
    # TODO: Check if these are fixed Values

    df["hour"] = df["time"].dt.hour
    df["Sensor"] = "pH"
    df["House"] = "G05"
    df["sensor"] = "pH"
    df["sensors"] = "G05 - pH"

    df["confort_pH"] = df["pH"].apply(
        lambda x: min_standard <= x and x <= max_standard
    )
    df.sort_values(["time"], inplace=True)

    df["month"] = pd.DatetimeIndex(df["date"]).month
    df["month_year"] = df["time"].dt.to_period("B")
    df["month"].replace(months, inplace=True)

    return df


def weekly_graph(weekwater: pd.DataFrame(), listaGalpones) -> dict:
    fig = go.Figure()

    weekwater = weekwater.sort_values(["semana"])

    for i in listaGalpones:
        fig.add_trace(
            go.Scatter(
                x=weekwater[weekwater["Sensor"] == i].semana,
                y=weekwater[weekwater["Sensor"] == i]["kilos_sum"],
                mode="lines",
                visible=True,
                legendgroup="H" + i,
                hovertemplate="Kilos: %{y:.2f}" + "<br>Semana: %{x}",
                name="" + i,
            )
        )

    fig.update_layout(
        width=800,
        title="Consumo semanal de Inhisalm",
        xaxis_title="Semana",
        yaxis_title="Kilos de Inhisalm",
        legend_title="Lineas",
    )

    t = "Entrega los valores de consumo de Inhisalm cada semana en kilogramos"
    data = {
        "values": fig,
        "title": None,
        "subtitle": "Semanal",
        "text": t,
        "type": "Graph",
    }

    return data


def monthly_graph(monthWater: pd.DataFrame()) -> dict:

    fig = px.bar(
        monthWater,
        x="Mes del ano",
        y="Kilos",
        color="Sensor",
        hover_data={
            "Mes del ano": True,
            "Kilos": True,
            "Total general": False,
        },
    )  # Color attribute
    fig.update_layout(
        width=800,
        title="Consumo mensual de Inhisalm",
        xaxis_title="Mes del ano",
        yaxis_title="Kilos de Inhisalm",
        legend_title="Lineas",
        xaxis=dict(dtick=1),
    )
    fig.update_yaxes(showspikes=True)

    t = "La grafica muestra el consumo total de Inhisalm en kilogramos mes a mes."
    data = {
        "values": fig,
        "title": None,
        "subtitle": "Mensual",
        "text": t,
        "type": "Graph",
    }
    return data



def to_html(list_data: list, company: str, farm: str) -> str:

    comFarm = company + " - " + farm

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
        "<h2 class=title><strong> %s </strong></h2>\n"
        % "Reporte de consumo de productos"
    )
    html_result += "<h3 class=title><strong> %s </strong></h3>\n" % comFarm
    html_result += (
        "<h4 class=title><strong> %s </strong></h4>\n"
        % time.strftime("%d-%b-%Y")
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
    html_result += "<h6>Quieres saber mas?</h6>"
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
    

    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    pio.templates.default = "plotly_white"
    
    
    # Water Graph List
    list_data = list()

    # Water Flow

    sensors_water = ioa._get_devices_in_company_mongo(company, "water")

    sensors_water = sensors_water[sensors_water.sensorName.str.contains("ora")]
    sensors_water["noGalpon"] = sensors_water["barnName"].apply(
        lambda x: x.split("|")[-1]
    )
    sensors_water["House"] = sensors_water["barnName"].apply(
        lambda x: x.split("|")[-1]
    )
    sensors_water["sensor"] = sensors_water["sensorName"]

    df_water = pd.DataFrame()

    for _, row in sensors_water.iterrows():
        temp = ioa.get_sensor_values(
            row["raw_id"], ini_date, end_date, period="1H"
        )
        temp.rename(
            columns={"value": row["sensor"].split("|")[-1]}, inplace=True
        )
        df_water = pd.concat([df_water, temp])

    df_water_backup = df_water.copy()

    df_water = df_water_backup.copy()
    df_water["time"] = df_water.timestamp.apply(
        lambda x: datetime.fromtimestamp(x / 1000)
    )
    df_water.set_index("time", inplace=True)
    df_water = (
        pd.DataFrame (df_water.drop (columns=["timestamp"]).stack ())
        .reset_index ()
        .rename (columns={0: "water", "level_1": "Sensor"})
    )

    df_water["water"] = pd.to_numeric(df_water["water"])
    df_water["date"] = pd.to_datetime(df_water["time"])
    df_water["kilos"] = [x * 1.3 for x in df_water.water]
    df_water["date"] = df_water["time"].dt.date

    df_water["hour"] = df_water["time"].dt.hour
    df_water["House"] = "Planta de produccion"
    df_water["sensors"] = "Planta - water"
    df_water["semana"] = df_water["time"].dt.isocalendar().week
    df_water["semana"] = [0 if x == 52 else x for x in df_water.semana]
    df_water["mes"] = df_water["time"].dt.month

    df_water["monthName"] = df_water["time"].dt.month_name()
    months = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre",
    }

    df_water["monthName"] = df_water["monthName"].map(months)
    df_water2 = (
        df_water.groupby(["date", "mes", "monthName", "semana", "Sensor"])
        .sum()
        .reset_index()
    )

    df_water2["water"] = [
        None if x > 250 and y == "Inhisalm-Pluma-Total Hora" else x
        for x, y in zip(df_water2.water, df_water2.Sensor)
    ]
    df_water2["water"] = [
        None
        if x > 200 and y == "Inhisalm salida prensa carne y hueso Total Hora"
        else x
        for x, y in zip(df_water2.water, df_water2.Sensor)
    ]

    df_water2["kilos"] = [
        None if x > 250 * 1.3 and y == "Inhisalm-Pluma-Total Hora" else x
        for x, y in zip(df_water2.kilos, df_water2.Sensor)
    ]
    df_water2["kilos"] = [
        None
        if x > 200 * 1.3
        and y == "Inhisalm salida prensa carne y hueso Total Hora"
        else x
        for x, y in zip(df_water2.kilos, df_water2.Sensor)
    ]

    listaGalpones = df_water2.Sensor.unique()
    listaGalpones.sort()

    # ------------- General Average - Daily Consumption -------------

    df_water2 = df_water2.sort_values(["date"])

    list_data.append(daily_graph(df_water2, listaGalpones))

    # ----------------------- Weekly Consumption -----------------------

    weekwater = (
        df_water2.groupby(["Sensor", "monthName", "mes", "semana"])
        .agg({"kilos": ["sum"]})
        .reset_index()
    )

    weekwater.columns = ["_".join(x) for x in weekwater.columns.ravel()]
    weekwater.rename(
        columns={
            "monthName_": "Mes del ano",
            "mes_": "Mes",
            "Sensor_": "Sensor",
            "semana_": "semana",
        },
        inplace=True,
    )
    weekwater = weekwater.sort_values(["semana"])

    inhiPromSem = (
        weekwater.groupby(["semana"])
        .agg({"kilos_sum": ["sum", "max", "min", "std", "median", "mean"]})
        .reset_index()
    )
    inhiPromSem.columns = ["_".join(x) for x in inhiPromSem.columns.ravel()]
    inhiPromSem.rename(
        columns={
            "Sensor_": "Sensor",
            "semana_": "semana",
            "kilos_sum_sum": "kilos_sum",
            "kilos_sum_max": "kilos_ma",
            "kilos_sum_min": "kilos_min",
            "kilos_sum_std": "kilos_std",
            "kilos_sum_median": "kilos_median",
            "kilos_sum_mean": "kilos_mean",
        },
        inplace=True,
    )
    inhiPromSem = inhiPromSem.sort_values(["semana"])

    list_data.append(weekly_graph(weekwater, listaGalpones))

    # ----------------------- Monthly Consumption -----------------------

    monthWater = (
        weekwater.groupby(["Sensor", "Mes", "Mes del ano"])
        .agg({"kilos_sum": ["sum", "max", "min", "mean", "median"]})
        .reset_index()
    )

    monthWater.columns = ["_".join(x) for x in monthWater.columns.ravel()]

    monthWater = (
        weekwater.groupby(["Sensor", "Mes", "Mes del ano"])
        .agg({"kilos_sum": ["sum"]})
        .reset_index()
    )

    monthWater.columns = ["_".join(x) for x in monthWater.columns.ravel()]

    monthWater.rename(
        columns={
            "kilos_sum_": "Kilos",
            "Mes_": "Mes",
            "Mes del ano_": "Mes del ano",
            "Sensor_": "Sensor",
            "kilos_sum_sum": "Kilos",
        },
        inplace=True,
    )

    monthWater = monthWater.sort_values(["Mes"])

    inhiProm = (
        monthWater.groupby(
            [
                "Mes",
            ]
        )
        .agg({"Kilos": ["sum"]})
        .reset_index()
    )

    inhiProm.columns = ["_".join(x) for x in inhiProm.columns.ravel()]

    inhiProm.rename(
        columns={"Mes_": "Mes", "Kilos_sum": "Total general"}, inplace=True
    )

    inhiProm = inhiProm.sort_values(["Mes"])

    monthWater = pd.merge(monthWater, inhiProm, on="Mes", how="left")

    list_data.append(monthly_graph(monthWater))

    html_doc = to_html(list_data, company=company, farm=farm)

    current_date = time.strftime("%d-%b-%y")

    with open(
        report_name
        + " "
        + current_date
        + ".html",
        "w",
    ) as f:
        f.write(html_doc)


if __name__ == "__main__":
    main()