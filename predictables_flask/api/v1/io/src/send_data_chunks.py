import asyncio
from typing import List

import aiohttp
import pandas as pd


# Asynchronous function to send the JSON data
async def send_json_data(session, url, json_data):
    async with session.post(url, json=json_data) as response:
        return await response.text()


# Function to handle the sending of each chunk
async def send_chunks(url: str, chunks: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [send_json_data(session, url, chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
        return results


# Main coroutine to split the DataFrame and send the chunks
async def split_and_send_dataframe(df: pd.DataFrame, url: str, n_chunks: int = 20):
    chunks = dataframe_to_json_chunks(df, n_chunks)
    results = await send_chunks(url, chunks)
    print(results)  # Or handle the results as needed
