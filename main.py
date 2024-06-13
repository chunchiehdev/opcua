import sys
sys.path.insert(0, "..")
import logging
from opcua import Client
# from opcua import ua
# import time


def datachange_notification(node, val, data):
    print("Python: New data change event", node, val)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    client = Client("opc.tcp://localhost:50000/")
    client.set_security_string("Basic256Sha256,SignAndEncrypt,./opcua_certs/certs/cert.der,./opcua_certs/private/cert.pem")
    client.application_uri = "urn:OpcPlc:opcplc"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000

    try:
        client.connect()
        
        # subscription = client.create_subscription(500, datachange_notification)

        # print("sub", subscription)
        
        # temp_var = client.get_node("ns=2;s=PLATFORM.AUTO.TEST.WRITE.DATA")

        # data_type = temp_var.get_data_type_as_variant_type()
        # print(f"Node Type: {data_type}")

        # access_level = temp_var.get_access_level()
        # print(f"Access level: {access_level}")

        # display_name = temp_var.get_display_name()
        # print(f"Node name: {display_name}")
        
        # current_value = temp_var.get_value()
        # print(f"current value: {current_value}")
        
        # handle = subscription.subscribe_data_change(temp_var)
        
        # new_value = 5
        # print(f"subscribe node, try to change value: {new_value}")
        # temp_var.set_value(ua.Variant(new_value, ua.VariantType.Int32))

        # time.sleep(2)

        # temp_value_after_change = temp_var.get_value()
        # print("After changing: ", temp_value_after_change)
         

        # if temp_value_after_change == new_value:
        #     print("Successfully change")
        # else:
        #     print("Failed change")
        
        # input("Press Enter to stop...")
        
    finally:
        # subscription.delete()
        
        client.disconnect()
