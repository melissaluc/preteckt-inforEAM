import requests
from helpers.constants import AUTH_TOKEN, PM_BASE_URL
import logging
import os
import ssl
import certifi
from urllib.request import urlopen
import pandas as pd
import argparse
import itertools
import time
from typing import Generator, Optional
import helpers
from helpers import timeConverter

def getRequest(URL_endpt, params=None):
    """
    Return get response as list of DataFrame
    """
    global BASE_URL; AUTH_TOKEN
    
    PAGE_SIZE = 100000
    headers = {"Authorization": f"Token {AUTH_TOKEN}"}
    URL = "/".join([PM_BASE_URL,URL_endpt])
    # TODO: update URL List to params dict
    params = helpers.cleanDict(params)
    params = params|{"page_size": PAGE_SIZE}

    results_ls = []  
    next_page = URL
    while next_page is not None:
        resp = requests.get(URL, headers=headers, params=params ,verify=False)
        if resp.status_code == 200:
            payload = resp.json()
            next_page = payload["next"]
            logging.info(f"Got {len(payload['results'])} items. Next: {next_page}")
            try: 
                data = pd.DataFrame(payload["results"])
            except Exception as e:
                data = []
            results_ls.append(data)
            URL = next_page
        else:
            print(f"Got {resp.status_code}... trying again in 5s.")
            time.sleep(5)


    return results_ls



def getAccelerometer(
                    unit_number=None,
                    from_time=None,
                    to_time=None
                    ):
    """
    Accelerometer Data
    This is the API for acceleration events for a specific Preteckt Unit. All requests to this and associated endpoints must be authenticated. This api is subject to change.

    unit_number: (Required) The Preteckt unit number associated with the vehicle. For example: ?unit_number=112.
    from_time: The beginning of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS (in UTC)
    to_time: The end of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS (in UTC)
    If from_time and to_time are both omitted, all available data will be returned. Warning: This could be a very large data set. It's best to specify a date range if possible.

    [OUTPUT]
    t: The timestamp from the device that recorded the data (e.g. the Preteckt Unit)
    ax: Raw accelerometer reading on the x-axis (in g).
    ay: Raw accelerometer reading on the y-axis (in g).
    az: Raw accelerometer reading on the z-axis (in g).
    gx: Raw gyroscope reading on the x-axis (in deg/s).
    gy: Raw gyroscope reading on the y-axis (in deg/s).
    gz: Raw gyroscope reading on the z-axis (in deg/s).
    mx: Raw Magnetometer reading on the x-axis (in Gauss)
    my: Raw Magnetometer reading on the y-axis (in Gauss)
    mz: Raw Magnetometer reading on the z-axis (in Gauss)
    """
    if from_time!= None: 
        from_time = timeConverter.convertEpochtoDT(from_time)
    if to_time!= None: 
        to_time = timeConverter.convertEpochtoDT(to_time)
    URL_endpt = "rtdv/accelerometer/"
    params = {
                "unit_number": unit_number,
                "from_time": from_time,
                "to_time": to_time
    }

    response = getRequest(URL_endpt, params=params)
    return response

def getGPS(
            unit_number=None,
            from_time=None,
            to_time=None
            ):
    """
    Gps Data
    This endpoint returns GPS information for a given Preteckt Unit.
    The following parameters may be accepted by this endpoint.

    unit_number: (Required) The Preteckt unit number associated with the vehicle. For example: ?unit_number=112.
    from_time: The beginning of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS (in UTC)
    to_time: The end of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS (in UTC)
    If from_time and to_time are both omitted, all available GPS data will be returned. Warning: This could be a very large data set. It's best to specify a date range if possible.

    [OUTPUT]
    t: The timestamp acquired from GPS (in UTC), i.e. the Fix timestamp.
    lat: Latitude in decimal degrees.
    lon: Longitude in decimal degrees.
    spd_over_grnd: Speed in kilometers / hour.
    timestamp: Timestamp acquired from GPS (in UTC)
    altitude: Altitude in Meters (if available)
    bearing: (may be null)
    accuracy: (may be null)
    """
    if from_time!= None: 
        from_time = timeConverter.convertEpochtoDT(from_time)
    if to_time!= None: 
        to_time = timeConverter.convertEpochtoDT(to_time)
    params = {
        "unit_number": unit_number,
        "from_time": from_time,
        "to_time": to_time
    }
    URL_endpt = "rtdv/gps/"

    response = getRequest(URL_endpt, params=params)
    return response

def getChartData(
            unit_number=None,
            spn=None,
            from_time=None,
            to_time=None,
            alert_type=None
            ):
    """
    Chart Data
    This endpoint provides the timeseries data for the Data Viewer. 
    It provides read-only data, and only accepts GET requests that include one or more of the following parameters.

    unit_number: (Required) The Preteckt unit number associated with the vehicle. For example: ?unit_number=112.
    spn: (Required) One or more SPN values to plot. For example: ?spn=100&spn=97 (Alternatively, you may provide the ID for a sensor group; read below for more information)
    from_time: The beginning of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS
    to_time: The end of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS
    alert_type: (optional). If provided, this endpoint will "remember" the last set of SPNs included for the given alert type for an authenticated user. Providing this value will pre-populate SPNs per user, per alert type.
    If from_time and to_time are omitted, the default time window is set to the past 2 days.

    [OUTPUT]
    spns: A list of dicts describing the SPNs (including units of measure)
    columns: the column names for point data.
    points: a list of point data columns
    timing: Amount of time taken to generate the result (in ms)


    https://dash.preteckt.us/api/rtdv/chart-data/

    """

    params = {
        "unit_number": unit_number,
        "spn":spn,
        "from_time": from_time,
        "to_time": to_time,
        "alert_type":alert_type
    }
    URL_endpt = "rtdv/chart-data/"

    response = getRequest(URL_endpt, params=params)
    return response

def getCAN(
            unit_number=None,
            spn=None,
            from_time=None,
            to_time=None,
            precision=None,
            sg=None,
            use_imperial=0
            ):
    """
    Can Data Api
    This endpoint provides read-only CAN bus timeseries data. It only accepts GET requests that include one or more of the following parameters.


    [OUTPUT]
    spns: A list of dicts describing the SPNs (including units of measure)
    columns: the column names for point data.
    points: a list of point data columns
    timing: Amount of time taken to generate the result (in ms)

    [PARAMS]
    unit_number: (Required) The Preteckt unit number associated with the vehicle. For example: ?unit_number=112.
    spn: (Required) One or more SPN values to plot. For example: ?spn=100&spn=97 (Alternatively, you may provide the ID for a sensor group; read below for more information)
    from_time: The beginning of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS
    to_time: The end of the time window for data; The accepted format is: YYYY-mm-ddTHH:MM:SS
    precision: (optional) If specified, this controls how many digits are included after the decimal point for all floating-point values. The default is 3.
    sg: (optional) Sensor Group: Provide the ID for a sensor group, and this request will be populated with the SPNs defined within that group. E.G.:?sg=123&sg=456. You may include more than one sensor group, and sensor groups may be included alongside spn values.
    use_imperial: (optional) Controls the system of measure for all returned data. Any integer value other than 0 will convert to US/imperial units. E.G.:?use_imperial=1. All other values will evaluate to 0, the default, which will return metric units.
    If from_time and to_time are omitted, the default time window is set to the past 15 days.

    https://dash.preteckt.us/api/rtdv/can-data/
    params = {
        unit_number:122,
        spn:97, (can provide more than one with spn:100, spn:23, spn:1)
        from_time:YYYY-mm-ddTHH:MM:SS, 
        to_time:YYYY-mm-ddTHH:MM:SS,
        precision:3, (num of decimal points for float values)
        sg:124,  (can provide more than one with sg:100, sg:23, sg:1)
        use_imperial:1 or 0
    }

    """
    params = {
        "unit_number":unit_number,
        "spn":spn,
        "from_time":from_time,
        "to_time":to_time,
        "precision":precision,
        "sg":sg,
        "use_imperial":use_imperial
    }
    URL_endpt = "rtdv/can-data/"

    response = getRequest(URL_endpt, params=params)
    return response

def get_SPN_FMI_Codes(       
                        unit_number=None,
                        grouped=None,
                        from_time=None,
                        to_time=None
        ):
    """
    Active Spn-Fmi Codes
    This endpoint provides information about the active SPNs + FMIs triggered for a vehicle and uses the FaultCodeHistory model. It accepts only GET requests and provides a read-only list of data. You must provide a unit_number as a GET parameter.
    https://dash.preteckt.us/api/rtdv/spns-fmis/

    unit_number: Required. The Preteckt unit number for the vehicle
    grouped: Boolean value, default is false (omitted). If given, results will be a JSON object where values are grouped by SPN.
    from_time: (optional) If provided will filter fault codes starting at or later than the provided time.
    to_time: (optional) If provided will filter fault codes ended at or before the provided time.

    params = {
        unit_number:,
        grouped:,
        from_time:,
        to_time:
    }

    """
    
    params = {
        "unit_number":unit_number,
        "grouped":grouped,
        "from_time":from_time,
        "to_time":to_time
    }
    URL_endpt = "rtdv/spns-fmis/"

    response = getRequest(URL_endpt, params=params)
    return response

def getVehSensors(
                    unit_number=None
                    ):
    """
    Vehicle Sensors
    This endpoint accepts only GET requests, and provides a read-only list of sensors (SPNs) availble on a specified vehicle. You must provide a unit_number as a GET parameter.

    [OUTPUT]
    spn: The SPN number (or 0 for battery voltage)
    description: A description of the SPN
    units: The units in which measurements for this SPN are stored (e.g. V for Voltage or C for temperature in Celcius.
    https://dash.preteckt.us/api/rtdv/sensors/
    params ={
        unit_number:123;
    }
    """
    params ={
        "unit_number":unit_number
    }
    URL_endpt = "rtdv/sensors/"

    response = getRequest(URL_endpt, params=params)
    return response

def getUnitList(
                    unit_number=None,
                    fleet_id=None,
                    group_id=None
                ):
    """
    Unit List
    A Preteckt Unit is the device installed in a vehicle that collects data used to provide Vehicle Prognostics.

    [OUTPUT]
    id: The database ID for the Unit.
    fleet: The database ID for the fleet in which the unit is installed.
    status: The status of a unit tells you if the unit is New, has been Shipped to a customer, is Active (collecting data), or if it is Decommissioned or not installed.
    unit_number: A unique number that identifies the Preteckt unit.
    cellid: Cellular ID for the unit.
    version: Software version running on the unit.
    barcode: Barcode ID for the unit.
    notes: Notes regarding the Unit.
    assets: Database ID for Assets in which this unit is installed

    https://dash.preteckt.us/api/units/
    params = {
        unit_number:,
        fleet_id:,
        group_id:
    }

    """
    params = {
        "unit_number":unit_number,
        "fleet_id":fleet_id,
        "group_id":group_id
    }
    URL_endpt = "units/"

    response = getRequest(URL_endpt, params=params)
    return response


def getTirePressHistList(        
            unit_number=None,
            asset_label=None,
            tire=None
        ):
    """
    Tire Pressure History List
    This endpoint exposes Tire Pressure (TPMS) data.

    By default, this endpoint provides a paginated list of TPMS readings that belong to the fleets to which your account has access. You may also request details about an individual entry at /api/tpms/<ID>/, where <ID> is the database ID of the TPMS reading.

    [OUTPUT]
    id: Unique database ID for the tire.
    asset: The database ID of the Asset (or vehicle) on which the tire was installed.
    unit: The database ID of the Unit.
    tire: The database ID for the Tire.
    temperature: The temperature reading.
    pressure: The pressure reading.
    status: The status reading from the TPMS sensor (if available).
    timestamp: The timestamp of the reading (if available).
    updated_on: The last time this information was updated.
    created_on: The date and time on which this record was created.

    https://dash.preteckt.us/api/tpms/
    unit_number: You may filter by preteckt unit numbers, e.g. /api/tpms/?unit_number=1234
    asset_label: You may filter by an Asset's label or slug: e.g. /api/tpms/?asset_label=ABC 123 or /api/tpms/?asset_label=abc-123
    tire: You may filter by a Tire's database ID or a by UUID: e.g. /api/tpms/?tire=42 or /api/tpms/?tire=0f5e91cd-59aa-4f16-a10d-7762149bc5b8

    params = {
        unit_number:,
        asset_label:,
        tire:
    }

    """
    params = {
        "unit_number":unit_number,
        "asset_label":asset_label,
        "tire":time
    }
    URL_endpt = "tpms/"

    response = getRequest(URL_endpt, params=params)
    return response


def getTireHistList(        
                uuid=None,
                fleet=None,
                asset_id=None,
                unit_number=None,
                action=None
        ):
    """
    Tire History List
    This endpoint exposes Tire History.

    By default, this endpoint provides a paginated list of Tire History entries that belong to the fleets to which your account has access. You may also request details about an individual history object at /api/tires-history/<ID>/, where <ID> is the database ID representing the tire.

    [OUTPUT]
    id: Unique database ID for the tire.
    fleet: Database ID for the fleet containing the tire.
    tire: The database ID for the Tire.
    tire_uuid: The UUID for the tire.
    unit: The database ID of the Unit to which this tire was related when this record was created.
    asset: The database ID of the Asset (or vehicle) on which this tire was installed.
    position: The position of the tire.
    action: Describes the action performed with the tire; e.g. installed, removed.
    updated_on: The last time this information was updated.
    created_on: The date and time on which this record was created.

    https://dash.preteckt.us/api/tire-history/
    uuid: you may filter by a tires UUID, e.g. /api/tire-history/?uuid=4af37559-a31c-4b17-af0d-d6a1da03583b
    fleet: you may filter on a Fleet ID, name or slug, e.g. /api/tire-history/?fleet=some-fleet or /api/tire-history/?fleet=123, provided you are a member of that fleet.
    asset_id: you may filter tire history by an Asset's database ID. /api/tire-history/?asset_id=12345.
    unit_number: you may filter tire history by a Preteckt Unit number: /api/tire-history/?unit_number=450.
    action: you may filter tires by an action (currently 'installed' or 'removed'), e.g.: /api/tire-history/?action=installed.

    params = {
        uuid,
        fleet,
        asset_id,
        unit_number,
        action
    }

    """
    params = {
        "uuid":uuid,
        "fleet":fleet,
        "asset_id":asset_id,
        "unit_number":unit_number,
        "action":action
    }
    URL_endpt = "tire-history/"

    response = getRequest(URL_endpt, params=params)
    return response

def getTireList(
                uuid=None,
                tpms_id=None,
                asset_id=None,
                unit_number=None
            ):
    """
    Tire List
    This endpoint exposes details about Tires.

    By default, this endpoint provides a paginated list of tires that belong to the fleets to which your account has access. You may also request details about an individual tire at /api/tires/<ID>/, where <ID> is either the database ID representing the tire or the tire's UUID.
    [OUTPUT]
    id: Unique database ID for the tire.
    fleet: Database ID for the fleet containing the tire.
    uuid: The UUID for the tire.
    tpms_id: The ID for the TPMS sensor installed in the tire.
    description: An arbitrary description of the tire.
    updated_on: The last time this information was updated.
    created_on: The date and time on which this record was created.

    uuid: you may filter by a tire's UUID, e.g. /api/tires/?uuid=4af37559-a31c-4b17-af0d-d6a1da03583b
    tpms_id: you may filter by a TPMS ID: /api/tires/?tpms_id=B0741D. NOTE: This will only return tires that are currently installed on the Asset (vehicle).
    asset_id: you may filter tires by an Asset's database ID. /api/tires/?asset_id=12345. NOTE: this will only return tires that are currently installed on the Asset (vehicle).
    unit_number: you may filter tires by a Preteckt Unit number: /api/tires/?unit_number=450. NOTE: this will only return tires that are currently installed on the Asset (vehicle).
    https://dash.preteckt.us/api/tires/

    params = {
        uuid:,
        tpms_id:,
        asset_id:,
        unit_number:
    }
    """
    params = {
        "uuid":uuid,
        "tpms_id":tpms_id,
        "asset_id":asset_id,
        "unit_number":unit_number
    }
    URL_endpt = "tires/"

    response = getRequest(URL_endpt, params=params)
    return response


def getSensorGroupList():
    """
    Sensor Group List
    Sensor Groups allow users to define a "grouping" of sensors (SPNs) that can be referenced by a single name and/or an ID.

    [OUTPUT]
    id: The database ID for the Sensor Group. Visit /api/sensor-groups/<id>/ to retrieve or update this object directly.
    user: The database ID for the user that created this sensor group. May be null.
    fleet: (required) The database ID of the fleet in which this group belongs. May be null for default sensor groups.
    fleet_name: A read-only field; this is the name of the fleet that owns the sensor group.
    public: A Boolean value; if true, this is a group available to every user. A number of these have been created for convenience.
    name: (required): The name for your Sensor group. This must be unique within a fleet.
    spns: (required) An array of SPN values that are grouped together. Note that these are SPNs and not database IDs.
    updated_on: The date on which this sensor group was last updated (UTC).
    created_on The date on which this sensor group was created (UTC).
    """

    if from_time!= None: 
        from_time = timeConverter.convertEpochtoDT(from_time)
    if to_time!= None: 
        to_time = timeConverter.convertEpochtoDT(to_time)

    URL_endpt = "sensor-groups/"

    response = getRequest(URL_endpt, params=params)
    return response


def getRepairPlanCommentList(
                                repairplan=None,
                                unit_number=None,
                                asset_label=None,
                                asset_label_slug=None,
                                since=None
                            ):
    """
    Repair Plan Comment List
    This API endpoint exposes a list of repair plan comments. A repair plan comment is a note added by a technician to a repair plan, providing further information or suggestions. A repair plan comment has an author, a related repair plan, and content.
    [OUTPUT]
    id: The unique database ID for the Repair Plan Comment. You can retrieve data for an individual Repair Plan Comment based on this value by sending a GET request to /api/repairplans/<id>/.
    author: The staff member responsible for creating the Repair Plan Comment.
    repairplan: The associated repair plan for which this comment was created.
    raw_content: The plan description in plain text. Use markdown to format the paragraph.
    rendered_content: The plan description, rendered from raw_content with markdown formatting applied.
    created_on: The timestamp at which a repair plan comment was created.
    updated_on: The timestamp at which a repair plan comment was last updated.

    https://dash.preteckt.us/api/repairplan-comments/
    Filter by Repair Plan ID /api/repairplan-comments/?repairplan=X: Returns repair plan comments for the given repair plan ID. You can also view a collection of repair plan comments using /api/repairplan-comments/?repairplan=X&repairplan=Y.
    Filter by Unit Number [..] /api/repairplan-comments/?unit_number=X: Returns repair plans for the given Unit Number. In this case the provided value should be the Unit's number or serial number.
    Filter by Asset label [..] /api/repairplan-comments/?asset_label=X: Returns repair plans for the given Asset label
    Filter by Asset label slug [..] /api/repairplan-comments/?asset_label_slug=X: Returns repair plans for the given Asset label specified as a slug.
    Filter for repair plan comments created since a given time [..] in UTC, e.g.: /api/repairplan-comments/?since=2017-12-25T00:00:00: Return the repair plan comments created after midnight (UTC) on Christmas 2017.

    params = {
        repairplan:,
        unit_number:,
        asset_label:,
        asset_label_slug:,
        since:2017-12-25T00:00:00
    }

    """
    if since != None: 
        since = timeConverter.convertEpochtoDT(since)

    params = {
        "repairplan":repairplan,
        "unit_number":unit_number,
        "asset_label":asset_label,
        "asset_label_slug":asset_label_slug,
        "since":since
    }

    URL_endpt = "repairplan-comments/"

    response = getRequest(URL_endpt, params=params)
    return response


def getRepairPlanList(
                        alert_id=None,
                        unit_number=None,
                        asset_label=None,
                        additional_state=None,
                        spn=None,
                        since=None
                    ):
    """
    Repair Plan List
    This API endpoint exposes repair plans. A repair plan is a plan created by a technician in response to a generated alert. A repair plan contains information about the author, related alerts, the asset in question, and a description of the proposed plan.

    [OUTPUT]
    id: The unique database ID for the Repair Plan. You can retrieve data for an individual Repair Plan based on this value by sending a GET request to /api/repairplans/<id>/.
    author: The staff member responsible for creating the Repair Plan.
    alerts: The associated alerts for which this repair plan was made.
    asset: The asset for which the repair plan was created.
    asset_label: The display label for the asset. Usually a bus or truck number.
    fleet: The fleet the repair plan was made for.
    fleet_name: The name of the associated fleet.
    raw_content: The plan description in plain text. Use markdown to format the paragraph.
    rendered_content: The plan description, rendered from raw_content with markdown formatting applied.
    state: Repair Plans go through a review process transition through states indicating where they are as part of the process. These include: draft, open, and closed.
    created_on: The timestamp at which a repair plan was created.
    updated_on: The timestamp at which a repair plan was last updated.

    Filter by Alert ID /api/repairplans/?alert=X: Returns repair plans for the given alert ID.
    Filter by Unit Number /api/repairplans/?unit_number=X: Returns repair plans for the given Unit Number. In this case the provided value should be the Unit's number or serial number.
    Filter by Asset label /api/repairplans/?asset_label=X: Returns repair plans for the given Asset label
    Filter by Asset label slug /api/repairplans/?asset_label_slug=X: Returns repair plans for the given Asset label specified as a slug.
    Filter by state: Filter results by their current state, e.g. /api/repairplans/?additional_state=X where X is one of: draft, open, or closed
    Filter by SPN /api/repairplans/?spn=X: Returns repair plans for the given SPN.
    Filter for repair plans modified since a given time in UTC, e.g.: /api/repairplans/?since=2017-12-25T00:00:00: Return the repair plans modified after midnight (UTC) on Christmas 2017.
    https://dash.preteckt.us/api/repairplans/

    params = {
        alert: alert_id,
        unit_number:,
        asset_label:,
        additional_state:,
        spn:,
        since:
    }

    """

    if since != None: 
        since = timeConverter.convertEpochtoDT(since)

    params = {
        "alert": alert_id,
        "unit_number":unit_number,
        "asset_label":asset_label,
        "additional_state":additional_state,
        "spn":spn,
        "since":since
    }
    URL_endpt = "repairplans/"

    response = getRequest(URL_endpt, params=params)
    return response

def getFautCodeHistList(
                            unit_number=None,
                            from_time=None,
                            to_time=None,
                            spn=None,
                            fmi=None,
                            source=None
                    ):
    """
    Fault Code History List
    This endpoint exposes details for active fault codes (or DTCs) for a vehicle.

    [OUTPUT]
    id: Unique database ID for the fault code entry.
    asset: The Unique database ID for the Asset (vehicle) to which this fault code is related
    unit_number: The Preteckt Unit number (or serial) for the data logging device.
    start_time: Starting time for the active fault code.
    end_time: Ending time for the active fault code.
    duration: The duration of the fault code (in seconds)
    spn: The (integer) SPN for the fault code.
    spn_description: A description for the SPN.
    fmi: The (integer) FMI for the fault code.
    fmi_description: A description of the FMI.
    source: The source address for the fault code.
    source_description: A short description for the source address.
    source_long_description: A longer description for the source address.
    count: The fault code count.
    meta: (optional) any additional meta data for the fault code. This will be either null or a JSON object.
    updated_on: The timestamp on which the fault code history entry was last updated.
    created_on: The timestamp on which the fault code history entry was created.


    unit_number: The Preteckt unit number for the vehicle
    from_time: (optional) If provided will filter fault codes starting at or later than the provided time. Expected format: YYYY-MM-DDThh:mm:ss in UTC.
    to_time: (optional) If provided will filter fault codes ended at or before the provided time. Expected format: YYYY-MM-DDThh:mm:ss in UTC.
    spn: (optional) Return faults that match the given SPN
    fmi: (optional) Return faults that match the given FMI
    source: (optional) Return only faults that match the given source address
    https://dash.preteckt.us/api/fault-history/

    params = {
        unit_number:,
        from_time:,
        to_time:,
        spn:,
        fmi:,
        source:
    }
    """
    if from_time!= None: 
        from_time = timeConverter.convertEpochtoDT(from_time)
    if to_time!= None: 
        to_time = timeConverter.convertEpochtoDT(to_time)

    params = {
        "unit_number":unit_number,
        "from_time":from_time,
        "to_time":to_time,
        "spn":spn,
        "fmi":fmi,
        "source":source
    }
    URL_endpt = "fault-history/"

    response = getRequest(URL_endpt, params=params)
    return response

def getFaultCodeList(
                            spn=None,
                            fmi=None,
                            source=None,
                            manufacturer=None,
                            year=None,
                            series=None
                ):
    """
    Fault Code List
    This endpoint exposes details about FaultCode (i.e. DTCs) and their related RepairRecommendations.

    spn: A fault code's Suspect Parameter Number (or SPN)
    fmi: A fault code's Failure Mode Identifier (or FMI)
    source: The source on which the fault was reported
    manufacturer: An Engine manufacturer
    year: The year in which the engine was manufactured.
    series: The engine's series / model.

    params = {
        spn:,
        fmi:,
        source:,
        manufacturer:,
        year:,
        series:
    }
    """
    params = {
        "spn":spn,
        "fmi":fmi,
        "source":source,
        "manufacturer":manufacturer,
        "year":year,
        "series":series
    }
    URL_endpt = "faultcodes/"

    response = getRequest(URL_endpt, params=params)
    return response

def getFleetList(
        enable_analysis=None,
        enable_rdtv=None,
        active=None,
        enable_reports=None,
        is_r_and_d=None,
        limit_fault_code_sources=None,
        automate_fault_code_repairplans=None,
        enable_scr_conversion_history=None,
        enable_dpf_report=None,
        enable_data_viewer_pre_caching=None
):
    """
    Fleet List
    This API endpoint exposes fleet information

    [OUTPUT]
    id: The database ID for the fleet.
    name: The name of the fleet.
    name_slug: The slugified name of the fleet.
    users: An array of database IDs for all users who are a member of the fleet.
    created_on: Date on which the fleet was created.
    updated_on: Date on which the fleet was last updated.
    enable_analysis: A flag indicating if analysis was performed for the vehicles in this fleet.
    enable_rtdv: A flag indicating if users in this fleet have access to the RTDV.
    active: A flag indicating if this fleet is active in the Dashboard.
    enable_reports: A flag indicating if users in this fleet have access to customer-facing reports.
    is_r_and_d: A flag indicating if the fleet is actively used for research and development.
    limit_fault_code_sources:A flag indicating if fault code alerts will only be displayed on the Technician Dashboard if they are relevant.
    automate_fault_code_repairplans: A flag indicating if this fleet will receive automatically-created repair plans for well-known fault codes.
    enable_scr_conversion_history: A flag indicating if the SCR conversion history is available for the fleet.
    enable_dpf_report: A flag indicating if the DPF health report is available for the fleet.
    enable_data_viewer_pre_caching: A flag indicating if the data viewer pre-catching is available for the fleet.

    This endpoint accepts the following fields; Each of these can be specified as a GET param, e.g. ?enable_analysis=true or ?active=false.
    Each of the following are boolean feature flags and accept values of true or false.
    enable_analysis
    enable_rtdv
    active
    enable_reports
    is_r_and_d
    limit_fault_code_sources
    automate_fault_code_repairplans
    enable_scr_conversion_history
    enable_dpf_report
    enable_data_viewer_pre_caching
    https://dash.preteckt.us/api/fleet/
    params = {
        enable_anbalysis:,
        enable_rdtv:,
        active:,
        enable_reports:,
        is_r_and_d:,
        limit_fault_code_sources:,
        automate_fault_code_repairplans:,
        enable_scr_conversion_history:,
        enable_dpf_report:,
        enable_data_viewer_pre_caching:
    }
    """
    params = {
        "enable_analysis":enable_analysis,
        "enable_rdtv":enable_rdtv,
        "active":active,
        "enable_reports":enable_reports,
        "is_r_and_d":is_r_and_d,
        "limit_fault_code_sources":limit_fault_code_sources,
        "automate_fault_code_repairplans":automate_fault_code_repairplans,
        "enable_scr_conversion_history":enable_scr_conversion_history,
        "enable_dpf_report":enable_dpf_report,
        "enable_data_viewer_pre_caching":enable_data_viewer_pre_caching
    }
    URL_endpt = "fleet/"

    response = getRequest(URL_endpt, params=params)
    return response

def getFailureTypeList():
    """
    Failure Type List
    This endpoint exposes details about Failure Types
    [OUTPUT]
    id: Unique id of the Failure
    name: Name of the Failure
    name_slug: Sluggified name field of the Failure
    description: Description of the Failure
    spns: SPNs of the Failure

    https://dash.preteckt.us/api/failure-types/
    """
    URL_endpt = "failure-types/"
    response = getRequest(URL_endpt, params=params)
    return response

def getAssetGroupList(id=None):
    """
    Asset Group List
    This endpoint exposes details about AssetGroups; i.e. arbitrary groupings of assets.
    [OUTPUT]
    id: Unique database ID for the asset.
    fleet: The database ID for the fleet containing the asset.
    name: The name of the AssetGroup.
    description: An optional description for the group.
    updated_on: The last time this information was updated.
    created_on: The date and time on which this record was created.

    You can also retrieve details for a single AssetGroup by sending a GET request to /api/assetgroups/<id>/, where <id> is the Database ID for that AssetGroup.
    https://dash.preteckt.us/api/assetgroups/
    params = {
        id:
    }
    """
    params = {
        "id":id
    }
    URL_endpt = "assetgroups/"

    response = getRequest(URL_endpt, params=params)
    return response

def getAssetList(    
        id=None,    
        unit_number=None,
        asset_label=None,
        fleet=None,
        group_id=None
        ):
    """
    Asset List
    This endpoint exposes details about Assets. An asset is generally a vehicle (e.g. a Truck or a Bus) in which a Preteckt Unit has been installed. An Asset may or may not have an active unit installed.

    [OUTPUT]
    id: Unique database ID for the asset.
    fleet: Database ID for the fleet containing the asset.
    fleet_name: Name of the fleet.
    group: The unique ID of the Group in which the asset belongs (if any).
    group_name: The name of the Group in which the asset belongs (if any).
    unit: The unique database ID for the installed unit (if any).
    unit_number: The Preteckt Unit Number.
    asset_label: Customer-supplied label for the Asset.
    asset_label_slug: A URL-friendly slug generated from the label.
    asset_type: An asset type (typically bus or truck).
    asset_type_display: Human-friendly version of the asset type.
    apu: APU Details
    drive_line: Drive line details.
    engine_series: Engine series.
    engine_capacity: Engine capacity.
    engine_manufacturer: Name of the engine manufacturer.
    make: Vehicle make.
    model: Vehicle model.
    year: Vehicle manufacture year.
    vin: Vehicle identification number.
    odometer: Current odometer reading.
    updated_on: The last time this information was updated.
    created_on: The date and time on which this record was created.

    Additional data fields ¶
    An asset instance (i.e. the response from requesting data for an individual asset: /api/assets/<id>/) may include additional meta-data:

    params = {
        id:
    }

    good_spns: An array of SPNs that are reporting valid values on the vehicle.
    last_data_reported_on: The latest timestamp associated with valid data reported from the vehicle.
    last_checkin: The last time that data was transferred from the vehicle.
    capabilities: Similar to the field on units, this is an array of additional capabilities; currently may include "accelerometer" or "gps".

    -------
    unit_number: Provide a unit number to filter on assets that contain a a given unit; e.g. ?unit_number=123. If you want to view a collection of assets at once, simply filter on multiple units; e.g. ?unit_number=123&unit_number=456.
    asset_label: Filter based on the asset's label. ?asset_label=Bus23. A collection of asset labels can also be viewed; e.g. ?asset_label=Bus23&asset_label=Truck456.
    fleet: Filter based on the fleet to which the asset belongs. This can be a fleet name, slug, or database ID; e.g. ?fleet=123, ?fleet=some-fleet, or ?fleet=Some%20Fleet. You may also filter based on a collection of fleets; e.g. ?fleet=123&fleet=some-other-fleet&fleet=456 to view many fleets simultaneously.
    group_id: Filter based on a group to which the asset belongs. This should be a unique ID; e.g. ?group_id=42.

    https://dash.preteckt.us/api/assets/
    params = {
        unit_number
        asset_label
        fleet
        group_id
    }
    """
    params = {
        "id":id,
        "unit_number":unit_number,
        "asset_label":asset_label,
        "fleet":fleet,
        "group_id":group_id
    }
    URL_endpt = "assets/"

    response = getRequest(URL_endpt, params=params)
    return response


def getAlertList(        
        unit_id=None,
        unit_number=None,
        asset_label=None,
        asset_label_slug=None,
        additional_state=None,
        type=None,
        severity=None,
        tag=None,
        days=None,
        since=None,
        from_date=None,
        to_date=None,
        q=None
        ):
    """
    Alert List
    This API endpoint exposes alerts. An alert is fundamentally information about a problem in a vehicle. The information contained within an alert may vary in a number of ways, but it highlights a region of time during which some problem likely exists.
    [OUTPUT]
    id: The unique database ID for the Alert. You can retrieve data for an individual Alert based on this value by sending a GET request to /api/alerts/<id>/.
    fleet: The unique database ID for the fleet in which this alert belongs.
    fleet_name: The name of the fleet (if any).
    unit_number: The unit unit (or device serial number) for the data collection device installed in the vehicle.
    unit_id: The unique database ID for the Unit.
    asset_id: The unique database ID for the Asset (vehicle).
    asset_label: The customer-provided label for the Asset.
    asset_label_slug: The asset_label as a slug.
    asset_type: The type of the Asset (e.g. bus or truck)
    asset_type_display: A display value for the Asset's type.
    asset_make: The manufacturer make of the vehicle.
    asset_model: The manufacturer model of the vehicle.
    asset_year: The year in which the vehicle was manufactured.
    asset_group_name: Group name for the vehicle (if any).
    start_date: Starting time range during which the alert is active.
    end_date: Ending time range of the alert.
    alert_type:An Alert type. Currently supported alert types are: aftertreatment, cng, faultcode, fuellevel, idletime, charging, oiltemperature, coolanttemperature, treadwear
    alert_type_display: Display value for the above alert type.
    alert_id: A numerical representation of the above alert type. This is an internally used value.
    tags: A list (array) of tags that have been applied to this alert.
    severity: DEPRECATED. A numerical representation of the severity of the alert; Currently supported values range from 0 - 5 with lower values meaning greater severity.
    severity_text: A human-friendly text representation of severity.
    severity_description: A description of the severity level.
    status: DEPRECATED. Status of the alert.
    workflow_state: Alerts that go through a review process transition through states indicating where they are as part of the process. These include: draft, inreview, active, closed or stale.
    workflow_state_display: A display representation of the above.
    short_desc: A short description for the Alert.
    long_desc: A longer description for the alert.
    values: Arbitrary data values that can be stored with the alert. Specify this as a JSON object.
    icon_html: An HTML string containing an icon based on severity.
    created_on: The timestamp at which an alert was created.
    updated_on: The timestamp at which an alert was last updated.
    source: The data source for an alert.
    notes: Any notes associated with the alert. See /api/notes/.
    read_by: An array of User ID's that have viewed / read the alert.
    read: Boolean value that indicates if an alert has been reviewed or read.
    rtdv_url: A URL used to populate data in the RTDV
    bookmarked: Boolean value that indicates if the alert has been bookmarked.
    repair_recommendations: A list (array) of repair recommendations for the Alert.
    failures: A list (array) of Failures based on the alert's type.
    reviewed_by: A list (array) of User IDs who have reviewed this alert.
    rtdv_spns: A list (array) of SAE SPN values that are relevant to the alert.

    Filter by Unit ID /api/alerts/?unit_id=X: Returns alerts for the given unit's ID. In this case the unit is a Database ID, not a Unit number.
    Filter by Unit Number /api/alerts/?unit_number=X: Returns alerts for the given Unit Number. In this case the provided value should be the Unit's number or serial number.
    Filter by Asset label /api/alerts/?asset_label=X: Returns alerts for the given Asset label
    Filter by Asset label slug /api/alerts/?asset_label_slug=X: Returns alerts for the given Asset label specified as a slug.
    Filter by workflow state: Filter results by their current workflow state, e.g. /api/alerts/?additional_state=X where X is one of: draft, inreview, active, closed
    Filter by alert type /api/alerts/?type=X: Returns alerts matching the given alert type: aftertreatment, charging, coolanttemperature, cng, egr, faultcode, fuellevel, global, gps, idletime, oiltemperature, replearning, treadwear
    Filter by severity /api/alerts/?severity=X: Returns alerts matching the given severity level (an integer in the range 0 - 5)
    Filter by tag /api/alerts/?tag=X: Returns alerts matching the given tag. NOTE: Tag input is case sensitive.
    Filter by days, e.g. /api/alerts?days=30: Show alerts from the last 30 days. This filter's on the Alert's created_on field (the date the Alert was generated, NOT the period during which the alert was detected).
    Filter for alerts created since a given time in UTC, e.g.: /api/alerts/?since=2017-12-25T00:00:00: Return the alerts created after midnight (UTC) on Christmas 2017.
    Filter by date range: Filter alerts by a range of dates by including from_date and to_date parameters; This range is applied to the Alert's start_date value. E.g. /api/alerts/?from_date=2021-01-01T00:00:00&to_date=2021-01-01T23:59:59
    Search for Unit or Asset: Filter by fuzzy searching for either a unit number or asset with: /api/alerts/?q=X where X is the value you wish to find.
    https://dash.preteckt.us/api/alerts/#retrieving-alerts

    params = {
        unit_id:
        unit_number:
        asset_label:
        asset_label_slug:
        additional_state: draft | inreview | active | closed
        type: aftertreatment | charging | coolantemperature | cng | egr | faultcode | global | gps | idletime | oiltemperature | replearning | treadwear
        severity: 0-5
        tag:
        days: 30 # from the last 30 days filters on created_on field
        since: 2017-12-25T00:00:00 #UTC time
        from_date:  # This range is applied to the Alert's start_date
        to_date: # This range is applied to the Alert's start_date
        q: # fuzzy search unit_number or asset
    }
    """

    if from_date!= None: 
        from_date = timeConverter.convertEpochtoDT(from_date)
    if to_date!= None: 
        to_date = timeConverter.convertEpochtoDT(to_date)
    if since != None:
        since = timeConverter.convertEpochtoDT(since)

    params = {
        "unit_id": unit_id,
        "unit_number": unit_number,
        "asset_label": asset_label,
        "asset_label_slug": asset_label_slug,
        "additional_state": additional_state,
        "type": type,
        "severity": severity,
        "tag": tag,
        "days": days,
        "since": since,
        "from_date": from_date,
        "to_date": to_date,
        "q": q,
        "status":"active"
    }
    URL_endpt = "alerts/"
    # .set_index("First Name", inplace = True)
    response = getRequest(URL_endpt, params=params)
    return response


