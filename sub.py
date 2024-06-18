import asyncio
from asyncua import Client
from asyncua.common.subscription import Subscription

class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    """
    def datachange_notification(self, node, val, data):
        print("New data change event on node {}: Value = {}".format(node, val))

    def event_notification(self, event):
        print("New event", event)

async def main():
    # URL of the OPC PLC server
    url = "opc.tcp://localhost:51210"

    async with Client(url) as client:
        # Assuming you know the NodeId of the node you want to subscribe to
        node = client.get_node("ns=2;i=2")

        # Create a subscription handler
        handler = SubHandler()

        # Create a subscription
        subscription = await client.create_subscription(100, handler)

        # Subscribe to the node
        handle = await subscription.subscribe_data_change(node)

        print("Subscribed to the node. Waiting for data changes...")

        # Keep the subscription active
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
