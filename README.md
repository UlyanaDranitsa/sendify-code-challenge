# MCP server for tracking your shipments with DB Schenker Shipment Tracker

## About this MCP server
This server exposes a tool that retrieves, structures shipment data from a tracking website (https://www.dbschenker.com/app/tracking-public/), as well as connects and provides context to a host, in this case, Claude for Desktop. You can also use any other LLM as an MCP host.
## Instructions on how to run and test the server
#### 1. Follow the Docker Desktop installation guide for your OS
[Install Docker Desktop for your system](https://docs.docker.com/manuals/) (if you do not already have it)
#### 2. Clone this repository into the directory of your choice on your computer
#### 3. Create Docker image based on the Dockerfile
- Open the root folder of the repository you just cloned inside the terminal
- Run the following command:
```
docker build -t shipment_mcp_server:latest .
```
The image will require ~5 GB of disk space
#### 4. Set up Claude Desktop
- Follow the installation guide for installing Claude Desktop for your system (if you do not already have it)
- Open the app, then log in or create a new account
- Once you can see the input field, click the hamburger menu in the top left of the app window.
- Navigate to File -> Settings -> Developer
- Click Edit Config, your file explorer will open at the location of claude_desktop_config.json file
- Open this config file (in a text editor, for example) and add our new MCP server to mcpServers list like so
```
"mcpServers": {
    "shipment_mcp_server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "shipment_mcp_server:latest"
      ]
    }
  }
  ```
- Save the file, then restart Claude Desktop
#### 5. Check setup correctness
- Open Claud
- Click the plus icon at the bottom left of the text field
- If you can see *shipment_mcp_server* when hovering over the "Connectors" menu item, the server is running, and you are ready to test the tool
#### 6. Ask AI about the details or tracking history of the shipments with the following reference numbers:
- 1806203236 and 1806256390 are valid reference numbers
- 1806203237, 123 and non-numeric values like "mynumber" are invalid
