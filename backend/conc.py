import asyncio
import httpx

BASE_URL = "https://aircook-light.onrender.com/get-recipe"

# Different user inputs
inputs = ["spicy pork", "sweet tofu", "grilled chicken", "vegan curry", "teriyaki salmon"]

async def fetch(client, user_input):
    params = {"user_input": user_input}
    try:
        response = await client.get(BASE_URL, params=params)
        print(f"{user_input} → {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"{user_input} → Error: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, input_text) for input_text in inputs]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
