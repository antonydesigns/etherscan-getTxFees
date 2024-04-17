import requests
import pandas as pd
import os


class GetTxFee:
    def __init__(self, apiKey="", path_to_csv=""):

        # Check that Api Key is provided

        if apiKey == "":
            self.err("Script cannot continue without API key.")
            return

        # Check the file path is provided and file is available

        elif not os.path.exists(path_to_csv):
            self.err("Data file is not found or path is wrong.")
            return

        # Read CSV and convert the one column to a list (array) of transactions (txs)

        df = pd.read_csv(path_to_csv)
        txs = df["header"].to_list()

        # Load the Api Key
        # Execute program

        self.apiKey = apiKey

        # Loop through the txs array
        # For each iteration, append the Tx ID and Tx Fee into 'result'

        result = []

        for i in range(len(txs)):

            # Etherscan API endpoint
            api_url = "https://api.etherscan.io/api"

            # Parameters for the API query
            params = {
                "module": "proxy",
                "action": "eth_getTransactionByHash",
                "txhash": txs[i],
                "apikey": self.apiKey,
            }

            response = requests.get(api_url, params=params)
            data = response.json()

            if "status" in data and data["status"] == "0":
                self.err(data["result"])
                print("Ending program...")
                print("")
                print("")
                return

            else:
                gasUsed = self.convert_hex_dec(data["result"]["gas"])
                gasPrice = self.convert_hex_dec(data["result"]["gasPrice"])
                fee = gasUsed * gasPrice / (10**18)
                result.append([str(txs[i]), str(fee)])
                print(f"{(i+1)/len(txs)*100}% done")

        # Convert the list as a pandas dataframe
        # to make it easier to convert back to CSV

        result = pd.DataFrame(result, columns=["Tx ID", "Tx Fee (ETH)"])
        result.to_csv("tx_id__tx_fees_.csv", index=False)

    # Some utility functions...

    def convert_hex_dec(self, hex_string):
        decimal_value = int(hex_string, 16)
        return decimal_value

    def err(self, msg=""):
        shrug_emoticon = r"¯\_(ツ)_/¯"
        print("")
        print("")
        print(f"OOPS... THERE'S AN ERROR  {shrug_emoticon}")
        print("")
        print("")
        print(msg)
        print("")
        print("")
