# client_test.py
import asyncio
from fastmcp import Client


async def main():
    # Point the client at the running script
    # (FastMCP knows how to handle .py files via stdio)
    client = Client("open_meteo_mcp.py")
    async with client:
        print("Client connected. Calling tool...")
        try:
            # Replace "London" with a location you want to test
            result = await client.call_tool(
                "get_current_weather", {"location": "Houston"}
            )
            print("\n--- Weather Result ---")
            print(result)
            print("----------------------\n")
        except Exception as e:
            print(f"An error occurred: {e}")
        print("Client disconnecting.")


if __name__ == "__main__":
    asyncio.run(main())
