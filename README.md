# zabbix-aggregate-items
Script to create Graph and calculated Items on Zabbix based on given Regex to filter hosts and items

## Usage 

main-aggregate_Items.py [-h] [-G GRAPH_NAME] [-C CALCULATED_ITEM_NAME]
                               -H RE_HOST -i RE_ITEM [-k] [--dry-run]
               
## Example 

- Generate calculated item and graph from matched items in Regex. 
python3 main-aggregate_Items.py -G "My Graph Name" -C "Calculated Item name" -H "router.*" -i "ethernet\d+\/\d+"

- Search by key name, use -k or --search_by_key argument
- Dry-Run (no item calculated and graph creation), use --dry-run


## Limitation 

- No color selection on Graphline items  
- No settings of graph  


## License MIT 
