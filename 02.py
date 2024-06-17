import asyncio
import logging
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256

from asyncua import Client

_logger = logging.getLogger(__name__)


async def main():

    url = "opc.tcp://localhost:50000"
    client = Client(url=url)
    
    client.application_uri = "urn:OpcPlc:opcplc"
    
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        "./client_certs/certs/cert.der",
        "./client_certs/private/cert.pem"
    )
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000

    async with client:
        
        ep = await client.get_endpoints()
        print(ep[0].Server.ApplicationUri)

        print("A", await client.get_namespace_array())
        print("N", await client.get_namespace_index('urn:OpcPlc:opc-deployment-7f8b4895bf-kzdqv'))
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)

        _logger.info("Children of root are: %r", await client.nodes.root.get_children())

        var = client.get_node("ns=1;s=PLATFORM.AUTO.TEST.WRITE.DATA")
        print(var)

        
        # idx = await client.get_namespace_index(uri)
        # _logger.info("index of our namespace is %s", idx)

        # res = await var.read_data_value() # get value of node as a DataValue object
        # _logger.info("read_data_value:", res)
        # resp = await var.read_value() # get value of node as a python builtin
        # _logger.info("read_data_value:", resp)

        # await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # await var.write_value(3.9) # set node value using implicit data type



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())