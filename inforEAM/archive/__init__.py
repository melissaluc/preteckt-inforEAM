import requests
from helpers.constants import EAMID, TENANT, USER_FUNCTION_NAME, SYSTEM_FUNCTION_NAME, WINDOW_, USERID, PASSWORD, EWSLANG, ISNAMEDUSER, HXGN_BASE_URL, USERGROUP, CURRENT_DIR
from datetime import datetime
import os
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlencode, quote_plus
import logging 

referer = f'{HXGN_BASE_URL}/web/base/loadmain?SYSTEM_FUNCTION_NAME=WSJOBS&USER_FUNCTION_NAME=WOBFMM&CURRENT_TAB_NAME=&MENU_MODULE_KEY=0&removescreenflows=yes&skipfirstfunccheck=true&isscreencache=true&initpath=WSJOBS&uitheme=theme-ux3&eamid={EAMID}&tenant={TENANT}'



# WO detail (req)
# Equipment No. (req) BUS-8404
# Service Location (req)
# Department (req) 
# Standard WO (opt)
# Type ()
# Class (COR-REPA)
# Priority (1-Urgent, 2-High, 3-Medium, 4-Low, 5-Routine) 
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



def startSession(REQUEST, payload):
    """
    """

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
            eamid = re.search('(?<={"eamid":").*?(?=","external_eamid")', script_tag_str).group(0)
            # print(re.search('gAppData',script_tag_str))
            session_cookies_dict = session.cookies.get_dict()
            session_cookies_dict_new = {f'{key}=': v for key, v in session_cookies_dict.items()}
            session_cookie = ';'.join(key + value for key, value in session_cookies_dict_new.items())

            if REQUEST == 'POST':
                req = session.post(f'{HXGN_BASE_URL}/web/base/dropdown',headers=headers,data=payload, verify=False)
            elif REQUEST == 'GET':
                req = session.get(f'{HXGN_BASE_URL}/web/base/dropdown',headers=headers, verify=False)
            print(req.json())


# DROPDOWN

def postWOType():
    """
    POST request to .../web/base/dropdown get a list of WO Type\n
    TAGNAME = workordertype
    """

    URL = f"{HXGN_BASE_URL}/web/base/dropdown?"

    payload_list = [
        f"_dc={int(datetime.now().timestamp()*(1000))}",
        f"&GRIDNAME=WOBFMM",
        f"&TAGNAME=workordertype",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    return postRequest(URL, payload, referer)


def postWOStatus():
    """
    POST request to .../web/base/dropdown to get a list of WO Status\n
    TAGNAME = workorderstatus
    """

    URL = f"{HXGN_BASE_URL}/web/base/dropdown?"
    payload_list = [
        f"_dc={int(datetime.now().timestamp()*(1000))}",
        f"&GRIDNAME=WOBFMM",
        f"&TAGNAME=workorderstatus",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)

    return postRequest(URL, payload, referer)


# LOVPOP
def postStandardWO():
    """
    POST request to .../web/base/LOVPOP to get List of Standard WO\n
    LOV_TAGNAME = standardwo
    """


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
    
    return postRequest(URL, payload, referer)

def postClasses():
    """
    POST request .../web/base/LOVPOP to get List of Classes\n
    LOV_TAGNAME = woclass
    """

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
    
    return postRequest(URL, payload, referer)

def postPriority():
    """
    POST request .../web/base/LOVPOP to get List of Priority Levels\n
    TAGNAME=priority
    """
   

    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
        f"_dc={int(datetime.now().timestamp()*(1000))}",
        f"&GRIDNAME=WOBFMM",
        f"&TAGNAME=priority",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    
    return postRequest(URL, payload, referer)


def postParentWO():
    """
    POST request .../web/base/LOVPOP to get List of Parent WO\n
    LOV_TAGNAME=parentwo
    """

    
    payload_list = [
            f"popup=true",
            f"&GRID_NAME=LVPARENTWO",
            f"&GRID_TYPE=LOV",
            f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
            f"&LOV_TAGNAME=parentwo",
            f"&usagetype=lov",
            f"&USER_FUNCTION_NAME=WOBFMM",
            f"&CURRENT_TAB_NAME=HDR",
            f"&LOV_ALIAS_NAME_1=control.org",
            f"&LOV_ALIAS_VALUE_1=BRT",
            f"&LOV_ALIAS_TYPE_1=text",
            f"&LOV_ALIAS_NAME_2=param.eventno",
            f"&LOV_ALIAS_VALUE_2=%3CAuto-Generated%3E",
            f"&LOV_ALIAS_TYPE_2=text",
            f"&LOV_ALIAS_NAME_3=parameter.pagemode",
            f"&LOV_ALIAS_VALUE_3=display",
            f"&LOV_ALIAS_TYPE_3=text",
            f"&eamid={EAMID}",
            f"&tenant={TENANT}"
    ]

    payload = "".join(payload_list)
    
    return postRequest(URL, payload, referer)


def postRelatedWO():
    """
    POST request .../web/base/LOVPOP to get List of Related WOs\n
    LOV_TAGNAME=udfchar07
    """

    URL = f"{HXGN_BASE_URL}/web/base/LOVPOP"
    payload_list = [
        f"popup=true",
        f"&GRID_NAME=LVUDFE",
        f"&GRID_TYPE=LOV",
        f"&REQUEST_TYPE=LOV.HEAD_DATA.STORED",
        f"&LOV_TAGNAME=udfchar07",
        f"&usagetype=lov",
        f"&USER_FUNCTION_NAME=WOBFMM",
        f"&CURRENT_TAB_NAME=HDR",
        f"&LOV_ALIAS_NAME_1=param.rentity",
        f"&LOV_ALIAS_VALUE_1=EVNT",
        f"&LOV_ALIAS_TYPE_1=text",
        f"&LOV_ALIAS_NAME_2=param.field",
        f"&LOV_ALIAS_VALUE_2=udfchar07",
        f"&LOV_ALIAS_TYPE_2=text",
        f"&LOV_ALIAS_NAME_3=param.fieldid",
        f"&LOV_ALIAS_VALUE_3=udfchar07",
        f"&LOV_ALIAS_TYPE_3=text",
        f"&LOV_ALIAS_NAME_4=param.associatedrentity",
        f"&LOV_ALIAS_VALUE_4=EVNT",
        f"&LOV_ALIAS_TYPE_4=text",
        f"&LOV_ALIAS_NAME_5=param.lookuprentity",
        f"&LOV_ALIAS_VALUE_5=EVNT",
        f"&LOV_ALIAS_TYPE_5=text",
        f"&LOV_ALIAS_NAME_6=control.org",
        f"&LOV_ALIAS_VALUE_6=BRT",
        f"&LOV_ALIAS_TYPE_6=text",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)
    
    return postRequest(URL, payload, referer)

def postOnHoldReason():
    """
    POST request .../web/base/LOVPOP to get List of On Hold Reasons\n
    &LOV_TAGNAME=udfchar01
    """
   
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
    
    return postRequest(URL, payload, referer)

def postWarrantyClaimReason():
    """
    POST request .../web/base/LOVPOP to get List of Warranty Claim Reasons\n
    LOV_TAGNAME=udfchar01
    """

    
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
    
    return postRequest(URL, payload, referer)

def postBFMVendor():
    """
    POST request .../web/base/LOVPOP to get List of BFM Vendors\n
    LOV_TAGNAME=udfchar08
    \noptional input
    """
    
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
    
    return postRequest(URL, payload, referer)


def postNewWORecord():
    """
    POST request .../web/base/WSJOBS.HDR?pageaction=SAVE to Create New WO Record\n
    """
    BUS_NO=4000
    SCHEDENDDATE="06%2F30%2F2023"
    CURRENTDATE="06%2F30%2F2023%2000%3A00"
    DATEREPORTED="06%2F30%2F2023%2014%3A10"
    EQUIPMANUF='ADL'
    EQUIPDESC={SuperLo%20Enviro%20500%3B%20DDS-Electric%3B%204000}
    WORKDAY =8
    URL = f"{HXGN_BASE_URL}/web/base/WSJOBS.HDR?pageaction=SAVE"
    payload_list = [
                        f"SYSTEM_FUNCTION_NAME=WSJOBS",
                        f"&USER_FUNCTION_NAME=WOBFMM",
                        f"&CURRENT_TAB_NAME=HDR",
                        f"&CHECK_CF_CHANGEFLAG=true",
                        f"&workday={WORKDAY}",
                        f"&stwohasval=",
                        f"&structurelevel=",
                        f"&spbtempturnaroundunit=",
                        f"&sessionid=",
                        f"&sourcesystem=",
                        f"&stwoduration=1",
                        f"&tempesthours=",
                        f"&actfrompoint=",
                        f"&actestmatlcost=",
                        f"&acttopointgeoref=",
                        f"&wohasact=false",
                        f"&can_delete=false",
                        f"&suppliercode=",
                        f"&equipmentsdmflag=0",
                        f"&acttolongitude=",
                        f"&actudfchar04=",
                        f"&actudfchar03=",
                        f"&actudfchar02=",
                        f"&completed=",
                        f"&actudfchar01=",
                        f"&fromreferencetype=",
                        f"&spbpermturnaroundunit=",
                        f"&acttooffsetdirection=",
                        f"&matlrev=",
                        f"&gisinstalled=true",
                        f"&erecordmoduleactivated=false",
                        f"&personneltype=",
                        f"&acttoverticaloffset=",
                        f"&deptsecinstall=ON",
                        f"&gislayer=",
                        f"&acttooffset=",
                        f"&actfromhorizontaloffset=",
                        f"&woclassorganization=BRT",
                        f"&acthastransaction=",
                        f"&install_gismaps=",
                        f"&routeparent=",
                        f"&productionrequestrstatus=",
                        f"&acttoxcoordinate=",
                        f"&workorderrtype=BR",
                        f"&equipmentclassorg=BRT",
                        f"&planninglevel=",
                        f"&actfromoffset=",
                        f"&actsourcecode=",
                        f"&actestlaborcost=",
                        f"&actrelatedworkorder=",
                        f"&equipmentlength=",
                        f"&orgoption_clgroup=OFF",
                        f"&pagesource=",
                        f"&wobillable=",
                        f"&actrelatedtoreference=",
                        f"&projhasval=",
                        f"&replace_mec_eq=",
                        f"&perioduom=",
                        f"&routerstatus=",
                        f"&batchreportsessionid=",
                        f"&storeferencetype=",
                        f"&equipmenttype=S",
                        f"&productionrequestgenerationconfirmation=",
                        f"&spbtempturnaround=",
                        f"&routerevision=",
                        f"&temptrade=",
                        f"&parentpropertyorg=",
                        f"&hmsint=NO",
                        f"&actfromverticaloffsetuom=",
                        f"&frequency=",
                        f"&taskdescription=",
                        f"&equipmentlist=",
                        f"&can_update=false",
                        f"&actudfnote02=",
                        f"&actudfnote01=",
                        f"&workspacepk=",
                        f"&activitynote=",
                        f"&taskrev=",
                        f"&acttohorizontaloffsettype=",
                        f"&productionrequeststatus=",
                        f"&supplierorganization=",
                        f"&deptsecreadonly=",
                        f"&meterdue=",
                        f"&actfromhorizontaloffsettype=",
                        f"&enhancedplanning=",
                        f"&meteruom2=",
                        f"&mapcode=",
                        f"&childequipmentlist=",
                        f"&startingat=",
                        f"&fixed=V",
                        f"&actfromverticaloffsettype=",
                        f"&acttopointrefdesc=",
                        f"&priorityicon=",
                        f"&actrelatedfromreference=",
                        f"&hire=",
                        f"&rtype=",
                        f"&planlev=TASK",
                        f"&originalustatus=",
                        f"&actfromverticaloffset=",
                        f"&acttoverticaloffsettype=",
                        f"&eqpusabilityorg=",
                        f"&eqpusabilitycode=",
                        f"&autoproductionrequestprompt=prompt",
                        f"&actfromrelationshiptype=",
                        f"&enteredby={USERID}",
                        f"&schedhrs=",
                        f"&printmapurl=",
                        f"&actfromxcoordinate=",
                        f"&completeaddress=",
                        f"&acttorelationshiptype=",
                        f"&roomoccupied=",
                        f"&viewgispopupdata=",
                        f"&wostatusentity=EVST",
                        f"&workordertypecode=",
                        f"&searchequipmentbylocation=",
                        f"&acttooffsetpercent=",
                        f"&temppriority=",
                        f"&salutationcode=",
                        f"&tempwoclass=",
                        f"&acttoverticaloffsetuom=",
                        f"&can_delete_act=true",
                        f"&woeqfltorgoption=YES",
                        f"&completenonevaluatedsurveyequipprompt=prompt",
                        f"&evtsequence=",
                        f"&acthaschecklistitemsupdated=",
                        f"&pmrvctrl=",
                        f"&taskuom=",
                        f"&acttohorizontaloffset=",
                        f"&actfrompointgeoref=",
                        f"&maintenancepatternrev=",
                        f"&confirmchecklist=",
                        f"&audittablename=R5EVENTS",
                        f"&cctrspcvalidation=M",
                        f"&usergroup={USERGROUP}",
                        f"&temptaskcode=",
                        f"&actnote=YES",
                        f"&workspace_revisionid=",
                        f"&statusrcode=R",
                        f"&spbpermturnaround=",
                        f"&actcpreq=ON",
                        f"&acttopoint=",
                        f"&projectrstatus=",
                        f"&taskqty=",
                        f"&sourcecode=",
                        f"&equip_in_mec_wo=",
                        f"&jtauth_update=",
                        f"&actfromycoordinate=",
                        f"&acttohorizontaloffsetuom=",
                        f"&actfromoffsetpercent=",
                        f"&equipmentclass=BUS",
                        f"&pmrevision=",
                        f"&actudfdate02=",
                        f"&actudfdate01=",
                        f"&actudfdate04=",
                        f"&actudfdate03=",
                        f"&linearreferenceuom=",
                        f"&actudfdate05=",
                        f"&actdept=",
                        f"&tempworkordertype=",
                        f"&recordid=",
                        f"&actudfchkbox01=0",
                        f"&actduration=",
                        f"&actudfchkbox04=0",
                        f"&stwohasact=true",
                        f"&actudfchkbox05=0",
                        f"&actudfchkbox02=0",
                        f"&actudfchkbox03=0",
                        f"&woduration=1",
                        f"&actudfnum03=",
                        f"&actudfnum04=",
                        f"&currentdate={CURRENT_DATE}",
                        f"&actudfnum05=",
                        f"&tempstandardwo=",
                        f"&tempcasetype=",
                        f"&actudfnum01=",
                        f"&actfromlongitude=",
                        f"&actudfnum02=",
                        f"&maporg=",
                        f"&actfrompointrefdesc=",
                        f"&esignaturestring=",
                        f"&relatedfromreference=",
                        f"&actudfchar30=",
                        f"&workspace_accountingentity=",
                        f"&equipassignedto=",
                        f"&actudfchar29=",
                        f"&actudfchar28=",
                        f"&temppeoplerequired=",
                        f"&actudfchar27=",
                        f"&workspace_location=",
                        f"&directioncode=",
                        f"&actassignmentstatus=",
                        f"&schedulingsessiontype=",
                        f"&vipstatuscode=",
                        f"&routetemplate=",
                        f"&actfromlatitude=",
                        f"&temptaskrevision=",
                        f"&failuremode=",
                        f"&gisobjid=",
                        f"&printsubid=",
                        f"&relatedtoreference=",
                        f"&workspace_bodnoun=",
                        f"&statusicon=",
                        f"&firstactpertype=",
                        f"&routedfrom=",
                        f"&evtisstype=",
                        f"&has_active_po=",
                        f"&actfromhorizontaloffsetuom=",
                        f"&actudfchar15=",
                        f"&actudfchar14=",
                        f"&actudfchar13=",
                        f"&actudfchar12=",
                        f"&actudfchar11=",
                        f"&actudfchar10=",
                        f"&workspace_documentid=",
                        f"&actsourcesystem=",
                        f"&is_deferred_act=",
                        f"&actrecordid=",
                        f"&actudfchar09=",
                        f"&actudfchar08=",
                        f"&actudfchar07=",
                        f"&actudfchar06=",
                        f"&actudfchar05=",
                        f"&routestatus=",
                        f"&meterdue2=",
                        f"&campaignorg=",
                        f"&tempwoclassorg=",
                        f"&acttolatitude=",
                        f"&locationorg=BRT",
                        f"&percentcomplete=",
                        f"&pmrvctrllist=",
                        f"&acttotalestcost=",
                        f"&equipmentcategory=",
                        f"&actudfchar26=",
                        f"&actudfchar25=",
                        f"&actudfchar24=",
                        f"&actudfchar23=",
                        f"&problemcodedesc=",
                        f"&actudfchar22=",
                        f"&erecordcode=",
                        f"&actcsend=ON",
                        f"&actudfchar21=",
                        f"&actudfchar20=",
                        f"&firstactwarranty=",
                        f"&multiorg=true",
                        f"&actudfchar19=",
                        f"&maintenancepatternorg=",
                        f"&actudfchar18=",
                        f"&actudfchar17=",
                        f"&equipsystype=S",
                        f"&actestmisccost=",
                        f"&pagemode=display",
                        f"&actudfchar16=",
                        f"&actfromoffsetdirection=",
                        f"&acttoycoordinate=",
                        f"&can_insert=true",
                        f"&utilitysystemincident=0",
                        f"&shift=",
                        f"&startdate=",
                        f"&fromverticaloffsettype=",
                        f"&fromverticaloffsettype_display=",
                        f"&toycoordinate=",
                        f"&reliabilityrankingscore=",
                        f"&inspectiondirection=",
                        f"&inspectiondirection_display=",
                        f"&tohorizontaloffsettype=",
                        f"&tohorizontaloffsettype_display=",
                        f"&workordernum=<Auto-Generated>",
                        f"&dependant=-1",
                        f"&estmisccostcurrency=CAD",
                        f"&relatedfromoffset=",
                        f"&fromgeoref=",
                        f"&hipaaconfidentiality=0",
                        f"&fromoffsetdirection=",
                        f"&fromoffsetdirection_display=",
                        f"&datecompleted=",
                        f"&downtimecostcurr=CAD",
                        f"&pmcode=",
                        f"&emailaddress=",
                        f"&datecreated=",
                        f"&causecode=",
                        f"&relatedtooffsetdir=",
                        f"&relatedtooffsetdir_display=",
                        f"&productionorder=",
                        f"&cnnumber=",
                        f"&datetimecreated=",
                        f"&servicecategory=",
                        f"&symptom=",
                        f"&servicecustomerrequest=",
                        f"&originatingwoactivity=",
                        f"&schedenddate={SCHEDENDDATE}",
                        f"&productionenddate=",
                        f"&servicerequeststatus=",
                        f"&tolongitude=",
                        f"&equipmentorg=BRT",
                        f"&activity=",
                        f"&latitude=",
                        f"&failuremodedesc=",
                        f"&preservecalcpriority=0",
                        f"&casecode=",
                        f"&tacticalcause=",
                        f"&reliabilityranking=",
                        f"&permfixpromisedate=",
                        f"&vendor=",
                        f"&equipmenttype_display=System",
                        f"&multiequip=0",
                        f"&datereported={datereported}",
                        f"&esignaturedate=",
                        f"&schedgroup=",
                        f"&smda=0",
                        f"&projbud=",
                        f"&securityincident=0",
                        f"&maintenancepattern=",
                        f"&msproject=",
                        f"&campaignevent=",
                        f"&parentpropertydesc=",
                        f"&originatingcase=",
                        f"&propertydamage=0",
                        f"&toverticaloffsetuom=",
                        f"&toverticaloffsetuom_display=",
                        f"&targetvalue=",
                        f"&workspace=",
                        f"&reopened=0",
                        f"&toverticaloffsettype=",
                        f"&toverticaloffsettype_display=",
                        f"&tohorizontaloffset=",
                        f"&criticality=",
                        f"&project=",
                        f"&workorderstatus=OPN",
                        f"&workorderstatus_display=",
                        f"&humanoversight=",
                        f"&fromoffsetpercent=",
                        f"&udfnum09=",
                        f"&medicalequipmentincident=0",
                        f"&createdby={USERID}",
                        f"&workaddress=",
                        f"&udfchkbox02=0",
                        f"&udfnum04=",
                        f"&torefdesc=",
                        f"&permitreviewedby=",
                        f"&udfnum03=",
                        f"&udfchkbox03=0",
                        f"&udfnum02=",
                        f"&udfchkbox01=0",
                        f"&udfnum01=",
                        f"&workaccomplished=",
                        f"&udfnum08=",
                        f"&udfnum07=",
                        f"&udfnum06=",
                        f"&udfnum05=",
                        f"&udfchkbox08=0",
                        f"&udfchkbox09=0",
                        f"&udfchkbox06=0",
                        f"&udfchkbox07=0",
                        f"&campaignstatusdesc=",
                        f"&lockouttagout=0",
                        f"&udfchkbox04=0",
                        f"&udfchkbox05=0",
                        f"&productionrequest=",
                        f"&fromlongitude=",
                        f"&calcpriority=",
                        f"&patientvisitorinjury=0",
                        f"&tooffsetdirection=",
                        f"&tooffsetdirection_display=",
                        f"&topointuom_display=",
                        f"&equipmentdesc={equipmentdesc}",
                        f"&safetyreviewedby=",
                        f"&fromxcoordinate=",
                        f"&campaign=",
                        f"&actenddate=",
                        f"&udfchkbox10=0",
                        f"&togeoref=",
                        f"&totalestmisccost=",
                        f"&firstname=",
                        f"&esigner=",
                        f"&routestatusdesc=",
                        f"&description={description}",
                        f"&productionrequestrevision=",
                        f"&humanfactor=",
                        f"&preconstructionriskassessment=0",
                        f"&buildingmaintenanceprogram=0",
                        f"&matlcode=",
                        f"&totalestimatedcost=",
                        f"&managerprofileid=",
                        f"&toxcoordinate=",
                        f"&toverticaloffset=",
                        f"&methodofdetection=",
                        f"&staffinjuryillness=0",
                        f"&udfnum10=",
                        f"&guestprofileid=",
                        f"&interiminfectioncontrol=0",
                        f"&middlename=",
                        f"&reqstartdate=",
                        f"&downtimecost=",
                        f"&relatedfromreferencedesc=",
                        f"&interimlifesafety=0",
                        f"&duedate=",
                        f"&reqenddate=",
                        f"&tolatitude=",
                        f"&location=L-BUS-{4000}",
                        f"&recallnotice=0",
                        f"&udfchar45=",
                        f"&udfchar43=",
                        f"&udfchar44=",
                        f"&udfchar41=",
                        f"&udfchar42=",
                        f"&statementofconditions=0",
                        f"&relatedfromoffsetdir=",
                        f"&relatedfromoffsetdir_display=",
                        f"&udfchar40=",
                        f"&salutation_display=",
                        f"&parentwo=",
                        f"&serviceproblemcodeorg=",
                        f"&udfnote02=",
                        f"&udfnote01=",
                        f"&safety=0",
                        f"&componentlocation=",
                        f"&supplier=",
                        f"&property=",
                        f"&tohorizontaloffsetuom=",
                        f"&tohorizontaloffsetuom_display=",
                        f"&warranty=-1",
                        f"&model={SuperLo%20Enviro%20500}",
                        f"&parentproperty=",
                        f"&flow=",
                        f"&flow_display=",
                        f"&fromoffset=",
                        f"&standardwo={standardwo}",
                        f"&totalestmatlcost=",
                        f"&reliabilityrankingindex=",
                        f"&hazardousmaterialsincident=0",
                        f"&priority={priority}",
                        f"&priority_display={priority_display}",
                        f"&patientsafety=0",
                        f"&lastname=",
                        f"&firesafetyincident=0",
                        f"&printed=0",
                        f"&servicerequestid=",
                        f"&productionstartdate=",
                        f"&casetype=",
                        f"&personalprotectiveequipment=0",
                        f"&accountingentity=",
                        f"&totalestlaborcost=",
                        f"&originatingwo=",
                        f"&udfchar23=",
                        f"&udfchar24=",
                        f"&vipstatus_display=",
                        f"&udfchar21=",
                        f"&udfchar22=",
                        f"&udfchar20=",
                        f"&schedstartdate={SCHEDSTARTDATE}",
                        f"&problemcode=",
                        f"&phonenumber=",
                        f"&locationdesc={Bus%204000%3B%20DDS-Electric}",
                        f"&actioncode=",
                        f"&supplierorg=",
                        f"&reportedby={USERID}",
                        f"&customercontract=",
                        f"&originatingjob=",
                        f"&manufacturer=",
                        f"&totalestcostcurrency=CAD",
                        f"&fromycoordinate=",
                        f"&confinedspace=0",
                        f"&fromreferencepoint=",
                        f"&servicecategoryorg=",
                        f"&planforimprovement=0",
                        f"&triggerevent=",
                        f"&udfchar29=",
                        f"&udfchar27=",
                        f"&udfchar28=",
                        f"&udfchar25=",
                        f"&estlaborcostcurrency=CAD",
                        f"&udfchar26=",
                        f"&udfchar34=",
                        f"&udfchar35=",
                        f"&udfchar32=",
                        f"&udfchar33=",
                        f"&udfchar30=",
                        f"&servicecustomerrequestorg=",
                        f"&udfchar31=",
                        f"&fromrelationshiptype=",
                        f"&fromrelationshiptype_display=",
                        f"&tooffsetpercent=",
                        f"&lastmeterread={4137}",
                        f"&organization=BRT",
                        f"&udfchar38=",
                        f"&udfchar39=",
                        f"&udfchar36=",
                        f"&udfchar37=",
                        f"&udfchar01={AWAITPROJ}",
                        f"&udfdate04=",
                        f"&udfchar02=",
                        f"&udfdate03={06%2F28%2F2023%2000%3A00}",
                        f"&udfdate06=",
                        f"&techpartfailure=",
                        f"&fromhorizontaloffset=",
                        f"&udfdate05={06%2F30%2F2023%2000%3A00}",
                        f"&minor=0",
                        f"&udfdate08=",
                        f"&remhrs=",
                        f"&udfdate07=",
                        f"&meteruom=KM",
                        f"&esthrs=",
                        f"&udfdate09=",
                        f"&aboveceilingpermit=0",
                        f"&toreferencepoint=",
                        f"&costcode={COSTCODE}",
                        f"&udfdate02=",
                        f"&syslevel=",
                        f"&udfdate01=",
                        f"&schedsessiontypedesc=",
                        f"&alertcode=",
                        f"&equipmanufacturer={equipmanufacturer}",
                        f"&estmatlcostcurrency=CAD",
                        f"&udfchar09={testing}",
                        f"&udfchar07=",
                        f"&frompoint=",
                        f"&actstartdate=",
                        f"&udfchar08={ADL}",
                        f"&udfchar05=",
                        f"&udfchar06=",
                        f"&serviceproblemcode=",
                        f"&udfchar03=",
                        f"&udfchar04=",
                        f"&longitude=",
                        f"&udfchar12={SERVICELOC}",
                        f"&udfchar13=",
                        f"&udfchar10=MX",
                        f"&package=",
                        f"&udfchar11=",
                        f"&serialnumber={SERIALNO}",
                        f"&workordertype={WO_TYPE_SHORT}",
                        f"&workordertype_display={WO_TYPE_LONG}",
                        f"&equipment=BUS-{BUS_NO}",
                        f"&torelationshiptype=",
                        f"&torelationshiptype_display=",
                        f"&fromhoroffsetuom=",
                        f"&fromhoroffsetuom_display=",
                        f"&multipletrades=0",
                        f"&eqpusabilitydesc=",
                        f"&routecode=",
                        f"&task=",
                        f"&woclass={WO_CLASS}",
                        f"&tempfixdatecompleted=",
                        f"&complevel=",
                        f"&fromrefdesc=",
                        f"&survey=0",
                        f"&udfchar18=",
                        f"&tempfixpromisedate=",
                        f"&udfchar19=",
                        f"&udfchar16=No",
                        f"&udfchar17=",
                        f"&asslevel=",
                        f"&udfchar14=",
                        f"&oemsitesystemid=",
                        f"&udfchar15=No",
                        f"&downtimehours=",
                        f"&duplicatecase=",
                        f"&mpsequence=",
                        f"&fromverticaloffsetuom=",
                        f"&fromverticaloffsetuom_display=",
                        f"&rejectreason=",
                        f"&targetvalcurrency=CAD",
                        f"&pplreq=",
                        f"&reasonforrepair=",
                        f"&hotworkburnpermit=0",
                        f"&relatedtooffset=",
                        f"&fromlatitude=",
                        f"&productionpriority=",
                        f"&alias={BUS_NO}",
                        f"&department={BUS_DEPT}",
                        f"&tooffset=",
                        f"&callername=",
                        f"&coveragetype=",
                        f"&coveragetype_display=",
                        f"&esignaturetype=",
                        f"&productionprioritydescription=",
                        f"&fromverticaloffset=",
                        f"&relatedtoreferencedesc=",
                        f"&workmanship=",
                        f"&frompointuom_display=",
                        f"&udfdate10=",
                        f"&topoint=",
                        f"&assignedto=",
                        f"&fromhoroffsettype=",
                        f"&fromhoroffsettype_display=",
                        f"&trade=",
                        f"&failurecode=",
                        f"&forprint=-1",
                        f"&relationshiptype=",
                        f"&relationshiptype_display=",
                        f"&categoryname=",
                        f"&categoryname_display=",
                        f"&origcasemanagementtask=",
                        f"&customer=",
                        f"&frompointuom=",
                        f"&topointuom=",
                        f"&temptopoint=",
                        f"&tempfrompoint=",
                        f"&PKID=<Auto-Generated>#BRT#",
                        f"&eamid={EAMID}",
                        f"&tenant={TENANT}"
    ]
    payload = "".join(payload_list)

    
    return postRequest(URL, payload, referer)



def postAddWOComments(REPAIRPLAN):

    """
    POST to .../web/base/WSJOBS.CMT?pageaction=SAV to Add WO Comment
    """
    BSCCODE=2355446
    REPAIRPLAN=""
    URL = f"{HXGN_BASE_URL}/web/base/WSJOBS.CMT?pageaction=SAV"
    payload_list = [
    
    f"COMMENTCODE=",
    f"&COMMENTENTITY=EVNT",
    f"&COMMENTORGANIZATION=BRT",
    f"&bsctype=*",
    f"&SYSTEM_FUNCTION_NAME=WSJOBS",
    f"&USER_FUNCTION_NAME=WOBFMM",
    f"&CURRENT_TAB_NAME=CMT",
    f"&updatedbyfull=",
    f"&equipmentorg=",
    f"&bsccreatedby=",
    f"&updatedby=",
    f"&categorycode=",
    f"&defaultlanguage=EN",
    f"&bscupdatecount=",
    f"&can_select=true",
    f"&can_delete=false",
    f"&bsccode={BSCCODE}",
    f"&can_update=true",
    f"&updatedbydate=",
    f"&bsclanguageorig=",
    f"&bscline=",
    f"&deptsecreadonly=false",
    f"&bsccreatedbydate=",
    f"&equipment=",
    f"&canViewOnly=false",
    f"&rentity=EVNT",
    f"&organization=BRT",
    f"&pagemode=display",
    f"&bsccomment={REPAIRPLAN}",
    f"&workorder=",
    f"&entity=EVNT",
    f"&can_insert=true",
    f"&createdbyfull=",
    f"&bscprintwdoc=-1",
    f"&bsclanguage=EN",
    f"&bsclanguage_display=English",
    f"&displaycreatedbydate=",
    f"&displayupdatedbydate=",
    f"&editdeletecontentpermission=",
    f"&pageaction=",
    f"&entitydescription=",
    f"&canLangChange=",
    f"&id=EAM.model.common.Comments-6",
    f"&eamid={EAMID}",
    f"&tenant={TENANT}"
    ]


    return

# Check if WO exists by repair plan id

# Get last meter reading
def postMTR(BUS_NO):
    """
    POST to .../web/base/OSOBJS.MTR' to get equipment meter readings
    Return lastmeter reading
    """
    URL = f'{HXGN_BASE_URL}/web/base/OSOBJS.MTR'
    payload = [
    f"SYSTEM_FUNCTION_NAME=OSOBJS",
    f"&USER_FUNCTION_NAME=R2OBJS",
    f"&CURRENT_TAB_NAME=MTR",
    f"&equipmentno=BUS-{BUS_NO}",
    f"&organization=BRT",
    f"&statusrcode=I",
    f"&eamid={EAMID}",
    f"&tenant={TENANT}"
    ]


def postOSOBJ(BUS_NO):
    """
    POST to .../web/base/OSOBJS.xmlhttp to get Equiment Details
    """

    URL = f'{HXGN_BASE_URL}/web/base/OSOBJS.xmlhttp'
    payload = [
        f"GRID_ID=100152",
        f"&GRID_NAME=R2OBJS",
        f"&DATASPY_ID=101098",
        f"&MADDON_FILTER_ALIAS_NAME_1=location",
        f"&MADDON_FILTER_OPERATOR_1=%3D",
        f"&MADDON_FILTER_JOINER_1=AND",
        f"&MADDON_FILTER_SEQNUM_1=1",
        f"&MADDON_FILTER_VALUE_1=L-BUS-{BUS_NO}",
        f"&MADDON_LPAREN_1=false",
        f"&MADDON_RPAREN_1=false",
        f"&MADDON_FILTER_ALIAS_NAME_2=class",
        f"&MADDON_FILTER_OPERATOR_2=%3D",
        f"&MADDON_FILTER_JOINER_2=AND",
        f"&MADDON_FILTER_SEQNUM_2=2",
        f"&MADDON_FILTER_VALUE_2=BUS",
        f"&MADDON_LPAREN_2=false",
        f"&MADDON_RPAREN_2=false",
        f"&MADDON_FILTER_ALIAS_NAME_3=operationalstatus",
        f"&MADDON_FILTER_OPERATOR_3=IN",
        f"&MADDON_FILTER_JOINER_3=AND",
        f"&MADDON_FILTER_SEQNUM_3=3",
        f"&MADDON_FILTER_VALUE_3='INSV'%2C'NOSV'",
        f"&MADDON_LPAREN_3=false",
        f"&MADDON_RPAREN_3=false",
        f"&USER_FUNCTION_NAME=R2OBJS",
        f"&SYSTEM_FUNCTION_NAME=OSOBJS",
        f"&CURRENT_TAB_NAME=LST",
        f"&COMPONENT_INFO_TYPE=DATA_ONLY",
        f"&eamid={EAMID}",
        f"&tenant={TENANT}"
    ]