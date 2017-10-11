# zabbix-aggregate-items
Script to create Graph and calculated Items on Zabbix based on given Regex to filter hosts and items

## Description 

Script to create Graph and calculated Items on Zabbix. 
It retrieve the items for selected Hosts - filtered by regex through '-H' argument.  
After retrieve the items for a host it filter based on given regex '-i' argument.
The script can filter by Item Name or key (when --search_by_key used)

config.cfg must be adapted in order to connect to zabbix

Graph Creation Specific : 
    - Graph Name must be unique (if not error popup)
    - Graph color line are randomly selected 

Calculated Item Specific : 
    - Key Item will be generated based on "api_key_calculated_item.{{ random.randrange(10000, 99999) }}"

## Usage 

main-aggregate_Items.py [-h] [-G GRAPH_NAME] [-C CALCULATED_ITEM_NAME]
                               -H RE_HOST -i RE_ITEM [-k] [--dry-run]
               
## Example 

- Generate calculated item and graph from matched items in Regex.   

*python3 main-aggregate_Items.py -G "My Graph Name" -C "Calculated Item name" -H "router.*" -i "ethernet\d+\/\d+"*  

- Search by key name, use -k or --search_by_key argument
- Dry-Run (no item calculated and graph creation), use --dry-run


## Limitation 

- Calculated Items only last and sum function supported 
- No color selection on Graphline items  
- No settings of graph  

## License MIT 
