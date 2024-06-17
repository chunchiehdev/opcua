import asyncio
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from asyncua import Client
import json

async def browse_node(node, node_list):
    children = await node.get_children()
    for child in children:
        try:
            browse_name = await child.read_browse_name()
            node_id = child.nodeid
            node_list.append({"Node Name": browse_name.Name, "Node ID": node_id.to_string()})

            await browse_node(child, node_list)
            
        except Exception as e:
            print(f"Error reading value from node {child}: {e}")

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

    async with client:
        print(f"Connected to {url}")

        root = client.nodes.root
        print("Root node is: ", root)

        # node_list = []
        # await browse_node(root, node_list)


        # with open("node_list.txt", "w") as file:
        #     json.dump(node_list, file, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
