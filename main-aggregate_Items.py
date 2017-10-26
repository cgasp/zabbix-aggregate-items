#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from zabbix.api import ZabbixAPI
import time
import random
import argparse
import configparser

##########
# 42 total items
##########
colors = {}
# dark colorssc
colors['dark_blue1'] = "5299AD"
colors['dark_violet'] = "5D549A"
colors['dark_green'] = "87B457"
colors['dark_red'] = "CF545E"
colors['dark_lemon'] = "CDDA13"
colors['dark_turquise'] = "5DAE99"
colors['dark_orange'] = "DD844C"
colors['dark_mauve'] = "AE5C8A"
colors['dark_ltbrown'] = "BD9F83"
colors['dark_blue2'] = "6B9BD4"
colors['dark_red-brown'] = "B75F73"
colors['dark_kaky'] = "646560"
colors['dark_deepblue'] = "335098"
colors['dark_bleu'] = "5FBFDB"
colors['dark_yellow'] = "D1CE85"
colors['dark_grey'] = "909090"
colors['dark_brown'] = "A16254"
colors['dark_pink'] = "E8678D"
colors['dark_deepgreen'] = "62B55A"
colors['dark_greypurple'] = "A599AD"
colors['dark_violet2'] = "6A5DD9"
# light colors
colors['light_blue1'] = "98D6E7"
colors['light_violet'] = "9E7EDF"
colors['light_green'] = "BDDA83"
colors['light_red'] = "EF747E"
colors['light_lemon'] = "EDFA33"
colors['light_tuquise'] = "7EC392"
colors['light_orange'] = "EDA46C"
colors['light_mauve'] = "DF93D7"
colors['light_ltbrown'] = "E2BB91"
colors['light_blue2'] = "A0CBEA"
colors['light_red-brown'] = "CB868B"
colors['light_kaky'] = "77897D"
colors['light_deepblue'] = "5370B8"
colors['light_bleu'] = "76DAF7"
colors['light_yellow'] = "EAD770"
colors['light_grey'] = "AEAEAE"
colors['light_brown'] = "B97A6F"
colors['light_pink'] = "E8849D"
colors['light_deepgreen'] = "95D36E"
colors['light_greypurple']= "B7AACF"
colors['light_violet2'] = "8A7DF9"


def arg_parse():
    text_description = """
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
            
        Example : 
    """

    parser = argparse.ArgumentParser(description=text_description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-G', '--graph_name', dest='graph_name',
                        action='store', type=str, help='Name for graph with founded items')
    parser.add_argument('-C', dest='calculated_item_name',
                        action='store', type=str, help='Calculated Item name with founded items')
    parser.add_argument('-O', dest='calculated_item_operator', default='+',
                        action='store', type=str, help="Operator to use for the Calculated Item ('+','-','/','*'")
    parser.add_argument('-F', dest='calculated_item_function', default='last',
                        action='store', type=str, help='Function to use for the Calculated Item (last, min, max, avg, count)')
    parser.add_argument('-H', '--re_host', dest='re_host',
                        action='store', type=str, required=True, help='Regex for Host Selection')
    parser.add_argument('-i', '--re_item', dest='re_item',
                        action='store', type=str, required=True, help='Regex for Item Selection')
    parser.add_argument('-k', '--search_by_key', dest='search_by_key',
                        action='store_true', help='Search by Key Value (instead of default Name)')
    parser.add_argument('--dry-run', dest='dry_run',
                        action='store_true', help="Don't create Graph or Calculated - only list founded items")
    return parser.parse_args()


###############################################################################
#
# Create Graph from Items
#
#
def verify_graph_exist(zapi, host, graph_name):

    try:
        graphs = zapi.graph.get(
            hostids=host,
            output='extend'
        )
    except:
        print("[WARNING] Problem in verifying Graph")


    for graph in graphs:
        if graph['name'] == graph_name:
            print("[ERROR] Graph Already Exist - Please choose another name")
            return True
    return False


def create_graph(zapi, graph_name, items_matched):

    gitems = []

    for k, v in items_matched.items():
        gitems.append({'itemid': k, "color": colors[random.choice(list(colors.keys()))]})

    try:
        zapi.graph.create(
            name=graph_name,
            gitems=gitems,
            # [{"itemid": "10735", "color": "26265b"},],
            width=900,
            height=200
        )
    except:
        print("[WARNING] Problem in creating Graph")

    print(
        "[INFO] Graph created\n"
        "\tname : " + graph_name + "\n"
    )


###############################################################################
#
# Calculated Items Generation
#
#
def retrieve_keys_for_formula(items_matched, items):
    key_items_list = []
    for item in items:
        if item['itemid'] in items_matched:
            key_items_list.append(item['key_'])
    return key_items_list


def generate_formula(key_items_list, calculated_item_operator, calculated_item_function):
    """ Generate formula for Calculated Item """

    valid_function = ['last', 'min', 'max', 'avg', 'count']
    valid_operator = ['+', '-', '/', '*']

    if calculated_item_operator in valid_operator and calculated_item_function in valid_function:
        key_items_list = [calculated_item_function + "(" + key_item + ")" for key_item in key_items_list]
        return calculated_item_operator.join(key_items_list)
    else:
        return False

def createCalculatedItem(zapi, hostid, calculated_item_name, key, items_matched, formula, calculated_item_operator, calculated_item_function):
    """ Create Calculated from a generated formula """

    if formula:
        item = zapi.item.create(
            name=calculated_item_name,  #
            key_=key,  #
            hostid=hostid,  #
            type=15,
            value_type=0,
            params=formula,
            # interfaceid = interfaceid, # optional for calculated items
            delay=60
        )

        print(
            "[INFO] calculated Item created\n"
            "\tname : " + calculated_item_name+"\n" 
            "\tkey_: " + key
              )
    else :
        print("[WARNING] Problem with Operator and Function of Calculated Item Formula")


###############################################################################
#
# Search Items in one Host
#
#
def returnItemList(zapi, hostid):
    return zapi.item.get(hostids = hostid, output = 'extend')

def retrieve_string_from_regex(pattern, string):
    # Return substring or False if not found
    try:
        return re.search(re.compile(pattern), string).group(1)
    except:
        return False


def search_items_in_one_Host(zapi,re_item, host, search_by_key):
    # Look for regex in item name (or key) in one Host
    regex_item = re.compile(re_item)

    itemList =  returnItemList(zapi, host)
    items_matched = {}

    if search_by_key:
        key_to_search = 'key_'
    else:
        key_to_search = 'name'

    for item in itemList:

        # print("itemid : " + item['itemid'] + " item name " + item['name'] + " item key : " + item['key_'])

        # If there is a variable in name
        if '$1' in item['name'] and not search_by_key:
            replace_var = retrieve_string_from_regex('\[(.*?)\]', item['key_'])
            # print(replace_var)
            item['name'] = item['name'].replace('$1', replace_var)

            # if regex_item.match(item['key_']): # replace_var:
            #   item['name'] = item['name'].replace('$1', replace_var)

        try:
            if regex_item.match(item[key_to_search]):  # retrieve_string_from_regex(search_pattern,item['name']):
                items_matched[item['itemid']] = item[key_to_search]

        except:
            print("[WARNING] Problem in Regex Item Name")
            pass
            # AAA, ZZZ not found in the original string
            # apply your error handling
    return items_matched


def retrieve_hostList(zapi,re_host):
    # Return the Host list from the given regex
    regex_host = re.compile(re_host)

    hosts = zapi.host.get(output='extend')
    hostList = []  # [host['hostid'] for host in hosts if retrieve_string_from_regex("lcr01.*", host['host'])]

    for host in hosts:
        if regex_host.match(host['host']):  # retrieve_string_from_regex("lcr01.*", ):
            hostList.append(host['hostid'])

    return hostList


def main():

    args = arg_parse()

    # Parse config file for the value to access Zabbix API
    config = configparser.ConfigParser()
    config.read_file(open(r'config.cfg'))
    zabbixurl = config.get('zabbix-config', 'serverurl')
    user = config.get('zabbix-config', 'user')
    password = config.get('zabbix-config', 'password')

    # Connect to Zabbix
    zapi = ZabbixAPI(url=zabbixurl, user=user, password=password)

    # re_host = 'lsr01.*'
    # re_item = '.*ps10.*'

    # -H 'lsr01.*' -i '.*ps10.*'

    # Measure Parse Execution time
    start_host_list = time.time()

    for host in retrieve_hostList(zapi, args.re_host):

        # Measure Parse Execution time
        start_host = time.time()

        items_matched = []

        items_matched = search_items_in_one_Host(zapi, args.re_item, host, args.search_by_key)
        if items_matched:
            # If match items name
            print("[INFO] Founded : " + str(len(items_matched)) + " Items")

            if not args.dry_run:
                if not verify_graph_exist(zapi, host, args.graph_name) and args.graph_name:
                    # Create Graph
                    create_graph(zapi, args.graph_name, items_matched)

                # Verify Item
                if args.calculated_item_name:

                    # Create Calculated Item
                    calculatedItemKey = "api_key_calculated_item." + str(random.randrange(10000, 99999))
                    formula = generate_formula(retrieve_keys_for_formula(items_matched, returnItemList(zapi, host)),
                                               args.calculated_item_operator, args.calculated_item_function)
                    createCalculatedItem(zapi, host, args.calculated_item_name, calculatedItemKey, items_matched,
                                         formula, args.calculated_item_operator, args.calculated_item_function)

            else:
                print("[INFO] DRY-RUN\n\tItem Matched : " + str(items_matched))
                if args.calculated_item_name:
                    print("[INFO] DRY-RUN\t Calculated Item Formula : " + generate_formula(retrieve_keys_for_formula(items_matched, returnItemList(zapi, host)),args.calculated_item_operator, args.calculated_item_function))

        else:
            print("[WARNING] No Items founded for the given Regular Expression - Please correct")

        end_host = time.time()
        print("[INFO] Host : " + host + "\t=> Process Time :" + str(end_host - start_host))

    end_host_list = time.time()
    print("[INFO] Hosts Total Process Time : " + str(end_host_list - start_host_list))

if __name__ == '__main__':
    main()