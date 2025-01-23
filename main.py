"""
We're going to attempt to add liquidity to a meteora pool
"""
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.message import Message
import asyncio
import os

API_KEY = os.getenv("API_KEY")

RPC_ENDPOINT = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"
PUB_KEY = 'Bj2VEavVi64zNFqs6P8BrwduT2eTCuASkWYtm3vAMw4'
#Turn into a pub key
PUB_KEY = Pubkey.from_string(PUB_KEY)

SENDER = Pubkey.from_string('Bj2VEavVi64zNFqs6P8BrwduT2eTCuASkWYtm3vAMw4')
RECEIVER = Pubkey.from_string('8Az4fKv45Z4TB3MMptE7b4NmsdVhnNeF1daMCHKR2NcB')

def get_solana_amount(account_info) -> float:
    """
    Gets the amount of solana in a GetAccountInfoResp object
    """
    lamports = account_info.value.lamports
    print(f"Amount of Solana: {lamports / 10**9}")
    return lamports / 10**9

I'll help create a practical function for sending SOL between accounts:
pythonCopyfrom solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solders.transaction import Transaction

def send_solana(sender_keypair: Keypair, receiver_pubkey: Pubkey, amount: float) -> str:
    """
    Sends solana from one account to another
    
    Args:
        sender_keypair (Keypair): The keypair of the sending account (must have private key)
        receiver_pubkey (Pubkey): The public key of the receiving account
        amount (float): Amount of SOL to send
        
    Returns:
        str: Transaction signature
        
    Raises:
        Exception: If transaction fails
    """
    try:
        # Connect to Solana
        client = Client("https://api.mainnet-beta.solana.com")  # For mainnet
        # client = Client("https://api.devnet.solana.com")      # For devnet
        
        # Convert SOL to lamports (1 SOL = 1 billion lamports)
        lamports = int(amount * 1_000_000_000)
        
        # Create transfer instruction
        transfer_ix = transfer(TransferParams(
            from_pubkey=sender_keypair.pubkey(),
            to_pubkey=receiver_pubkey,
            lamports=lamports
        ))
        
        # Create message
        message = Message([transfer_ix], sender_keypair.pubkey())
        
        # Get recent blockhash
        blockhash = client.get_latest_blockhash()
        
        # Create and sign transaction
        transaction = Transaction([sender_keypair], message, blockhash)
        
        # Send transaction
        signature = client.send_transaction(transaction)
        
        return signature
        
    except Exception as e:
        raise Exception(f"Failed to send SOL: {str(e)}")
    

async def main():
    async with AsyncClient(RPC_ENDPOINT) as client:
        res = await client.is_connected()
    

    # Alternatively, close the client explicitly instead of using a context manager:
    client = AsyncClient(RPC_ENDPOINT)
    res = await client.is_connected()

    #Get Account Info
    res = await client.get_account_info(PUB_KEY)
    get_solana_amount(res)

    
    

asyncio.run(main())