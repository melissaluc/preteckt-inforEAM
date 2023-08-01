import preteckt as pt
from urllib.request import urlopen
import pandas as pd
import helpers
import inforEAM
from datetime import datetime, date, timezone
import logging
import numpy as np


logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(pathname)s:%(lineno)d %(funcName)s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.DEBUG,
                    handlers=[logging.FileHandler('repairplan_gen_log.log'),logging.StreamHandler()])



def main():
    alertList = pt.getAlertList(        
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
            q=None,
            )
    # asset_label | repairplans | severity_text | status | source
    alert_df = pd.concat(alertList).drop(columns=['alert_id', 'fleet', 'fleet_name', 'unit_number','asset_id', 'asset_label_slug', 
                                    'asset_type', 'asset_type_display','asset_make', 'asset_model', 'asset_year', 
                                    'asset_group_name','start_date', 'end_date', 'severity_text', 'workflow_state_display',
                                    'source', 'read_by', 'read'])
    # alert_df = pd.concat(alertList).drop(columns=['alert_id', 'fleet', 'fleet_name',"unit_id", 'unit_number','asset_id', 'asset_label_slug', 
    #                                 'asset_type', 'asset_type_display','asset_make', 'asset_model', 'asset_year', 
    #                                 'asset_group_name','start_date', 'end_date', 'severity_text', 'workflow_state_display',
    #                                 'source', 'read_by', 'read',"alert_type","tags","workflow_state","short_desc","long_desc","rtdv_url","rtdv_url"])

    alert_df_filtered = alert_df[alert_df['status'] =='active']

    alert_df_filtered = alert_df_filtered[alert_df_filtered['repairplans'].apply(lambda x: len(x)) > 0]
    alert_df_filtered = alert_df_filtered[alert_df_filtered['reviewed_by'].apply(lambda x: len(x)) > 0]
    alert_df_filtered.sort_values(by=['id','updated_on'] ,ascending=False,inplace=True)

    # alert_df_grouped = alert_df_filtered.groupby(by=["alert_id", "asset_label"]).apply(lambda group: group.reset_index().drop(group.index.to_list()[0:], axis=0) if group.size>1 else None) 
    # alert_df_grouped = alert_df_filtered.groupby(by=["id", "asset_label"]).apply(lambda group: group.reset_index().iloc[0]) 

    return alert_df_filtered

if __name__ == "__main__":
    alert_df=main().head(5)
    print(alert_df)
    print(alert_df.columns)
    alert_df.apply(lambda row: inforEAM.main(row['repairplans'], row['alert_type'], row['tags'],row['short_desc'],row['long_desc']), axis=1)




    





# def main():
#     # unit_number=None
#     # alert_id=None
#     # fleet_id=None
#     # group_id=None
#     # asset_label=None
#     # asset_label_slug=None,
#     # tpms_id=None,
#     # id=None
#     # unit_id=None
#     # asset_label=None,
#     # asset_id=None,
#     # uuid=None,

#     # from_time=None
#     # to_time=datetime.now(timezone.utc)
#     # since=None

#     # spn=None
#     # fmi=None
#     # source=None
#     # alert_type=None
#     # precision=None
#     # sg=None
#     # use_imperial=0
#     # grouped=None
#     # tire=None
#     # fleet=None
#     # action=None
#     # repairplan=None,
#     # manufacturer=None
#     # year=None
#     # series=None
#     # enable_analysis=None
#     # enable_rdtv=None
#     # active=None
#     # enable_reports=None
#     # is_r_and_d=None
#     # limit_fault_code_sources=None
#     # automate_fault_code_repairplans=None
#     # enable_scr_conversion_history=None
#     # enable_dpf_report=None
#     # enable_data_viewer_pre_caching=None
#     # asset_label_slug=None
#     # additional_state=None
#     # type=None
#     # severity=None
#     # tag=None
#     # days=None
#     # q=None

#     # accelMeterList = pt.getAccelerometer(
#     #                 unit_number=unit_number,
#     #                 from_time=from_time,
#     #                 to_time=to_time
#     #                 )
    
#     # gpsList = pt.getGPS(
#     #         unit_number=unit_number,
#     #         from_time=from_time,
#     #         to_time=to_time
#     #         )

#     # chartList = pt.getChartData(
#     #         unit_number=unit_number,
#     #         spn=spn,
#     #         from_time=from_time,
#     #         to_time=to_time,
#     #         alert_type=alert_type
#     #         )

#     # canList = pt.getCAN(
#     #         unit_number=unit_number,
#     #         spn=spn,
#     #         from_time=from_time,
#     #         to_time=to_time,
#     #         precision=precision,
#     #         sg=sg,
#     #         use_imperial=0
#     #         )

#     # spnfmiCodesList = pt.get_SPN_FMI_Codes(       
#     #                     unit_number=unit_number,
#     #                     grouped=grouped,
#     #                     from_time=from_time,
#     #                     to_time=to_time
#     #     )

#     # vSensorList= pt.getVehSensors(
#     #                 unit_number=unit_number
#     #                 )
    
#     # unitsList = pt.getUnitList(
#     #                 unit_number=unit_number,
#     #                 fleet_id=fleet_id,
#     #                 group_id=group_id
#     #             )

#     # tirepHistList = pt.getTirePressHistList(        
#     #         unit_number=unit_number,
#     #         asset_label=asset_label,
#     #         tire=tire
#     #     )

#     # tieHistList = pt.getTireHistList(        
#     #             uuid=uuid,
#     #             fleet=fleet,
#     #             asset_id=asset_id,
#     #             unit_number=unit_number,
#     #             action=action
#     #     )

#     # tireList = pt.getTireList(
#     #             uuid=uuid,
#     #             tpms_id=tpms_id,
#     #             asset_id=asset_id,
#     #             unit_number=unit_number
#     #         )
    
#     # sensorGrpList = pt.getSensorGroupList()

#     # rpCommentList = pt.getRepairPlanCommentList(
#     #                             repairplan=repairplan,
#     #                             unit_number=unit_number,
#     #                             asset_label=asset_label,
#     #                             asset_label_slug=asset_label_slug,
#     #                             since=since
#     #                         )
    
#     # rpList = pt.getRepairPlanList(
#     #                     alert_id=alert_id,
#     #                     unit_number=,
#     #                     asset_label=None,
#     #                     additional_state=None,
#     #                     spn=None,
#     #                     since=None
#     #                 )

#     # fcHistList = pt.getFautCodeHistList(
#     #                         unit_number=None,
#     #                         from_time=None,
#     #                         to_time=None,
#     #                         spn=None,
#     #                         fmi=None,
#     #                         source=None
#     #                 )
    
#     # fcList = pt.getFaultCodeList(
#     #                         spn=None,
#     #                         fmi=None,
#     #                         source=None,
#     #                         manufacturer=None,
#     #                         year=None,
#     #                         series=None
#     #             )

#     # fleetList = pt.getFleetList(
#     #     enable_analysis=None,
#     #     enable_rdtv=None,
#     #     active=None,
#     #     enable_reports=None,
#     #     is_r_and_d=None,
#     #     limit_fault_code_sources=None,
#     #     automate_fault_code_repairplans=None,
#     #     enable_scr_conversion_history=None,
#     #     enable_dpf_report=None,
#     #     enable_data_viewer_pre_caching=None
#     # )

#     # failureTypeList =pt.getFailureTypeList()
#     # pt.getAssetGroupList(id=None)

#     # assetList = pt.getAssetList(    
#     #     id=None,    
#     #     unit_number=None,
#     #     asset_label=None,
#     #     fleet=None,
#     #     group_id=None
#     #     )

#     alertList = pt.getAlertList(        
#         unit_id=None,
#         unit_number=None,
#         asset_label=None,
#         asset_label_slug=None,
#         additional_state=None,
#         type=None,
#         severity=None,
#         tag=None,
#         days=None,
#         since=None,
#         from_date=None,
#         to_date=None,
#         q=None,
#         )



#     return None
