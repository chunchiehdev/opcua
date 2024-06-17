import asyncio
from asyncua import Client
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

import logging

_logger = logging.getLogger(__name__)

async def main():
    url = "opc.tcp://localhost:4840"
    client = Client(url=url)

    await client.set_security(
        SecurityPolicyBasic256Sha256,
        "./client_certs/certs/cert.der",
        "./client_certs/private/cert.pem"
    )
    client.application_uri = "urn:OpcPlc:opcplc"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000

    try:
        async with client:
            _logger.info("Connected to OPC UA server")

            _logger.info("Root node is: %r", client.nodes.root)
            _logger.info("Objects node is: %r", client.nodes.objects)
            
            namespaces = await client.get_namespace_array()
            for idx, ns in enumerate(namespaces):
                _logger.info(f"Namespace {idx}: {ns}")
                
            uri = "http://microsoft.com/Opc/OpcPlc/"
            idx = await client.get_namespace_index(uri)
            node_id = f"ns={idx};s=TemperatureSensor1" 
            var = client.get_node(node_id)

            try:
                exists = await var.read_data_value()
                _logger.info("Node value: %r", exists)
            except Exception as e:
                _logger.error("Failed to read node value: %s", e)

            
            try:
                res = await var.read_data_value()
                _logger.info("Read value: %r", res)
            except Exception as e:
                _logger.error("Failed to read node value: %s", e)
    except Exception as e:
        _logger.error("Failed to connect or interact with OPC UA server: %s", e)
    finally:
        await client.disconnect()
        _logger.info("Disconnected from OPC UA server")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
