"""
helper module to get all the AIS pyaisnmea.messages together in one module
"""

# pylint: disable=no-member
# pylint: disable=import-error
# pylint: disable=no-name-in-module

import pyaisnmea.messages
import pyaisnmea.messages.aismessage
import pyaisnmea.messages.t123
import pyaisnmea.messages.t4
import pyaisnmea.messages.t5
import pyaisnmea.messages.t6
import pyaisnmea.messages.t7
import pyaisnmea.messages.t8
import pyaisnmea.messages.t9
import pyaisnmea.messages.t10
import pyaisnmea.messages.t11
import pyaisnmea.messages.t12
import pyaisnmea.messages.t13
import pyaisnmea.messages.t14
import pyaisnmea.messages.t15
import pyaisnmea.messages.t16
import pyaisnmea.messages.t17
import pyaisnmea.messages.t18
import pyaisnmea.messages.t19
import pyaisnmea.messages.t20
import pyaisnmea.messages.t21
import pyaisnmea.messages.t22
import pyaisnmea.messages.t23
import pyaisnmea.messages.t24
import pyaisnmea.messages.t25
import pyaisnmea.messages.t26
import pyaisnmea.messages.t27

MSGDESCRIPTIONS = pyaisnmea.messages.aismessage.MSGDESCRIPTIONS

MSGTYPES = {
    0: pyaisnmea.messages.aismessage.AISMessage,
    1: pyaisnmea.messages.t123.Type123PositionReportClassA,
    2: pyaisnmea.messages.t123.Type123PositionReportClassA,
    3: pyaisnmea.messages.t123.Type123PositionReportClassA,
    4: pyaisnmea.messages.t4.Type4BaseStationReport,
    5: pyaisnmea.messages.t5.Type5StaticAndVoyageData,
    6: pyaisnmea.messages.t6.Type6BinaryMessage,
    7: pyaisnmea.messages.t7.Type7BinaryAcknowlegement,
    8: pyaisnmea.messages.t8.Type8BinaryBroadcastMessage,
    9: pyaisnmea.messages.t9.Type9StandardSARAircraftPositionReport,
    10: pyaisnmea.messages.t10.Type10UTCDateInquiry,
    11: pyaisnmea.messages.t11.Type11UTCDateResponse,
    12: pyaisnmea.messages.t12.Type12AddressedSafetyMessage,
    13: pyaisnmea.messages.t13.Type13SafetyAcknowlegement,
    14: pyaisnmea.messages.t14.Type14SafetyBroadcastMessage,
    15: pyaisnmea.messages.t15.Type15Interrogation,
    16: pyaisnmea.messages.t16.Type16AssignmentModeCommand,
    17: pyaisnmea.messages.t17.Type17DGNSSBroadcastBinaryMessage,
    18: pyaisnmea.messages.t18.Type18PositionReportClassB,
    19: pyaisnmea.messages.t19.Type19ExtendedReportClassB,
    20: pyaisnmea.messages.t20.Type20DatalinkManagementMessage,
    21: pyaisnmea.messages.t21.Type21AidToNavigation,
    22: pyaisnmea.messages.t22.Type22ChannelManagement,
    23: pyaisnmea.messages.t23.Type23GroupAssignmentCommand,
    24: pyaisnmea.messages.t24.Type24StaticDataReport,
    25: pyaisnmea.messages.t25.Type25SingleSlotBinaryMessage,
    26: pyaisnmea.messages.t26.Type26MultipleSlotBinaryMessage,
    27: pyaisnmea.messages.t27.Type27LongRangeAISPositionReport}
