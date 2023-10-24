import asyncio
from mango_explorer_v4.mango_client import MangoClient
from solana.keypair import Keypair
from base58 import b58decode

async def main():
    mango_client = await MangoClient.connect('https://mango.rpcpool.com/946ef7337da3f5b8d3e4a34e7f88')
    
    # General data functions:
    print(mango_client.banks[0])
    

asyncio.run(main())