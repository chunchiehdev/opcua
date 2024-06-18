import asyncio
from asyncua import Client, ua
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
import logging
# import numpy as np

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

logging.getLogger("asyncua.client.client").setLevel(logging.WARNING)

    
async def fetch_node_value(client: Client, node_id: str):
    try:
        
        var = client.get_node(node_id)
        data_value = await var.read_data_value()
        _logger.info("Node value: %r", data_value)

        parsed_data = {
            "value": data_value.Value.Value,
            "type": data_value.Value.VariantType,
            "source_timestamp": data_value.SourceTimestamp,
            "server_timestamp": data_value.ServerTimestamp,
            "status_code": data_value.StatusCode_
        }

        return parsed_data
    
    except Exception as e:
        _logger.error("Failed to read node value: %s", e)
        return None
    
async def write_node_value(client: Client, node_id: str, value):
    try:

        node = client.get_node(node_id)
        await node.write_value(ua.DataValue(ua.Variant(value, ua.VariantType.Int64)))  
        _logger.info("Successfully wrote value to node %s", node_id)

    except Exception as e:
        _logger.error("Failed to write value to node %s: %s", node_id, e)
        


async def browse_namespace(client, namespace_index):
    objects = client.nodes.objects

    _logger.info(f"Browsing node in namespace {namespace_index}")

    async def browse_node(node):
        children = await node.get_children()
        print("children", children)
        for child in children:
            node_id = child.nodeid
            browse_name = await child.read_browse_name()
            display_name = await child.read_display_name()
            references = await child.get_references(refs=ua.BrowseDirection.Forward)
            node_class = await child.read_node_class()

            print("reference", references)
            print("node_class", node_class)
            
            print(f"Node ID: {node_id}, Browse Name: {browse_name}, Display Name: {display_name}")
            # await browse_node(child)
            # browse_name = await child.read_browse_name()
            # display_name = await child.read_display_name()
            # _logger.info(f"Node ID: {node_id}, Browse Name: {browse_name}, Display Name: {display_name}")

            # await browse_node(child)

    await browse_node(objects)


async def main():
    url = "opc.tcp://localhost:4840"
    client = Client(url=url)
    client.application_uri = "urn:OpcPlc:opcplc"

    await client.set_security(
        SecurityPolicyBasic256Sha256,
        "./client_certs/certs/cert.der",
        "./client_certs/private/key.pem"
    )
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000

    try:
        async with client:
            _logger.info("Connected to OPC UA server")
            server_node = client.get_node("ns=0;i=2253")  
            diagnostics_node = await server_node.get_child(["0:ServerDiagnostics", "0:SessionsDiagnosticsSummary"])
            sessions = await diagnostics_node.get_child("0:SessionDiagnosticsArray")
            session_array = await sessions.read_value()
            
            # for session in session_array:
            #     print(f"Session Name: {session.SessionName}")
            #     print(f"Client Description: {session.ClientDescription.ApplicationName}")
            #     print(f"Client URI: {session.ClientDescription.ApplicationUri}")
            #     print(f"Client Product URI: {session.ClientDescription.ProductUri}")
            #     print(f"Client Connection Time: {session.ClientConnectionTime}")
            #     print(f"Client Last Contact Time: {session.ClientLastContactTime}")
            #     print(f"Current Subscriptions Count: {session.CurrentSubscriptionsCount}")
            #     print("-" * 50)

            namespaces = await client.get_namespace_array()
            for idx, ns in enumerate(namespaces):
                _logger.info(f"Namespace {idx}: {ns}")
                
            uri = "http://microsoft.com/Opc/OpcPlc/"
            idx = await client.get_namespace_index(uri)
            node_id = f"ns={idx};s=TemperatureSensor1" 
            node_data = await fetch_node_value(client, node_id)

            if node_data:
                _logger.info(f"Parsed value: {node_data['value']}")
                _logger.info(f"Value type: {node_data['type']} ({node_data['type'].name})")
                _logger.info(f"Source timestamp: {node_data['source_timestamp'] or 'None'}")
                _logger.info(f"Server timestamp: {node_data['server_timestamp'] or 'None'}")
                _logger.info(f"Status code: {node_data['status_code']}")


            new_value = 10000
            # uint32 = np.uint32(new_value)
            await write_node_value(client, node_id, new_value)


            for session in session_array:
                print(f"Session Name: {session.SessionName}")
                print(f"Client Description: {session.ClientDescription.ApplicationName}")
                print(f"Client URI: {session.ClientDescription.ApplicationUri}")
                print(f"Client Product URI: {session.ClientDescription.ProductUri}")
                print(f"Client Connection Time: {session.ClientConnectionTime}")
                print(f"Client Last Contact Time: {session.ClientLastContactTime}")
                print(f"Current Subscriptions Count: {session.CurrentSubscriptionsCount}")
                print("-" * 50)

            # namespaces_index = 2
            # await browse_namespace(client, namespaces_index)

    except Exception as e:
        _logger.error("Failed to connect or interact with OPC UA server: %s", e)
    finally:
        await client.disconnect()
        _logger.info("Disconnected from OPC UA server")

if __name__ == "__main__":
    asyncio.run(main())
