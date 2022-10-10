# Python packages
import time
import argparse
import json

# import boto3
import numpy as np
import pandas as pd
from typing import List
from datetime import datetime
from funciones_ioa import ioa as ioa

# Graphics packages
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot


def to_html(list_data: List, com_farm: str) -> str:

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

    html_result += '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXgAAACGCAMAAADgrGFJAAAAsVBMVEX///80NDQigHQmJiYiIiIrKyva2towMDC7u7spKSng4OBzc3Pz8/MgICAuLi6enp4bGxvp6enx8fH5+fmUlJQAd2p8fHxmZmaxsbHQ0NBDQ0NKSkoSEhLl5eWlpaVfX1+EhIQ7OztSUlKOjo7Hx8fR0dGamppvb29XV1diYmK/v7+5089TmI7i7uzr8/Kjo6ODsKo7joPH3Nmmx8JEkIbX5+SVvrioyMNspp4LCwt2q6NMT6YaAAAOJ0lEQVR4nO1daXuizBINNoioEAxxN4hrTCbLJLPlvv//h13Mql1LFwaGeQxn5qPprj4U1bV1c3JSoUKFChUqVKhQoUKFChXyRhRFZYvw9RA9fr95qD3cfH8sW5IvhehHrdutbdHt/vxWtjRfB79+vrD+gu7NbdkCfRE81vbRrf0qW6QvgdsaRKXzfwEPCPEPZQv1BfC7ixDf/V22WMcPjPeU+cqlLxjfCOL/lC3YseMJ5b1WuylbsGMHwXutVrZgxw7c0tQqj7Jg3FHEd6sgqljkqPGNS8cbtwbtAqQ8QpA2Pqs/ee3bgWW5ju3HhQh6bLgheM8auw4m1hvCpAhBjw1/CD8+Y+ja/OA9ZX5djKxHBWJ37WY08f3A2mX+rBhhjwrfUeafsg3S2VV4y1KVypsRoQp/l22QWO0R746KkfW48AhVPnOmZt/SWJZd+ZQCgDxZ90fWISwN9qoIQY8Oj7V96jOXu9ueTvyyCDmPD3dP79R3u0/ZY9YOIP66ACmPEre/bx663e7DzfdDcjRNpRPfyF3C48Xd7a/bjM7MG+oV8eWgIr4kVMSXhIr4klARXxIq4ktCRXxJqIgvCRXxJaEiviRUxJeEiviSUBFfEiriD0TUvlg2Gvf393GjsTprZ+6Nz0R81GzE8VJYG2wPB6eDa0HTwuq8NZ324o5sWF2kdnOVEtBoDFed7Ks/EGfDdWvshL5tqxS2HYazTTJoZiqaZiF+MArTmXxrIeCofW49/9hrNQ0CXIXKcQNH2YuMvEXNQTIdeeGWANv2w4k7vzxfHvb8MqBz3bJCFbj7tLmOHY4XK/kS5MRHPf91MjWrG6WbvY3rKNZ2LR3nbWa/n0FlouFi7NvO/vrdwPOd6drwqD+FemL5joXD9exxLO1LEhMf9e2PGdwLftRottO7EDLFxKa/w5zqC4U+6azHtqfp3LtwSm2K2qfqV55eKtUnt85lWi8lPpru/tC55Eft7YrnzmgtmO+3sckK7Z2eqwjWX2e0R0W037Z7fsBN+wIViB67kPhovP+kJ6wpvdh/Ge176oercJ+wuUTktUHrXqgf594tcR1SNkZDOBfYGxnx7bEj+NU71tLutHONwolZ4tVMl5igPrzM1cmJktA86SsCx/zURcRHG/1ZK/ZV1rvTyPdjrlkM3yjw6YQ1MrtwAqMPIMfZRva8XxGemgaUEB/1wbutBpyQI40csldHH9bmht1KcilXu1TpJ4bh5LiYC83MG8KFYUQB8dElfNgTrtGvM9N+TT2mtq693jkrbJRN7dI3yKh4MnRmGXlPp074IQXEt2wwKr8LNqWGCRDvsNK25+ZdVV++SfFEiMYCbwZMzSuRmfge5N2asLYYEk8oHiS+xY17lZn3dPmkR5UB5MRpxO3oMezH1KyhMxKP8a56rJwFEd+j7Ay//M/3gq59dFZ7ojaXSXI1moT4g7G5zd1E/AKZ1BnzjloxxA/Q5Qf2xJumy++PJj6+fN8QZRuxmiCjBva88e6rrdYWFtG5I4YnA/EY7wETiT6jEOJBd+3z79X0Y/nDhYv9xh3z0poQ6T7a84r6mjYPRshjVwk9LE/8KcK7OzMloQohfoPsb3ZfEyW2sOV/boO9R3wLJCsQ9RCuFG1sWOJjjHfLGJYUQfwAOvCBC813u4Uo/f8+Y2w6CAV4dhYRkclpccQPkH3VtcxHdQogPpqB990Zo2/eOWTelNJjsQDjuQ7xIBHm6VCcIb6B8B6Y9b0Q4uH77o6IPMQpFNsfmoUmcAY5CEnVg+4P/cxp4q8R3p2R5K0tgHho4F1yp0mAjgbiRD9ADFiwmWh4CuQMKTFJ4peIfffmohpR/sQ3gDBcdDKGZunQolSkp/H4oP0CPHOP2tkp4utINsq+kiVa8yceeHSsDteB432wYwOH4os1yA5DjYwTX0f03U6E0uZOPNQC/jRuTxfANYR8JPSCgeVu2N9DH4jaEQDxzjYd0EQicFt8y0HuxN/rQhqMdgfoKRu9MwCWxjfU9RJ97VTCFRBveevmEjpvlpJnm3InHixfGdwUvRJz6N0YHWhwDVH7UN+MqfIbJN5SoQ95z+IY5E38BUyGGyS41i1lcCUXfwfAo+bTpydYgmGCWzmEeBRZDnznTfwSLD8xLR88KlN+CQcw8aYSGbK/EEGElPgwg5HMm/i1LqO5NNvSbQ3pT7OY6gLaxmFAuE9UgcTEZ7jUI2/ir3QWzc0Ip8BZO6j8qrPgjoyBTF1/SRy8eCElnuIOQ97Eg4AoMIoAwj8ykOEQ6d6RYKsAOQYi4pISn6WekDPxoHYemJNeZ7o7QuidYSGHjAJ2Vxf9mZh4R+4X5Ew8GM7Qi7BFNNJXPxWL/wH43phnPtkA3xd1a8TEZ7CSORO/0pfPNvW8AORYBNYZAniTgplPLkEMge5IcuLdmbT1vGjiJYdWQAjlHuBPAg9FonzAn1SoJyQn3vKkZjJn4oHemb1JRO9MIScGSLwgmoHEo554BuLF15XlTPwAuPGCugbMmRxAfKzPLHGqCyCebVfYwT9JvKARGc58yLtWAPGWEmzqJ/8o8fgWx+MfsfEpJqLEQd7EA70TEN8C2ZoDiC/Hq3EcmKOUHdnImfhhaV4N9OMF2WXox6OOLEW8G/QWU9gdJOoBFRMP8r0y4v+aHw8qXwdFrniCgyA+eO7ZiSHzocCZFxMPfogSD9JOoshVJ356QPEP5mrMVYnP5Wqc16aVHmDeERREYIxPvKEy4kEdU5Kr0d8SYwUDBUi7jA/IThJ1ZLQXdPxqEJF2HsHGDvkk3tAVKPhiQsKizswowlA3EgdlJ2E+XhlThaAdiag6YsQ7H+0zsJ/HNbsHgHhKRYci4uF2NTHqHQh9+NNyFNagAmXc12EFCvf9EeKd+Y45hM1B5swBIJ5yhoB24MQDn1xQgdL/JEsFjRPQuHhAGBG5QeLd2a4+wY4e87IB8ZaD/xAoFE48WL5xd82r5grS+tbM8LIhfEp/qF36kID91dgdBIknKu1AL3FGm6CryGTklzphB3YZQCtnOvW/ALpEbC6AeL0PBAQ5qaEzKBwknog1wWtJqDLYXW1D7ArDdnTg6O7OoENZW6nOZmDpxJMCxIPtvwGbegx9WaBWR2xtF2BgwgOAasQ7h9BCwERV9Pj95qFWe3j6wX3toAlaGfnNAmzqRP0JIR6GhbD3ODA0EALi8Y5D2IBP+KqgFGJo/wUPClrHbz+7r1+a6Nb+Y+7eBw4lq/LQ/SZ3Y8EB4zrS6c86ZxF0hXzsucNiBVVogH3XCTM/bLzTu4XvnnY/rdJlPq0Czxpy1+/AgJN8QSR3GcDTKIbMAdiSUFsDtwIy7wjaZNiiDHxFtRfk7kH7mlD3OzUWNNqWTa4dWuWArLFLiG/DA4f0gFuA1CDaugl2QPp5toFTyyS9YNCnm4cH+Pks8gOJyBkoamoQLnNOkOjaFOQ0VMiFcKDlEHMrsCMnITUifEjOhti14OkRy9+v2P2HfKqP/PowkjVxpmhQgCyI0U/ZRUF9qJxcfhs7PqW0Z9/EjkKTm3YHLkrhd8c1oF3UFP4X+onEn9TU0MxZzgypvcIXjXV7ZcQj5pjLHNSRS0bc/VuLsBZ8rk8Q2We8EbJxIWf+rMl+ZusJ473WfSRmxk52uyrRjGK9j0zMciS7kww528MdDsBOobve6buw9QRpwU8tDT3kGfKgXHWuvXbDKfauJXu/uUV5r9VuqKlX2OVEatZbvb9xneu+h+kal6eQXgYH1x3M6agPpLVehLX6i8FgcNrbKPy+B64ZFTNf6fKTjzs2O40rGzl3r+/r4PuIbypPLmeBTW05anaVnMZxuhwLm9eQ1JJefwiyH+kvaWceHEh5Y9ZTtq2QYu4z+Jw5PL76/DfeqJ/EcXzfopav98LgX8FlbE3qHhP3MwXO9opbajk2uxzxhZ+gSZ1NlmG2xogJG45GxLVgLr/8UFcP3MSnxNNRVKRfQiiB4fpSMfHIOSwmhsMvl+Fhqs5hZt4IeEaU+sY890XWs1Fm5pWhIQN+ZJFiE/oLXNx+gMp7prLaBXkNE718WPsiNZ77BHEn63VoynTrJTgETsbiMAPDqShM65nAbBnvy896GZ6NSEjaePZbuO2rTJ1fvrFSFYGqIpn2BJEZm6mKs9wQmUJJ2gA682zXbmLbG+nV8N8HjbDLqgi4kkPB4HJO+qd6EMN7IetMzCtZ30sbuweJXD6aZKb8+AfT3NeO0NyokeSknpa75npW2pqxMRwvTzJYG3UlbfQaYKEKBntMvLv47kqnyd7RaUnu1w1C2UXmWjV7whXVtHYMx9BVFofSzTBsyfu8LvqSYR11Sg35iNsayZeIhyPT3M6kLz2lt+cee3yT1nrXs+HumHuV0xKZZCfjHcDLmXn5LUYpnrDsJOfT7M698akvBmyNm2/6MscOOu5HaGS6UfJk53rnwNTpsMXa56/Y384ZtjK3XlzP2eXbPVbrIoT3J/Hc9cXIQ8I117GD8TrTtXMXo1dyXHtq4jJ6v17RE9wKl6J9P/YY7l3lXB7UarRKRgp8IeV5+e7Y+IGdX4D3m0wtrfW4NbZ8X3nOM5TylTXvDTKf2o/OR9vv6thjQZtbu+/YTuDYdk/c9ly/nwa+h5LkbO4Pv5qwHl+OXdt+W76XLn+2SRqSAe9u9qyNYGMFuKgv7897SS/9v46X9QM/xrP9ZlM8FJ5wGiSXySCbmjaXyeXYCv30+XpbKDv0Z9Ok8dnv10TN+vXpIl17+u98kGX5P2rdD3Wn02PHgKjTXA7i00WK83gwbB7UU5cf7v481bopHv47btr/Rdxt8be+llahQoUKFSpUqFChQoUKFSrkhv8DTyjruv0fWwcAAAAASUVORK5CYII=" alt="asimetrix-full" alt="Asimetrix">'
    html_result += '<div class="container">'
    html_result += (
        "<h2 class=title><strong> %s </strong></h2>\n" % "H2Okuo Reporting"
    )
    html_result += "<h3 class=title><strong> %s </strong></h3>\n" % com_farm
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
    html_result += "<h6>¿Quieres saber mas?</h6>"
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


def get_sensors(company: str, farm: str, type_value: str) -> pd.DataFrame:
    """Return sensors by type of value
    Args:
        company (str): Company Name
        farm (str): Farm Name
        type_value (str): Type of sensor value exp('pH','water')
    Returns:
        pd.DataFrame: Sensors info Dataframe.
    """

    df_sensors = ioa._get_devices_in_company_mongo(company, type_value)

    if type_value == "pH":

        df_sensors["noGalpon"] = df_sensors["barnName"].apply(
            lambda x: x.split("|")[-1]
        )

        df_sensors = df_sensors[df_sensors.farmName == farm]

        df_sensors["House"] = df_sensors["barnName"].apply(
            lambda x: x.split("|")[-1]
        )

        df_sensors["sensor"] = df_sensors["kind"]

    elif type_value == "water":

        df_sensors = df_sensors[df_sensors.sensorName.str.contains("Min")]

        df_sensors["noGalpon"] = df_sensors["barnName"].apply(
            lambda x: x.split("|")[-1]
        )

        df_sensors["House"] = df_sensors["barnName"].apply(
            lambda x: x.split("|")[-1]
        )

        df_sensors["sensor"] = df_sensors["sensorName"]

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
    type_value: str,
    min_standard: float = None,
    max_standard: float = None,
    min_alert: float = None,
    max_alert: float = None,
) -> pd.DataFrame:
    """Proccess Sensors df and return Varieble Values df
    Args:
        df (pd.DataFrame): sensors Data Frame
        type_value (str): Type if variable exp(pH, water)
        min_standard (float): min_standard
        max_standard (float): max_standa
        min_alert (float): min_alert
        max_alert (float): max_alert
    Returns:
        pd.DataFrame: Variable values Data Frame
    """

    df["time"] = df.timestamp.apply(lambda x: datetime.fromtimestamp(x / 1000))

    df.set_index("time", inplace=True)

    df = (
        pd.DataFrame(df.drop(columns=["timestamp"]).stack())
        .reset_index()
        .rename(columns={0: type_value, "level_1": "Sensor"})
    )

    df[type_value] = pd.to_numeric(df[type_value])

    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour

    if type_value == "pH":

        df["Sensor"] = "pH tanque"
        df["House"] = "La Loteria"
        df["sensor"] = "pH tanque"
        df["sensors"] = "La Loteria - pH tanque"
        df["min_standard"] = min_standard
        df["max_standard"] = max_standard
        df["min_alert"] = min_alert
        df["max_alert"] = max_alert

        df["confort_pH"] = [
            True if x <= y and y <= z else False
            for x, y, z in zip(df["min_standard"], df.pH, df["max_standard"])
        ]

        df["programa"] = [
            "Antes"
            if x <= datetime.strptime("2021-07-08", "%Y-%m-%d")
            else "Después"
            for x in df["time"]
        ]

    elif type_value == "water":

        df["litros"] = [
            x * 3.785411784
            if y == "Consumo Agua - Total Minuto Galones"
            else x / 1000
            for x, y in zip(df.water, df.Sensor)
        ]

        df["m3"] = [
            x * 0.00378541
            if y == "Consumo Agua - Total Minuto Galones"
            else x / 1000000
            for x, y in zip(df.water, df.Sensor)
        ]

        df["House"] = "Planta de producción"
        df["sensors"] = [
            "Citroquim"
            if x == "Citroquim - Total Minuto mL"
            else "Consumo de agua"
            for x in df.Sensor
        ]
        df["semana"] = df["time"].dt.weekofyear
        df["semana"] = [0 if x == 52 else x for x in df.semana]
        df["mes"] = df["time"].dt.month
        df["monthName"] = df["time"].dt.month_name(locale="Spanish")
        df["year"] = df["time"].dt.year
        df["yearMonth"] = [
            str(x) + "-" + str(y) for x, y in zip(df["monthName"], df["year"])
        ]

        df = (
            df.groupby(
                ["date", "mes", "yearMonth", "monthName", "semana", "sensors"]
            )
            .sum()
            .reset_index()
        )

    return df


def plot_daily_ph(df_ph_average: pd.DataFrame, sensor_list: List) -> go.Figure:

    df_ph_farm = df_ph_average.sort_values(["time"])

    fig = tls.make_subplots(
        rows=1, cols=1, shared_xaxes=True, print_grid=False
    )

    for i in sensor_list:
        fig.add_trace(
            go.Scatter(
                x=df_ph_farm[df_ph_farm["sensors"] == i].time,
                y=df_ph_farm[df_ph_farm["sensors"] == i]["pH"],
                mode="lines",
                connectgaps=False,
                legendgroup="H" + i,
                hovertemplate="pH: %{y:.2f}" + "<br>Fecha y hora: %{x}",
                name="" + i,
            )
        )

    layout = go.Layout(xaxis={"type": "category"})

    fig.add_trace(
        go.Scatter(
            x=df_ph_farm["time"],
            y=df_ph_farm["min_alert"],
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
            x=df_ph_farm["time"],
            y=df_ph_farm["max_alert"],
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
            x=df_ph_farm["time"],
            y=df_ph_farm["min_standard"],
            mode="lines",
            name="pH óptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            showlegend=False,
            legendgroup="optimo",
            hovertemplate="pH mínimo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_ph_farm["time"],
            y=df_ph_farm["max_standard"],
            mode="lines",
            name="pH óptimo",
            opacity=1,
            line=dict(dash="dash"),
            line_color="rgba(0, 177, 106, 0.5)",
            fill="tonexty",
            legendgroup="optimo",
            fillcolor="rgba(0, 177, 106, 0.13)",
            hovertemplate="pH máximo: %{y:.2f}" + "<br>Fecha y hora: %{x}",
        )
    )

    fig.update_layout(
        width=850,
        title="pH Diario",
        xaxis_title="Fecha",
        yaxis_title="pH",
        legend_title="Sensores",
    )

    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True, tick0=0, dtick=0.5)

    return fig


def plot_flat_daily_ph(
    df_ph_average: pd.DataFrame, df_daily_ph: pd.DataFrame, sensor_list: List
) -> go.Figure:

    data = [
        go.Scatter(
            x=df_ph_average[df_ph_average["sensors"] == i]
            .sort_values("time")
            .time,
            y=df_ph_average[df_ph_average["sensors"] == i]
            .sort_values("time")
            .pH.diff(),
            mode="lines",
            name=i,
            hovertemplate="Variación de pH: %{y:.2f}"
            + "<br>Fecha y hora: %{x}",
            legendgroup=i,
        )
        for i in sensor_list
    ]

    layout = go.Layout(
        title="Variación pH Planta",
        xaxis=dict(title="Fecha"),
        width=850,
        yaxis=dict(title="Delta pH"),
        legend={"traceorder": "normal"},
    )

    fig = go.Figure(data=data, layout=layout)

    fig.add_trace(
        go.Scatter(
            x=df_ph_average[df_ph_average["sensors"] == sensor_list[0]]
            .sort_values("time")
            .time,
            y=[-2 * df_daily_ph.pH_std.mean()]
            * df_ph_average[df_ph_average.sensors == sensor_list[0]].shape[0],
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
            x=df_ph_average[df_ph_average["sensors"] == sensor_list[0]]
            .sort_values("time")
            .time,
            y=[2 * df_daily_ph.pH_std.mean()]
            * df_ph_average[df_ph_average.sensors == sensor_list[0]].shape[0],
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
    fig.update_yaxes(showspikes=True, tick0=0, dtick=0.5)

    return fig


def plot_hourly_ph(
    df_ph_average: pd.DataFrame, sensor_list: List
) -> go.Figure:

    df_ph3 = (
        df_ph_average.groupby(["hour", "sensors"])
        .agg({"pH": ["mean", "std"]})
        .reset_index()
    )

    df_ph3 = df_ph3.set_axis(
        ["hour", "sensors", "mean", "std"], axis=1, inplace=False
    )

    fig = tls.make_subplots(
        rows=1, cols=1, shared_xaxes=True, print_grid=False
    )

    df_ph3 = df_ph3.sort_values(["hour"])

    for i in sensor_list:
        fig.add_trace(
            go.Scatter(
                x=df_ph3[df_ph3["sensors"] == i].hour,
                y=df_ph3[df_ph3["sensors"] == i]["mean"],
                mode="lines",
                legendgroup="H" + i,
                name="" + i,
                hovertemplate="temp promedio: %{y:.2f}" + "<br>Fecha: %{x}",
            )
        )

    fig.update_layout(legend_traceorder="reversed")

    fig.update_layout(
        width=850,
        title="pH por horas",
        xaxis_title="horas",
        yaxis_title="pH",
        legend_title="Sensores",
    )

    fig.update_xaxes(showspikes=True)

    fig.add_trace(
        go.Scatter(
            x=df_ph3.hour,
            y=df_ph3["mean"] + df_ph3["std"],
            mode="lines",
            line=dict(width=1),
            showlegend=False,
            line_color="rgba(0, 177, 106, 0.5)",
            legendgroup="std",
            hovertemplate="pH: %{y:.2f}" + "<br>Fecha y hora: %{x}",
            name="Desviación estandar",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_ph3.hour,
            y=df_ph3["mean"] - df_ph3["std"],
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

    fig.update_yaxes(showspikes=True, tick0=2, dtick=0.5, range=[2, 5])

    return fig


def plot_average_ph(df_ph_average: pd.DataFrame) -> go.Figure:

    df_ph4 = (
        df_ph_average.groupby(["date", "year", "sensors"])
        .agg({"pH": ["mean", "std", "max", "mean"]})
        .reset_index()
    )
    df_ph4 = df_ph4.set_axis(
        ["date", "year", "sensors", "mean", "std", "max", "mean"],
        axis=1,
        inplace=False,
    )
    dias = df_ph4.year.count()
    df_ph4 = (
        df_ph_average.groupby(["year", "sensors"])
        .agg({"pH": ["mean", "std", "max", "mean"]})
        .reset_index()
    )
    df_ph4 = df_ph4.set_axis(
        ["year", "sensors", "mean", "std", "max", "mean"],
        axis=1,
        inplace=False,
    )
    df_ph4

    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=df_ph4.iloc[0][2],
            number={"prefix": "pH "},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )

    fig.update_layout(
        paper_bgcolor="lightgray",
        title="Valor de pH promedio de " + str(dias) + " días.",
        width=400,
        height=400,
    )

    return fig


def plot_ideal_ph(df_ph: pd.DataFrame, houses_list: List) -> go.Figure:

    idealpH = {}
    for i in houses_list:
        idealpH["pH_ideal" + str(i)] = (
            np.sum(df_ph[df_ph.House == i]["confortpH"])
            * 100
            / df_ph[df_ph.House == i].shape[0]
        )

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
            # Porcentaje del tiempo en el rango ideal
            value=idealpH["pH_idealLa Loteria"],
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": "Porcentaje dentro del pH óptimo",
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
        title_text="Porcentaje del tiempo en el rango de pH ideal (4 - 5)",
        showlegend=True,
    )

    return fig


def plot_daily_water_consumption(df_water: pd.DataFrame) -> go.Figure:

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    ###########

    inhiProm = (
        df_water.groupby(["date"])
        .agg({"litros": ["sum", "max", "min", "std", "median", "mean"]})
        .reset_index()
    )

    inhiProm.columns = ["_".join(x) for x in inhiProm.columns.ravel()]

    inhiProm.rename(
        columns={"sensors_": "sensors", "date_": "date"}, inplace=True
    )

    inhiProm = inhiProm.sort_values(["date"])

    inhiProm

    ###########

    fig.add_trace(
        go.Scatter(
            x=df_water[df_water["sensors"] == "Citroquim"].date,
            y=df_water[df_water["sensors"] == "Citroquim"]["litros"],
            mode="lines",
            visible=True,
            legendgroup="H" + "Citroquim",
            name="Citroquim",
            hovertext=[
                "Fecha: {} <br>Litros: {:0.2f} <br>Sensor: {}".format(w, x, y)
                for w, x, y in zip(
                    df_water[df_water["sensors"] == "Citroquim"]["date"],
                    df_water[df_water["sensors"] == "Citroquim"]["litros"],
                    df_water[df_water["sensors"] == "Citroquim"]["sensors"],
                )
            ],
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df_water[df_water["sensors"] == "Consumo de agua"].date,
            y=df_water[df_water["sensors"] == "Consumo de agua"]["m3"],
            mode="lines",
            visible=True,
            legendgroup="H" + "Consumo de agua",
            name="Consumo de agua",
            hovertext=[
                "Fecha: {} <br>Litros: {:0.2f} <br>Sensor: {}".format(w, x, y)
                for w, x, y in zip(
                    df_water[df_water["sensors"] == "Consumo de agua"]["date"],
                    df_water[df_water["sensors"] == "Consumo de agua"][
                        "litros"
                    ],
                    df_water[df_water["sensors"] == "Consumo de agua"][
                        "sensors"
                    ],
                )
            ],
        ),
        secondary_y=True,
    )

    fig.update_layout(
        width=800,
        title="Consumos diarios",
        xaxis_title="Fecha",
        legend_title="Líneas",
    )

    fig.update_yaxes(
        showspikes=True,
        tick0=0,
        dtick=0.5,
        title_text="Consumo de <b>Citroquim</b> (litros)",
        secondary_y=False,
    )

    fig.update_yaxes(
        showspikes=True,
        tick0=0,  # dtick=0.5,
        title_text="Consumo de <b>Agua</b> (m<sup>3</sup>)",
        secondary_y=True,
    )

    return fig


def get_weekly_df_water(df_water: pd.DataFrame) -> pd.DataFrame:

    df_week_water = (
        df_water.groupby(
            ["sensors", "yearMonth", "monthName", "mes", "semana"]
        )
        .agg({"litros": ["sum"], "m3": ["sum"]})
        .reset_index()
    )

    df_week_water.columns = [
        "_".join(x) for x in df_week_water.columns.ravel()
    ]

    df_week_water.rename(
        columns={
            "monthName_": "Mes del año",
            "mes_": "Mes",
            "sensors_": "sensors",
            "semana_": "semana",
            "yearMonth_": "yearMonth",
        },
        inplace=True,
    )

    df_week_water = df_week_water.sort_values(["semana"])

    return df_week_water


def plot_weekly_water_consumption(df_week_water: pd.DataFrame) -> go.Figure:

    inhiPromSem = (
        df_week_water.groupby(["semana"])
        .agg(
            {
                "litros_sum": ["sum", "max", "min", "std", "median", "mean"],
                "m3_sum": ["sum", "max", "min", "std", "median", "mean"],
            }
        )
        .reset_index()
    )

    inhiPromSem.columns = ["_".join(x) for x in inhiPromSem.columns.ravel()]

    inhiPromSem.rename(
        columns={
            "Sensor_": "Sensor",
            "semana_": "semana",
            "litros_sum_sum": "litros_sum",
            "litros_sum_max": "litros_max",
            "litros_sum_min": "litros_min",
            "litros_sum_std": "litros_std",
            "litros_sum_median": "litros_median",
            "litros_sum_mean": "litros_mean",
            "m3_sum_sum": "m3_sum",
            "m3_sum_max": "m3_max",
            "m3_sum_min": "m3_min",
            "m3_sum_std": "m3_std",
            "m3_sum_median": "m3_median",
            "m3_sum_mean": "m3_mean",
        },
        inplace=True,
    )
    inhiPromSem = inhiPromSem.sort_values(["semana"])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    df_week_water = df_week_water.sort_values(["semana"])

    fig.add_trace(
        go.Scatter(
            x=df_week_water[df_week_water["sensors"] == "Citroquim"].semana,
            y=df_week_water[df_week_water["sensors"] == "Citroquim"][
                "litros_sum"
            ],
            mode="lines",
            visible=True,
            legendgroup="H" + "Citroquim",
            hovertemplate="Litros: %{y:.2f}" + "<br>Semana: %{x}",
            name="Citroquim",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df_week_water[
                df_week_water["sensors"] == "Consumo de agua"
            ].semana,
            y=df_week_water[df_week_water["sensors"] == "Consumo de agua"][
                "m3_sum"
            ],
            mode="lines",
            visible=True,
            legendgroup="H" + "Consumo de agua",
            hovertemplate="Litros: %{y:.2f}" + "<br>Semana: %{x}",
            name="Consumo de agua",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        width=800,
        title="Consumo semanal en litros",
        xaxis_title="Semana",
        legend_title="Líneas",
    )

    fig.update_yaxes(
        title_text="Consumo de <b>Citroquim</b> (litros)", secondary_y=False
    )

    fig.update_yaxes(
        title_text="Consumo de <b>Agua</b> (m<sup>3</sup>)", secondary_y=True
    )

    return fig


def get_monthly_df_water(df_week_water: pd.DataFrame) -> pd.DataFrame:

    df_month_water = (
        df_week_water.groupby(["sensors", "Mes", "yearMonth", "Mes del año"])
        .agg({"litros_sum": ["sum"], "m3_sum": ["sum"]})
        .reset_index()
    )

    df_month_water.columns = [
        "_".join(x) for x in df_month_water.columns.ravel()
    ]

    df_month_water.rename(
        columns={
            "litros_sum_": "litros",
            "Mes_": "Mes",
            "Mes del año_": "Mes del año",
            "sensors_": "sensors",
            "litros_sum_sum": "litros",
            "m3_sum_sum": "m3",
            "yearMonth_": "yearMonth",
        },
        inplace=True,
    )

    df_month_water = df_month_water.sort_values(["Mes"])

    return df_month_water


def plot_monthly_citroquim_consumption(
    df_month_water: pd.DataFrame,
) -> go.Figure:

    inhiProm = (
        df_month_water.groupby(["Mes"])
        .agg({"litros": ["sum"], "m3": ["sum"]})
        .reset_index()
    )

    inhiProm.columns = ["_".join(x) for x in inhiProm.columns.ravel()]

    inhiProm.rename(
        columns={
            "Mes_": "Mes",
            "litros_sum": "Total general litros",
            "m3_sum": "Total general m3",
        },
        inplace=True,
    )
    inhiProm = inhiProm.sort_values(["Mes"])

    df_month_water = pd.merge(df_month_water, inhiProm, on="Mes", how="left")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df_month_water[df_month_water["sensors"] == "Citroquim"][
                "yearMonth"
            ],
            y=df_month_water[df_month_water["sensors"] == "Citroquim"][
                "litros"
            ],
            legendgroup="H" + "Citroquim",
            showlegend=True,
            hovertemplate="Litros: %{y:.2f}" + "<br>Mes: %{x}",
            name="" + "Citroquim",
        ),
        secondary_y=False,
    )

    fig.update_layout(
        width=800,
        title="Consumo mensual de Citroquim",
        xaxis_title="Mes del año",
        yaxis_title="Litros",
        legend_title="Líneas",
        xaxis=dict(dtick=1),
        yaxis=dict(
            title="Mes del año",
            showline=True,
            showgrid=False,
            showticklabels=True,
        ),
        yaxis2=dict(
            title="Mes del año",
            showline=True,
            showgrid=False,
            showticklabels=True,
            side="right",
            overlaying="y",
        ),
    )
    fig.update_yaxes(showspikes=False)

    fig.update_yaxes(
        title_text="Consumo de <b>Citroquim</b> (lts)", secondary_y=False
    )

    fig.update_yaxes(title_text="Consumo de <b>Agua</b>", secondary_y=True)

    fig.update_xaxes(
        categoryorder="array",
        categoryarray=[
            "Septiembre-2021",
            "Octubre-2021",
            "Noviembre-2021",
            "Diciembre-2021",
            "Enero-2022",
            "Febrero-2022",
            "Marzo-2022",
            "Abril-2022",
            "Mayo-2022",
            "Junio-2022",
        ],
    )

    return fig


def plot_monthly_water_consumption(df_month_water: pd.DataFrame) -> go.Figure:

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df_month_water[df_month_water["sensors"] == "Consumo de agua"][
                "yearMonth"
            ],
            y=df_month_water[df_month_water["sensors"] == "Consumo de agua"][
                "m3"
            ],
            legendgroup="H" + "Consumo de agua",
            showlegend=True,
            hovertemplate="Metros cúbicos: %{y:.2f}" + "<br>Mes: %{x}",
            name="" + "Consumo de agua",
        ),
        secondary_y=False,
    )

    fig.update_layout(
        width=800,
        title="Consumo mensual de Agua",
        xaxis_title="Mes del año",
        yaxis_title="Metros cúbicos",
        legend_title="Líneas",
        xaxis=dict(dtick=1),
        yaxis=dict(
            title="Mes del año",
            showline=True,
            showgrid=False,
            showticklabels=True,
        ),
        yaxis2=dict(
            title="Mes del año",
            showline=True,
            showgrid=False,
            showticklabels=True,
            side="right",
            overlaying="y",
        ),
    )
    fig.update_yaxes(showspikes=False)

    fig.update_yaxes(
        title_text="Consumo de <b>Agua</b> (m<sup>3</sup>)", secondary_y=False
    )

    fig.update_xaxes(
        categoryorder="array",
        categoryarray=[
            "Septiembre-2021",
            "Octubre-2021",
            "Noviembre-2021",
            "Diciembre-2021",
            "Enero-2022",
            "Febrero-2022",
            "Marzo-2022",
            "Abril-2022",
            "Mayo-2022",
            "Junio-2022",
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

    com_farm = company + " - " + farm

    # Graphs Data List
    list_data = list()

    current_date = time.strftime("%d-%m-%y")

    # ------------- pH -------------

    df_sensors_ph = get_sensors(company, farm, "pH")

    df_ph = get_sensor_data(df_sensors_ph, ini_date, end_date)

    df_ph = process_data(
        df_ph, "pH", min_standard, max_standard, min_alert, max_alert
    )

    # ------- df_ph_average -----

    df_ph_average = (
        df_ph.groupby(["time", "date", "sensors"]).mean().reset_index()
    )
    df_ph_average["year"] = df_ph_average["time"].dt.year
    df_ph_average["month"] = df_ph_average["time"].dt.month_name(
        locale="Spanish"
    )
    df_ph_average["yearMonth"] = [
        str(x) + "-" + str(y)
        for x, y in zip(df_ph_average["month"], df_ph_average["year"])
    ]

    sensor_list = df_ph_average.sensors.unique()

    houses_list = df_ph.House.unique()

    houses_list.sort()

    # ----------------------- Daily pH -----------------------

    fig = plot_daily_ph(df_ph_average, sensor_list)

    text = "Muestra los valores de pH"

    data = {
        "values": fig,
        "title": "Niveles de pH",
        "subtitle": None,
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    df_daily_ph = (
        df_ph.groupby(["sensors"]).agg({"pH": ["mean", "std"]}).reset_index()
    )

    df_daily_ph.columns = ["_".join(x) for x in df_daily_ph.columns.ravel()]

    df_daily_ph.rename(
        columns={"sensors_": "sensors", "time_": "time"}, inplace=True
    )

    # ----------------------- Daily flat pH -----------------------

    fig = plot_flat_daily_ph(df_ph_average, df_daily_ph, sensor_list)

    text = "Muestra la variación del pH. Ideal no variar más de 2 desviaciones estandard."

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Variación de pH",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # ----------------------- Hourly pH -----------------------

    fig = plot_hourly_ph(df_ph_average, sensor_list)

    text = "Muestra cuantos puntos varía el pH cada hora, no debe superar 2 desviaciones estandar."

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Variación de pH cada hora",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # ----------------------- Average pH -----------------------

    df_ph_average["year"] = df_ph_average["time"].dt.year

    df_ph_average["month"] = df_ph_average["time"].dt.month

    fig = plot_average_ph(df_ph_average)

    text = "Este es el valor promedio de pH durante todo el tiempo medido."

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Promedio de pH general",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # ----------------------- Confort pH processings-----------------------

    df_ph["confortpH"] = [
        True if x <= y and y <= z else False
        for x, y, z in zip(
            df_ph["min_standard"], df_ph.pH, df_ph["max_standard"]
        )
    ]

    fig = plot_ideal_ph(df_ph, houses_list)

    text = "El pH está entre 4 y 5 más del 88% del tiempo."

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Tiempo (%) del pH dentro de los niveles optimos",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # Water Flow

    df_sensors_water = get_sensors(company, farm, "water")

    df_water = get_sensor_data(df_sensors_water, ini_date, end_date)

    df_water = process_data(df_water, "water")

    df_water = df_water.sort_values(["date"])

    # ------------- General Average - Daily Consumption -------------

    fig = plot_daily_water_consumption(df_water)

    text = "Entrega los valores de consumo de Citroquim cada día en Litros"

    data = {
        "values": fig,
        "title": "Consumo de Citroquim y Agua",
        "subtitle": "Diario",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # ----------------------- Weekly Consumption -----------------------

    df_week_water = get_weekly_df_water(df_water)

    fig = plot_weekly_water_consumption(df_week_water)

    text = "Entrega los valores de consumo de Citroquim cada semana en litros"

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Semanal",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    # ----------------------- Monthly Consumption -----------------------

    df_month_water = get_monthly_df_water(df_week_water)

    fig = plot_monthly_citroquim_consumption(df_month_water)

    text = (
        "La gráfica muestra el consumo total de Citroquim en litros mes a mes."
    )

    data = {
        "values": fig,
        "title": None,
        "subtitle": "Mensual",
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    fig = plot_monthly_water_consumption(df_month_water)

    text = "La gráfica muestra el consumo total de agua en litros mes a mes."

    data = {
        "values": fig,
        "title": None,
        "subtitle": None,
        "text": text,
        "type": "Graph",
    }

    list_data.append(data)

    html_doc = to_html(list_data, com_farm)

    with open(
        report_name + " " + current_date + ".html", "w"
    ) as f:
        f.write(html_doc)


if __name__ == "__main__":
    main()