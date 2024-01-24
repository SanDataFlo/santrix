from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import pandas as pd
from pydantic import BaseModel
from typing import List

api_titel = "SanTrix API Container"
api_version = "1.2.1"
api_summary = "API communicates between watsonxAssistant and the database"
server = "https://application-3e.1b7hlo69yoj4.eu-de.codeengine.appdomain.cloud/"


class DeviceItem(BaseModel):
    id: str
    description: str
    stock: int
    manufacturercode: str
    manufacturer_article_id: str
    searchstring: str


class User(BaseModel):
    userid: int
    username: str
    usermail: str
    superior_id: int


class TicketItSupport(BaseModel):
    ticket_id: str
    description: str
    prompt: str
    userid: int
    status: int


class TicketOrder (BaseModel):
    ticket_id: str
    userid: int
    device_id: str
    approval_of_superior: bool


# Create a new FastAPI instance
app = FastAPI(openapi_version="3.0.1")


@app.get("/search_in_asset_list/{query}", response_model=List[DeviceItem])
def search_in_asset_list(query: str):
    # Read the data from an Excel file
    df = pd.read_excel("asset-list.xlsx")
    # Create an empty list to store the JSON objects
    json_results = []
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the query string is present in any of the columns
        if row.str.contains(query, case=False).any():
            # If the query string is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Lagerbestand"], manufacturercode=str(row["Herstellercode"]),  manufacturer_article_id=str(row["Herstellerartikelnr."]), searchstring=row["Suchbegriff"])
            # Add the JSON object to the json_results list
            json_results.append(device_item)
    # Return the json_results list
    return json_results


@app.get("/get_device_by_id/{id}", response_model=DeviceItem)
def get_device_by_id(id: str):
    # Read the data from an Excel file
    df = pd.read_excel("asset-list.xlsx")
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["Nr."] == id:
            # If the userid is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Lagerbestand"],
                                     manufacturercode=str(row["Herstellercode"]),
                                     manufacturer_article_id=str(row["Herstellerartikelnr."]),
                                     searchstring=row["Suchbegriff"])
            return device_item


@app.get("/get_user_by_userid/{userid}", response_model=User)
def get_user_by_userid(userid: int):
    # Read the data from an Excel file
    df = pd.read_excel("hierachy.xlsx")
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["MitarbeiterID"] == userid:
            user = User(userid=userid, username=row["MitarbeiterName"], usermail=row["Mail"], superior_id=row["VorgesetzterID"])
            # Add the JSON object to the json_results list
            return user


@app.get("/get_devices_by_userid/{userid}", response_model=List[DeviceItem])
def get_devices_by_userid(userid: int):
    # Read the data from an Excel file
    df = pd.read_excel("device-management.xlsx")
    # Create an empty list to store the JSON objects
    json_results = []
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the userid is present in the MitarbeiterID column
        if row["MitarbeiterID"] == userid:
            # If the userid is present, create a DeviceItem object and fill the attributes with the values from the Excel file
            device_item = DeviceItem(id=str(row["Nr."]), description=row["Beschreibung"], stock=row["Menge"],
                                     manufacturercode=str(row["Herstellercode"]),
                                     manufacturer_article_id=str(row["Herstellerartikelnr."]),
                                     searchstring=row["Suchbegriff"])
            # Add the JSON object to the json_results list
            json_results.append(device_item)
    # Return the json_results list
    return json_results


@app.get("/openapi.json")
def custom_openapi_json():
    openapi_schema = get_openapi(
        title=api_titel,
        version=api_version,
        summary=api_summary,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/container_trigger")
def container_trigger():
    return


