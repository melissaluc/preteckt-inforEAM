import requests
from helpers.constants import TENANT, USER_FUNCTION_NAME, SYSTEM_FUNCTION_NAME, WINDOW_, USERID, PASSWORD, EWSLANG, ISNAMEDUSER, HXGN_BASE_URL, USERGROUP, CURRENT_DIR
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlencode, quote
import logging 



def sendRequest(REQUEST, URL, payload):
    """
    Returns JSON object
    """
    global TENANT; USER_FUNCTION_NAME, SYSTEM_FUNCTION_NAME; WINDOW_; USERID; PASSWORD; EWSLANG; ISNAMEDUSER; HXGN_BASE_URL; USERGROUP; CURRENT_DIR

    # print(payload)
    if REQUEST == 'POST':
        headers= {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Connection':'keep-alive',
        'Host':'eam-u2alnxapp.metrolinxuat.com',
        'Origin':'https://eam-u2alnxapp.metrolinxuat.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
    elif REQUEST == 'GET':
        headers= {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Connection':'keep-alive',
        'Host':'eam-u2alnxapp.metrolinxuat.com',
        'Origin':'https://eam-u2alnxapp.metrolinxuat.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
    else:
        logging.info('REQUEST can only be POST or GET')


    login_payload = { 
                'USER_FUNCTION_NAME':USER_FUNCTION_NAME,
                'SYSTEM_FUNCTION_NAME':SYSTEM_FUNCTION_NAME,
                'window':WINDOW_,
                'userid':USERID,
                'password':PASSWORD,
                'tenant':TENANT
                }

    with requests.Session() as session:
            # post = session.post(URL, verify=False)
            # post = session.post(f"{HXGN_BASE_URL}/web/base/logindisp", json=payload, verify=False)
            login_page = session.get(f'{HXGN_BASE_URL}/web/base/logindisp')

            login = session.post(f"{HXGN_BASE_URL}/web/base/login",headers=headers, data=urlencode(login_payload), verify=False)
            soup = BeautifulSoup(login.text, 'html.parser')
            script_tag_str = soup.find('script').string
            EAMID = re.search('(?<={"eamid":").*?(?=","external_eamid")', script_tag_str).group(0)

            session_cookies_dict = session.cookies.get_dict()
            session_cookies_dict_new = {f'{key}=': v for key, v in session_cookies_dict.items()}
            session_cookie = ';'.join(key + value for key, value in session_cookies_dict_new.items())
            payload['eamid']=EAMID
            payload = urlencode(payload, quote_via=quote)
            # print(payload)
        

            if REQUEST == 'POST':
                req = session.post(URL,headers=headers,data=payload, verify=False)
            elif REQUEST == 'GET':
                req = session.get(URL,headers=headers, verify=False)
            
            try:
                response=req.json()
                # print(response)
                return response
            except Exception as e:
                response=req.text
                print(response)
                print(e)
            


# DROPDOWN
def postWOType():
    """
    POST request to .../web/base/dropdown get a list of WO Type\n
    TAGNAME = workordertype
    """
    global TENANT;HXGN_BASE_URL

    URL = f"{HXGN_BASE_URL}/web/base/dropdown?"

    payload_list = [
        f"_dc={int(datetime.now().timestamp()*(1000))}",
        f"&GRIDNAME=WOBFMM",
        f"&TAGNAME=workordertype",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    return sendRequest('POST', URL, payload)

def postWOStatus():
    """
    POST request to .../web/base/dropdown to get a list of WO Status\n
    TAGNAME = workorderstatus
    """
    global TENANT;HXGN_BASE_URL

    URL = f"{HXGN_BASE_URL}/web/base/dropdown?"
    payload = {
        "_dc":f"{int(datetime.now().timestamp()*(1000))}",
        "GRIDNAME":"WOBFMM",
        "TAGNAME":"workorderstatus",
        "eamid":None,
        "tenant":TENANT
    }

    return sendRequest('POST', URL, payload)

# LOVPOP
def postClasses():
    """
    POST request .../web/base/LOVPOP to get List of Classes\n
    LOV_TAGNAME = woclass
    # Class (COR-REPA)
    """
    global TENANT;HXGN_BASE_URL

    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
                f"popup=true",
                f"&GRID_NAME=LVCLAS",
                f"&GRID_TYPE=LOV",
                f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
                f"&LOV_TAGNAME=woclass",
                f"&usagetype=lov",
                f"&USER_FUNCTION_NAME=WOBFMM",
                f"&CURRENT_TAB_NAME=HDR",
                f"&LOV_ALIAS_NAME_1=parameter.rentity",
                f"&LOV_ALIAS_VALUE_1=EVNT",
                f"&LOV_ALIAS_TYPE_1=text",
                f"&LOV_ALIAS_NAME_2=param.wotype",
                f"&LOV_ALIAS_VALUE_2=COR",
                f"&LOV_ALIAS_TYPE_2=text",
                f"&LOV_ALIAS_NAME_3=control.org",
                f"&LOV_ALIAS_VALUE_3=BRT",
                f"&LOV_ALIAS_TYPE_3=text",
                f"&eamid={EAMID}",
                f"&tenant={TENANT}"
    ]

    payload = "".join(payload_list)
    
    return sendRequest('POST', URL, payload)
    return
def postPriority():
    """
    POST request .../web/base/LOVPOP to get List of Priority Levels\n
    TAGNAME=priority
    # Priority (1-Urgent, 2-High, 3-Medium, 4-Low, 5-Routine) 

    """
   
    global TENANT;HXGN_BASE_URL

    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
        f"_dc={int(datetime.now().timestamp()*(1000))}",
        f"&GRIDNAME=WOBFMM",
        f"&TAGNAME=priority",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    
    return sendRequest('POST', URL, payload)

# Get last meter reading
def postMTR(BUS_NO):
    """
    POST to .../web/base/OSOBJS.MTR' to get equipment meter readings
    Return lastmeter reading: 'totalusage'' or 'usagesinceinstall'
    """
    global TENANT;HXGN_BASE_URL
    URL = f'{HXGN_BASE_URL}/web/base/OSOBJS.MTR'

    payload = {
            "SYSTEM_FUNCTION_NAME":"OSOBJS",
            "USER_FUNCTION_NAME":"R2OBJS",
            "CURRENT_TAB_NAME":"MTR",
            "equipmentno":f"BUS-{BUS_NO}",
            "organization":"BRT",
            "statusrcode":"I",
            "eamid":None,
            "tenant":TENANT
    }

    response = sendRequest('POST', URL, payload)['pageData']['grid']['GRIDRESULT']['GRID']['DATA'][0]
    lastreading=response['totalusage'].replace(',','')
    # usagesincelastwo= int(response['usagesincelastwo'].replace(',',''))
    # mtr = lastreading - usagesincelastwo
    return lastreading

def postOSOBJ(BUS_NO):
    """
    POST to .../web/base/OSOBJS.xmlhttp to get Equiment Details
    """
    global TENANT;HXGN_BASE_URL

    URL = f'{HXGN_BASE_URL}/web/base/OSOBJS.HDR'
    payload = {
        "SYSTEM_FUNCTION_NAME": "OSOBJS",
        "USER_FUNCTION_NAME": "R2OBJS",
        "CURRENT_TAB_NAME": "HDR",
        "equipmentno": f"BUS-{BUS_NO}",
        "organization": "BRT",
        "statusrcode": "I",
        "SCROLLROW": "YES",
        "ONLY_DATA_REQUIRED": "true",
        "eamid":None,
        "tenant":TENANT
    }
    
    res = sendRequest('POST', URL, payload)['pageData']['values']
    data = {
        "MODEL":res["model"],
        "SERIALNO":res["serialnumber"],
        "EQUIPDEPARTMENT":res["department"],
        "EQUIPDESC":res["equipmentdesc"],
        "EQUIPMANUF":res["manufacturer"],
        "EQUIPLOCATION":res["location"],
        "EQUIPCAT":res["category"]
    }
    print(data)
    return data


# Optional Inputs
def postStandardWO():
    """
    POST request to .../web/base/LOVPOP to get List of Standard WO\n
    LOV_TAGNAME = standardwo
    RETURN WO detail (req)
    """

    global TENANT;HXGN_BASE_URL; USERGROUP

    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
                f"popup=true",
                f"&GRID_NAME=LVSTANDWOREP",
                f"&GRID_TYPE=LOV",
                f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
                f"&LOV_TAGNAME=standardwo",
                f"&usagetype=lov",
                f"&USER_FUNCTION_NAME=WOBFMM",
                f"&CURRENT_TAB_NAME=HDR",
                f"&LOV_ALIAS_NAME_1=control.org",
                f"&LOV_ALIAS_VALUE_1=BRT",
                f"&LOV_ALIAS_TYPE_1=text",
                f"&LOV_ALIAS_NAME_2=param.equipclass",
                f"&LOV_ALIAS_VALUE_2=BUS",
                f"&LOV_ALIAS_TYPE_2=text",
                f"&LOV_ALIAS_NAME_3=param.equipclassorg",
                f"&LOV_ALIAS_VALUE_3=BRT",
                f"&LOV_ALIAS_TYPE_3=text",
                f"&LOV_ALIAS_NAME_4=param.category",
                f"&LOV_ALIAS_VALUE_4=",
                f"&LOV_ALIAS_TYPE_4=text",
                f"&LOV_ALIAS_NAME_5=param.problemcode",
                f"&LOV_ALIAS_VALUE_5=",
                f"&LOV_ALIAS_TYPE_5=text",
                f"&LOV_ALIAS_NAME_6=param.description",
                f"&LOV_ALIAS_VALUE_6=",
                f"&LOV_ALIAS_TYPE_6=text",
                f"&LOV_ALIAS_NAME_7=param.woclass",
                f"&LOV_ALIAS_VALUE_7=",
                f"&LOV_ALIAS_TYPE_7=text",
                f"&LOV_ALIAS_NAME_8=param.woclassorg",
                f"&LOV_ALIAS_VALUE_8=",
                f"&LOV_ALIAS_TYPE_8=text",
                f"&LOV_ALIAS_NAME_9=param.priority",
                f"&LOV_ALIAS_VALUE_9=P3",
                f"&LOV_ALIAS_TYPE_9=select",
                f"&LOV_ALIAS_NAME_10=param.pagemode",
                f"&LOV_ALIAS_VALUE_10=display",
                f"&LOV_ALIAS_TYPE_10=text",
                f"&LOV_ALIAS_NAME_11=param.rjobtype",
                f"&LOV_ALIAS_VALUE_11=",
                f"&LOV_ALIAS_TYPE_11=text",
                f"&LOV_ALIAS_NAME_12=param.group",
                f"&LOV_ALIAS_VALUE_12={USERGROUP}",
                f"&LOV_ALIAS_TYPE_12=text",
                f"&eamid={EAMID}",
                f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    
    return sendRequest('POST', URL, payload)

def postWarrantyClaimReason():
    """
    POST request .../web/base/LOVPOP to get List of Warranty Claim Reasons\n
    LOV_TAGNAME=udfchar01
    optional input
    """

    global TENANT;HXGN_BASE_URL
    
    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
            f"popup=true",
            f"&GRID_NAME=LVUDFCD",
            f"&GRID_TYPE=LOV",
            f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
            f"&LOV_TAGNAME=udfchar01",
            f"&usagetype=lov",
            f"&USER_FUNCTION_NAME=WOBFMM",
            f"&CURRENT_TAB_NAME=HDR",
            f"&LOV_ALIAS_NAME_1=param.rentity",
            f"&LOV_ALIAS_VALUE_1=EVNT",
            f"&LOV_ALIAS_TYPE_1=text",
            f"&LOV_ALIAS_NAME_2=param.field",
            f"&LOV_ALIAS_VALUE_2=udfchar01",
            f"&LOV_ALIAS_TYPE_2=text",
            f"&LOV_ALIAS_NAME_3=param.fieldid",
            f"&LOV_ALIAS_VALUE_3=udfchar01",
            f"&LOV_ALIAS_TYPE_3=text",
            f"&LOV_ALIAS_NAME_4=param.associatedrentity",
            f"&LOV_ALIAS_VALUE_4=EVNT",
            f"&LOV_ALIAS_TYPE_4=text",
            f"&eamid={EAMID}",
            f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    
    return sendRequest('POST', URL, payload)

def postBFMVendor():
    """
    POST request .../web/base/LOVPOP to get List of BFM Vendors\n
    LOV_TAGNAME=udfchar08
    \noptional input
    """
    global TENANT;HXGN_BASE_URL
    
    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
        f"popup=true",
        f"&GRID_NAME=LVUDFCD",
        f"&GRID_TYPE=LOV",
        f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
        f"&LOV_TAGNAME=udfchar08",
        f"&usagetype=lov",
        f"&USER_FUNCTION_NAME=WOBFMM",
        f"&CURRENT_TAB_NAME=HDR",
        f"&LOV_ALIAS_NAME_1=param.rentity",
        f"&LOV_ALIAS_VALUE_1=EVNT",
        f"&LOV_ALIAS_TYPE_1=text",
        f"&LOV_ALIAS_NAME_2=param.field",
        f"&LOV_ALIAS_VALUE_2=udfchar08",
        f"&LOV_ALIAS_TYPE_2=text",
        f"&LOV_ALIAS_NAME_3=param.fieldid",
        f"&LOV_ALIAS_VALUE_3=udfchar08",
        f"&LOV_ALIAS_TYPE_3=text",
        f"&LOV_ALIAS_NAME_4=param.associatedrentity",
        f"&LOV_ALIAS_VALUE_4=EVNT",
        f"&LOV_ALIAS_TYPE_4=text",
        f"&eamid={EAMID}"
    ]
    payload = "".join(payload_list)
    
    return sendRequest('POST', URL, payload)


def postNewWORecord(BUS_NO,DESCRIPTION):
    """
    POST request .../web/base/WSJOBS.HDR?pageaction=SAVE to Create New WO Record\n
    # Equipment No. (req) BUS-8404
    # Service Location (req)
    # Department (req) 
    # Standard WO (opt)
    # Type ()
    # Parent Work Order (opt)
    # Related WO
    # Status (Open, Requires Approval, Work Request)
    # On Hold Reason (AWAITPROJ)
    # Date Reported 07/10/2023 15:31
    # Reported By MELISSALU
    # Assigned By
    # Assigned To
    # Sched. Start Date 07/10/2023
    # Sched. End Date 07/10/2023
    """

    global TENANT; USERID; HXGN_BASE_URL; USERGROUP
    
    OBJ_DATA = postOSOBJ(BUS_NO)
    # 07/19/2023
    SCHEDENDDATE=(datetime.now() + timedelta(days=14)).strftime("%m/%d/%Y")
    SCHEDSTARTDATE = (datetime.now() + timedelta(days=1)).strftime("%m/%d/%Y")
    # 07/10/2023 11:03
    CURRENTDATE=datetime.now().strftime("%m/%d/%Y 00:00")
    DATEREPORTED=datetime.now().strftime("%m/%d/%Y %H:%M")

    EQUIPMANUF=OBJ_DATA['EQUIPMANUF']
    EQUIPDESC=OBJ_DATA['EQUIPDESC']
    EQUIPLOCATION=OBJ_DATA['EQUIPLOCATION']
    EQUIPCAT=OBJ_DATA['EQUIPCAT']
    WORKDAY ='8'
    MODEL=OBJ_DATA['MODEL']
    STANDARDWO=''

    # ------HARDCODED
    #  P3
    PRIORITY='P3'
    # 3 - Medium
    PRIORITY_DISPLAY='3 - Medium'
    LASTMETERREAD=postMTR(BUS_NO)
    SERIALNO=OBJ_DATA['SERIALNO']
    DEPARTMENT=OBJ_DATA['EQUIPDEPARTMENT']
    LOCATIONDESC=f"Bus {BUS_NO}; {EQUIPCAT}"
    SERVICELOCATION='BFM-BAW-STREETSVILLE'
    WOSTATUS='OPN'
    WOSTATUS_DISPLAY=''
    WOTYPE='COR'
    WODISPLAY='Corrective Maintenance'
    WOCLASS='FSMAINT'
    # udfchar1
    VENDORSUPPORT='No'

    URL = f"{HXGN_BASE_URL}/web/base/WSJOBS.HDR?pageaction=SAVE"

    payload={
            "SYSTEM_FUNCTION_NAME":"WSJOBS",
            "USER_FUNCTION_NAME":"WOBFMM",
            "CURRENT_TAB_NAME":"HDR",
            "CHECK_CF_CHANGEFLAG":"true",
            "workday":WORKDAY,
            "stwohasval":"",
            "structurelevel":"",
            "spbtempturnaroundunit":"",
            "sessionid":"",
            "sourcesystem":"",
            "stwoduration":"",
            "tempesthours":"",
            "actfrompoint":"",
            "actestmatlcost":"",
            "acttopointgeoref":"",
            "wohasact":"false",
            "can_delete":"false",
            "suppliercode":"",
            "equipmentsdmflag":"0",
            "acttolongitude":"",
            "actudfchar04":"",
            "actudfchar03":"",
            "actudfchar02":"",
            "completed":"",
            "actudfchar01":"",
            "fromreferencetype":"",
            "spbpermturnaroundunit":"",
            "acttooffsetdirection":"",
            "matlrev":"",
            "gisinstalled":"true",
            "erecordmoduleactivated":"false",
            "personneltype":"",
            "acttoverticaloffset":"",
            "deptsecinstall":"ON",
            "gislayer":"",
            "acttooffset":"",
            "actfromhorizontaloffset":"",
            "woclassorganization":"BRT",
            "acthastransaction":"false",
            "install_gismaps":"",
            "routeparent":"",
            "productionrequestrstatus":"",
            "acttoxcoordinate":"",
            "workorderrtype":"BR",
            "equipmentclassorg":"BRT",
            "planninglevel":"",
            "actfromoffset":"",
            "actsourcecode":"",
            "actestlaborcost":"",
            "actrelatedworkorder":"",
            "equipmentlength":"",
            "orgoption_clgroup":"OFF",
            "pagesource":"",
            "wobillable":"",
            "actrelatedtoreference":"",
            "projhasval":"",
            "replace_mec_eq":"",
            "perioduom":"",
            "routerstatus":"",
            "batchreportsessionid":"",
            "toreferencetype":"",
            "equipmenttype":"S",
            "productionrequestgenerationconfirmation":"",
            "spbtempturnaround":"",
            "routerevision":"",
            "temptrade":"",
            "parentpropertyorg":"",
            "hmsint":"NO",
            "actfromverticaloffsetuom":"",
            "frequency":"",
            "taskdescription":"",
            "equipmentlist":"",
            "can_update":"false",
            "actudfnote02":"",
            "actudfnote01":"",
            "workspacepk":"",
            "activitynote":"",
            "taskrev":"",
            "acttohorizontaloffsettype":"",
            "productionrequeststatus":"",
            "supplierorganization":"",
            "deptsecreadonly":"",
            "meterdue":"",
            "actfromhorizontaloffsettype":"",
            "enhancedplanning":"",
            "meteruom2":"",
            "mapcode":"",
            "childequipmentlist":"",
            "startingat":"",
            "fixed":"V",
            "actfromverticaloffsettype":"",
            "acttopointrefdesc":"",
            "priorityicon":"",
            "actrelatedfromreference":"",
            "hire":"",
            "rtype":"",
            "planlev":"TASK",
            "originalustatus":"",
            "actfromverticaloffset":"",
            "acttoverticaloffsettype":"",
            "eqpusabilityorg":"",
            "eqpusabilitycode":"",
            "autoproductionrequestprompt":"prompt",
            "actfromrelationshiptype":"",
            "enteredby":USERID,
            "schedhrs":"",
            "printmapurl":"",
            "actfromxcoordinate":"",
            "completeaddress":"",
            "acttorelationshiptype":"",
            "roomoccupied":"",
            "viewgispopupdata":"",
            "wostatusentity":"EVST",
            "workordertypecode":"",
            "searchequipmentbylocation":"",
            "acttooffsetpercent":"",
            "temppriority":"",
            "salutationcode":"",
            "tempwoclass":"",
            "acttoverticaloffsetuom":"",
            "can_delete_act":"true",
            "woeqfltorgoption":"YES",
            "completenonevaluatedsurveyequipprompt":"prompt",
            "evtsequence":"",
            "acthaschecklistitemsupdated":"false",
            "pmrvctrl":"",
            "taskuom":"",
            "acttohorizontaloffset":"",
            "actfrompointgeoref":"",
            "maintenancepatternrev":"",
            "confirmchecklist":"",
            "audittablename":"R5EVENTS",
            "cctrspcvalidation":"M",
            "usergroup":USERGROUP,
            "temptaskcode":"",
            "actnote":"YES",
            "workspace_revisionid":"",
            "statusrcode":"R",
            "spbpermturnaround":"",
            "actcpreq":"ON",
            "acttopoint":"",
            "projectrstatus":"",
            "taskqty":"",
            "sourcecode":"",
            "equip_in_mec_wo":"",
            "jtauth_update":"",
            "actfromycoordinate":"",
            "acttohorizontaloffsetuom":"",
            "actfromoffsetpercent":"",
            "equipmentclass":"BUS",
            "pmrevision":"",
            "actudfdate02":"",
            "actudfdate01":"",
            "actudfdate04":"",
            "actudfdate03":"",
            "linearreferenceuom":"",
            "actudfdate05":"",
            "actdept":"",
            "tempworkordertype":"",
            "recordid":"",
            "actudfchkbox01":"0",
            "actduration":"",
            "actudfchkbox04":"0",
            "stwohasact":"",
            "actudfchkbox05":"0",
            "actudfchkbox02":"0",
            "actudfchkbox03":"0",
            "woduration":"1",
            "actudfnum03":"",
            "actudfnum04":"",
            "currentdate":CURRENTDATE,
            "actudfnum05":"",
            "tempstandardwo":"",
            "tempcasetype":"",
            "actudfnum01":"",
            "actfromlongitude":"",
            "actudfnum02":"",
            "maporg":"",
            "actfrompointrefdesc":"",
            "esignaturestring":"",
            "relatedfromreference":"",
            "actudfchar30":"",
            "workspace_accountingentity":"",
            "equipassignedto":"",
            "actudfchar29":"",
            "actudfchar28":"",
            "temppeoplerequired":"",
            "actudfchar27":"",
            "workspace_location":"",
            "directioncode":"",
            "actassignmentstatus":"",
            "schedulingsessiontype":"",
            "vipstatuscode":"",
            "routetemplate":"",
            "actfromlatitude":"",
            "temptaskrevision":"",
            "failuremode":"",
            "gisobjid":"",
            "printsubid":"",
            "relatedtoreference":"",
            "workspace_bodnoun":"",
            "statusicon":"",
            "firstactpertype":"",
            "routedfrom":"",
            "evtisstype":"",
            "has_active_po":"",
            "actfromhorizontaloffsetuom":"",
            "actudfchar15":"",
            "actudfchar14":"",
            "actudfchar13":"",
            "actudfchar12":"",
            "actudfchar11":"",
            "actudfchar10":"",
            "workspace_documentid":"",
            "actsourcesystem":"",
            "is_deferred_act":"",
            "actrecordid":"",
            "actudfchar09":"",
            "actudfchar08":"",
            "actudfchar07":"",
            "actudfchar06":"",
            "actudfchar05":"",
            "routestatus":"",
            "meterdue2":"",
            "campaignorg":"",
            "tempwoclassorg":"",
            "acttolatitude":"",
            "locationorg":"BRT",
            "percentcomplete":"",
            "pmrvctrllist":"",
            "acttotalestcost":"",
            "equipmentcategory":EQUIPCAT,
            "actudfchar26":"",
            "actudfchar25":"",
            "actudfchar24":"",
            "actudfchar23":"",
            "problemcodedesc":"",
            "actudfchar22":"",
            "erecordcode":"",
            "actcsend":"ON",
            "actudfchar21":"",
            "actudfchar20":"",
            "firstactwarranty":"",
            "multiorg":"true",
            "actudfchar19":"",
            "maintenancepatternorg":"",
            "actudfchar18":"",
            "actudfchar17":"",
            "equipsystype":"S",
            "actestmisccost":"",
            "pagemode":"display",
            "actudfchar16":"",
            "actfromoffsetdirection":"",
            "acttoycoordinate":"",
            "can_insert":"true",
            "utilitysystemincident":"0",
            "shift":"",
            "startdate":"",
            "fromverticaloffsettype":"",
            "fromverticaloffsettype_display":"",
            "toycoordinate":"",
            "reliabilityrankingscore":"",
            "inspectiondirection":"",
            "inspectiondirection_display":"",
            "tohorizontaloffsettype":"",
            "tohorizontaloffsettype_display":"",
            "workordernum":"<Auto-Generated>",
            "dependant":"0",
            "estmisccostcurrency":"CAD",
            "relatedfromoffset":"",
            "fromgeoref":"",
            "hipaaconfidentiality":"0",
            "fromoffsetdirection":"",
            "fromoffsetdirection_display":"",
            "datecompleted":"",
            "downtimecostcurr":"CAD",
            "pmcode":"",
            "emailaddress":"",
            "datecreated":"",
            "causecode":"",
            "relatedtooffsetdir":"",
            "relatedtooffsetdir_display":"",
            "productionorder":"",
            "cnnumber":"",
            "datetimecreated":"",
            "servicecategory":"",
            "symptom":"",
            "servicecustomerrequest":"",
            "originatingwoactivity":"",
            "schedenddate":SCHEDENDDATE,
            "productionenddate":"",
            "servicerequeststatus":"",
            "tolongitude":"",
            "equipmentorg":"BRT",
            "activity":"",
            "latitude":"",
            "failuremodedesc":"",
            "preservecalcpriority":"0",
            "casecode":"",
            "tacticalcause":"",
            "reliabilityranking":"",
            "permfixpromisedate":"",
            "vendor":"",
            "equipmenttype_display":"System",
            "multiequip":"0",
            "datereported":DATEREPORTED,
            "esignaturedate":"",
            "schedgroup":"",
            "smda":"0",
            "projbud":"",
            "securityincident":"0",
            "maintenancepattern":"",
            "msproject":"",
            "campaignevent":"",
            "parentpropertydesc":"",
            "originatingcase":"",
            "propertydamage":"0",
            "toverticaloffsetuom":"",
            "toverticaloffsetuom_display":"",
            "targetvalue":"",
            "workspace":"",
            "reopened":"0",
            "toverticaloffsettype":"",
            "toverticaloffsettype_display":"",
            "tohorizontaloffset":"",
            "criticality":"",
            "project":"",
            "workorderstatus":WOSTATUS,
            "workorderstatus_display":WOSTATUS_DISPLAY,
            "humanoversight":"",
            "fromoffsetpercent":"",
            "udfnum09":"",
            "medicalequipmentincident":"0",
            "createdby":USERID,
            "workaddress":"",
            "udfchkbox02":"0",
            "udfnum04":"",
            "torefdesc":"",
            "permitreviewedby":"",
            "udfnum03":"",
            "udfchkbox03":"0",
            "udfnum02":"",
            "udfchkbox01":"0",
            "udfnum01":"",
            "workaccomplished":"",
            "udfnum08":"",
            "udfnum07":"",
            "udfnum06":"",
            "udfnum05":"",
            "udfchkbox08":"0",
            "udfchkbox09":"0",
            "udfchkbox06":"0",
            "udfchkbox07":"0",
            "campaignstatusdesc":"",
            "lockouttagout":"0",
            "udfchkbox04":"0",
            "udfchkbox05":"0",
            "productionrequest":"",
            "fromlongitude":"",
            "calcpriority":"",
            "patientvisitorinjury":"0",
            "tooffsetdirection":"",
            "tooffsetdirection_display":"",
            "topointuom_display":"",
            "equipmentdesc":EQUIPDESC,
            "safetyreviewedby":"",
            "fromxcoordinate":"",
            "campaign":"",
            "actenddate":"",
            "udfchkbox10":"0",
            "togeoref":"",
            "totalestmisccost":"",
            "firstname":"",
            "esigner":"",
            "routestatusdesc":"",
            "description":DESCRIPTION,
            "productionrequestrevision":"",
            "humanfactor":"",
            "preconstructionriskassessment":"0",
            "buildingmaintenanceprogram":"0",
            "matlcode":"",
            "totalestimatedcost":"",
            "managerprofileid":"",
            "toxcoordinate":"",
            "toverticaloffset":"",
            "methodofdetection":"",
            "staffinjuryillness":"0",
            "udfnum10":"",
            "guestprofileid":"",
            "interiminfectioncontrol":"0",
            "middlename":"",
            "reqstartdate":"",
            "downtimecost":"",
            "relatedfromreferencedesc":"",
            "interimlifesafety":"0",
            "duedate":"",
            "reqenddate":"",
            "tolatitude":"",
            "location":EQUIPLOCATION,
            "recallnotice":"0",
            "udfchar45":"",
            "udfchar43":"",
            "udfchar44":"",
            "udfchar41":"",
            "udfchar42":"",
            "statementofconditions":"0",
            "relatedfromoffsetdir":"",
            "relatedfromoffsetdir_display":"",
            "udfchar40":"",
            "salutation_display":"",
            "parentwo":"",
            "serviceproblemcodeorg":"",
            "udfnote02":"",
            "udfnote01":"",
            "safety":"0",
            "componentlocation":"",
            "supplier":"",
            "property":"",
            "tohorizontaloffsetuom":"",
            "tohorizontaloffsetuom_display":"",
            "warranty":"0",
            "model":MODEL,
            "parentproperty":"",
            "flow":"",
            "flow_display":"",
            "fromoffset":"",
            "standardwo":"",
            "totalestmatlcost":"",
            "reliabilityrankingindex":"",
            "hazardousmaterialsincident":"0",
            "priority":PRIORITY,
            "priority_display":PRIORITY_DISPLAY,
            "patientsafety":"0",
            "lastname":"",
            "firesafetyincident":"0",
            "printed":"0",
            "servicerequestid":"",
            "productionstartdate":"",
            "casetype":"",
            "personalprotectiveequipment":"0",
            "accountingentity":"",
            "totalestlaborcost":"",
            "originatingwo":"",
            "udfchar23":"",
            "udfchar24":"",
            "vipstatus_display":"",
            "udfchar21":"",
            "udfchar22":"",
            "udfchar20":"",
            "schedstartdate":SCHEDENDDATE,
            "problemcode":"",
            "phonenumber":"",
            "locationdesc":LOCATIONDESC,
            "actioncode":"",
            "supplierorg":"",
            "reportedby":USERID,
            "customercontract":"",
            "originatingjob":"",
            "manufacturer":"",
            "totalestcostcurrency":"CAD",
            "fromycoordinate":"",
            "confinedspace":"0",
            "fromreferencepoint":"",
            "servicecategoryorg":"",
            "planforimprovement":"0",
            "triggerevent":"",
            "udfchar29":"",
            "udfchar27":"",
            "udfchar28":"",
            "udfchar25":"",
            "estlaborcostcurrency":"CAD",
            "udfchar26":"",
            "udfchar34":"",
            "udfchar35":"",
            "udfchar32":"",
            "udfchar33":"",
            "udfchar30":"",
            "servicecustomerrequestorg":"",
            "udfchar31":"",
            "fromrelationshiptype":"",
            "fromrelationshiptype_display":"",
            "tooffsetpercent":"",
            "lastmeterread":LASTMETERREAD,
            "organization":"BRT",
            "udfchar38":"",
            "udfchar39":"",
            "udfchar36":"",
            "udfchar37":"",
            "udfchar01":"",
            "udfdate04":"",
            "udfchar02":"",
            "udfdate03":"",
            "udfdate06":"",
            "techpartfailure":"",
            "fromhorizontaloffset":"",
            "udfdate05":"",
            "minor":"0",
            "udfdate08":"",
            "remhrs":"",
            "udfdate07":"",
            "meteruom":"KM",
            "esthrs":"",
            "udfdate09":"",
            "aboveceilingpermit":"0",
            "toreferencepoint":"",
            "costcode":"0622",
            "udfdate02":"",
            "syslevel":"",
            "udfdate01":"",
            "schedsessiontypedesc":"",
            "alertcode":"",
            "equipmanufacturer":EQUIPMANUF,
            "estmatlcostcurrency":"CAD",
            "udfchar09":"",
            "udfchar07":"",
            "frompoint":"",
            "actstartdate":"",
            "udfchar08":"",
            "udfchar05":"",
            "udfchar06":"",
            "serviceproblemcode":"",
            "udfchar03":"",
            "udfchar04":"",
            "longitude":"",
            "udfchar12":SERVICELOCATION,
            "udfchar13":"",
            "udfchar10":"",
            "package":"",
            "udfchar11":"",
            "serialnumber":SERIALNO,
            "workordertype":WOTYPE,
            "workordertype_display":WODISPLAY,
            "equipment":f"BUS-{BUS_NO}",
            "torelationshiptype":"",
            "torelationshiptype_display":"",
            "fromhoroffsetuom":"",
            "fromhoroffsetuom_display":"",
            "multipletrades":"0",
            "eqpusabilitydesc":"",
            "routecode":"",
            "task":"",
            "woclass":WOCLASS,
            "tempfixdatecompleted":"",
            "complevel":"",
            "fromrefdesc":"",
            "survey":"0",
            "udfchar18":"",
            "tempfixpromisedate":"",
            "udfchar19":"",
            "udfchar16":VENDORSUPPORT,
            "udfchar17":"",
            "asslevel":"",
            "udfchar14":"",
            "oemsitesystemid":"",
            "udfchar15":"",
            "downtimehours":"",
            "duplicatecase":"",
            "mpsequence":"",
            "fromverticaloffsetuom":"",
            "fromverticaloffsetuom_display":"",
            "rejectreason":"",
            "targetvalcurrency":"CAD",
            "pplreq":"",
            "reasonforrepair":"",
            "hotworkburnpermit":"0",
            "relatedtooffset":"",
            "fromlatitude":"",
            "productionpriority":"",
            "alias":BUS_NO,
            "department":DEPARTMENT,
            "tooffset":"",
            "callername":"",
            "coveragetype":"",
            "coveragetype_display":"",
            "esignaturetype":"",
            "productionprioritydescription":"",
            "fromverticaloffset":"",
            "relatedtoreferencedesc":"",
            "workmanship":"",
            "frompointuom_display":"",
            "udfdate10":"",
            "topoint":"",
            "assignedto":"",
            "fromhoroffsettype":"",
            "fromhoroffsettype_display":"",
            "trade":"",
            "failurecode":"",
            "forprint":"-1",
            "relationshiptype":"",
            "relationshiptype_display":"",
            "categoryname":"",
            "categoryname_display":"",
            "origcasemanagementtask":"",
            "customer":"",
            "frompointuom":"",
            "topointuom":"",
            "temptopoint":"",
            "tempfrompoint":"",
            "PKID":"<Auto-Generated>#BRT#",
            "cust_3_CODE_EVNT_FSCAT":"",
            "cust_3_CODE_EVNT_FSREPAIR":"",
            "PKID":"<Auto-Generated>#BRT#",
            "eamid":None,
            "tenant":TENANT
    }
    
    res = sendRequest('POST', URL, payload)
    print(res)

    if res['pageData']['success'] == True:
        result = res['pageData']['values']['workordernum']
        # print(f"{res['pageData']['messages'][0]['type']}: {res['pageData']['messages'][0]['msg']}")
    else:
        result=None
        # print(f"{res['pageData']['messages'][0]['type']}: {res['pageData']['messages'][0]['msg']}")

    return result


def searchWO( DESCRIPTION):
    """

    """
    URL = f"{HXGN_BASE_URL}/web/base/WSJOBS.xmlhttp"
    payload ={
        "GRID_ID": 100310,
        "GRID_NAME": "WOBFMM",
        "DATASPY_ID": 101634,
        "MADDON_FILTER_ALIAS_NAME_1": "description",
        "MADDON_FILTER_OPERATOR_1": "=",
        "MADDON_FILTER_JOINER_1": "AND",
        "MADDON_FILTER_SEQNUM_1": 1,
        "MADDON_FILTER_VALUE_1": DESCRIPTION,
        "MADDON_LPAREN_1": "false",
        "MADDON_RPAREN_1": "false",
        "MADDON_FILTER_ALIAS_NAME_2": "equipment",
        "MADDON_FILTER_OPERATOR_2": "CONTAINS",
        "MADDON_FILTER_JOINER_2": "AND",
        "MADDON_FILTER_SEQNUM_2": 2,
        "MADDON_FILTER_VALUE_2": "BUS",
        "MADDON_LPAREN_2": "false",
        "MADDON_RPAREN_2": "false",
        "USER_FUNCTION_NAME": "WOBFMM",
        "SYSTEM_FUNCTION_NAME": "WSJOBS",
        "CURRENT_TAB_NAME": "LST",
        "COMPONENT_INFO_TYPE": "DATA_ONLY",
        "eamid": None,
        "tenant": TENANT
    }

    response = sendRequest('POST',URL,payload)
    # print("--->",response['pageData']['grid']['GRIDRESULT']['GRID']['DATA'])


    if response['pageData']['grid']['GRIDRESULT']['GRID']['METADATA']['RECORDS'] =='0':
        return False 
    else:
        WO_NUM=response['pageData']['grid']['GRIDRESULT']['GRID']['DATA'][0]['workordernum']
        # DATE_REPORTED=response['pageData']['grid']['GRIDRESULT']['GRID']['DATA'][0]['datereported']
        return True, WO_NUM


def postCheckLastWOComment(WO_NUM):
    """
    Check if comment exists
    """
    URL=f"{HXGN_BASE_URL}/web/base/WSJOBS.CMT"
    payload= {
        "SYSTEM_FUNCTION_NAME": "WSJOBS",
        "USER_FUNCTION_NAME": "WOBFMM",
        "CURRENT_TAB_NAME": "CMT",
        "workordernum": WO_NUM,
        "organization": "BRT",
        "workorderrtype": "BR",
        "COMMENTCODE": WO_NUM,
        "COMMENTENTITY": "EVNT",
        "COMMENTORGANIZATION": "BRT",
        "bsctype": "*",
        "SCROLLROW": "YES",
        "ONLY_DATA_REQUIRED": "true",
        "eamid": None,
        "tenant": TENANT,
    }

    response = sendRequest('POST', URL, payload)
    # print(response)
    try:
        lastComment = (response['pageData']['commentList'].pop()).get('bsccomment',None)
    except Exception as e:
        lastComment=None
    return lastComment

def postAddWOComments(WO_NUM,COMMENTS):

    """
    POST to .../web/base/WSJOBS.CMT?pageaction=SAV to Add WO Comment
    """
    global TENANT;HXGN_BASE_URL


    URL = f"{HXGN_BASE_URL}/web/base/WSJOBS.CMT?pageaction=SAVE"
    payload= {
                "COMMENTCODE":"",
                "COMMENTENTITY":"EVNT",
                "COMMENTORGANIZATION":"BRT",
                "bsctype":"*",
                "SYSTEM_FUNCTION_NAME":"WSJOBS",
                "USER_FUNCTION_NAME":"WOBFMM",
                "CURRENT_TAB_NAME":"CMT",
                "updatedbyfull":"",
                "equipmentorg":"",
                "bsccreatedby":"",
                "updatedby":"",
                "categorycode":"",
                "defaultlanguage":"EN",
                "bscupdatecount":"",
                "can_select":"true",
                "can_delete":"false",
                "bsccode":WO_NUM,
                "can_update":"true",
                "updatedbydate":"",
                "bsclanguageorig":"",
                "bscline":"",
                "deptsecreadonly":"false",
                "bsccreatedbydate":"",
                "equipment":"",
                "canViewOnly":"false",
                "rentity":"EVNT",
                "organization":"BRT",
                "pagemode":"display",
                "bsccomment":COMMENTS,
                "workorder":"",
                "entity":"EVNT",
                "can_insert":"true",
                "createdbyfull":"",
                "bscprintwdoc":"-1",
                "bsclanguage":"EN",
                "bsclanguage_display":"English",
                "displaycreatedbydate":"",
                "displayupdatedbydate":"",
                "editdeletecontentpermission":"",
                "pageaction":"",
                "entitydescription":"",
                "canLangChange":"",
                "id":"EAM.model.common.Comments-3",
                "eamid":None,
                "tenant":TENANT
            }

    res = sendRequest('POST', URL, payload)
    try:
        value = res['pageData']['commentList'].pop()['bsccomment']
        logging.info(f'Sucessful comment post: {value}')
        return value
    except Exception as e:
        logging.info(f'Post Failed: {e}')
        return False


def addRepairPlan(REPAIRPLAN, TAGS, ALERT_TYPE,SHORT_DESC,LONG_DESC):

    REPAIRPLAN_NO = REPAIRPLAN.get('id',None)
    UPDATED_DATE=REPAIRPLAN.get('updated_on',None)
    CREATED_DATE=REPAIRPLAN.get('created_on',None)
    REPAIR_PLAN_TXT=f"RepairPlan#{REPAIRPLAN_NO}\n{SHORT_DESC};{LONG_DESC}\n{REPAIRPLAN.get('raw_content',"")}"
    BUS_NO=REPAIRPLAN.get('asset_label',None)
   


    # DESCRIPTION=f"Preteckt Repair Plan #{REPAIRPLAN_NO} - Alert Type:{ALERT_TYPE}; TAGS:{TAGS}; Short Description:{SHORT_DESC}; Long Description: {LONG_DESC}"
    DESCRIPTION=f"Preteckt RepairPlan#{REPAIRPLAN_NO}-{TAGS}; {SHORT_DESC}"
    updated=0
    created=0
    update_wo=[]
    created_wo=[]
    woSearch= searchWO(DESCRIPTION)
    if woSearch:
        WO_NUM = woSearch[1]
        # WO_DATE_REPORTED = woSearch[2]
        COMMENTS=f"[UPDATED {UPDATED_DATE}]: #{REPAIRPLAN_NO}\n {REPAIR_PLAN_TXT}"
        if WO_NUM!=None:
            updated+=1
            update_wo.append(WO_NUM)
    else:
        WO_NUM=postNewWORecord(BUS_NO,DESCRIPTION)
        COMMENTS =f"[CREATED {CREATED_DATE}] Repair Plan #{REPAIRPLAN_NO}\n {REPAIR_PLAN_TXT}"
        if WO_NUM!=None:
            created+=1
            created_wo.append(WO_NUM)
    
    # ADD COMMENTS TO EXISITING WO
    lastComment=postCheckLastWOComment(WO_NUM)
    if lastComment != COMMENTS:
        postComment = postAddWOComments(WO_NUM,COMMENTS)
    else:
        print(f'Comment already exists for {WO_NUM} RepairPlan#{REPAIRPLAN_NO}')
    return f'Created {created} WO {created_wo}; Updated {updated} {update_wo}'

# -------
def main(REPAIRPLANS, ALERT_TYPE, TAGS,SHORT_DESC,LONG_DESC):
    # print(REPAIRPLANS)
    TAGS="|".join(TAGS)
    
    # ADD REPAIRPLAN 
    rp = list(map(lambda repairplan: addRepairPlan(repairplan, TAGS,ALERT_TYPE,SHORT_DESC,LONG_DESC),REPAIRPLANS))
    print(rp)


if __name__ == "__main__":
    main()





