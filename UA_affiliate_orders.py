import collections
import requests
import pandas as pd
import json
import os
from pprint import pprint, pformat
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, date
import time
from pprint import pprint


headers = {
        'accept': 'application/json',
        'X-Auth-API-Key': os.environ.get('THINKIFIC_API_KEY'),
        'X-Auth-Subdomain': os.environ.get('THINKIFIC_SUBDOMAIN')
    }


def main():

    get_affiliate_orders()
    get_affiliate_cash_made()


list_of_affiliate_orders = []
affiliate_cash_made = []
tribe_affiliate_cash_made = []


def get_affiliate_orders(page_num=1):
    with open("affiliate_members.json", "r") as affiliate_members:
        affiliate_members = json.load(affiliate_members)
    list_of_affiliate_members = affiliate_members

    params = (
            ('page', page_num),  # page_num
            # as of 9/21 there are a total of 17962 users
            # as of 11/7 there are a total of 18261 users
            ('limit', '1000')
            # ('limit', '100')
        )

    response = requests.get('https://api.thinkific.com/api/public/v1/orders?', headers=headers, params=params)
    # members_response = response.text.encode('utf8')
    # members_parsed = json.loads(members_response)
    # members = members_parsed
    # url = "https://api.thinkific.com/api/public/v1/orders?page=1&limit=10000"

    payload = {}

    # response = requests.request("GET", url, headers=headers, data=payload)
    orders_response = response.text.encode('utf8')
    orders_parsed = json.loads(orders_response)
    # pprint(orders_parsed)
    current_page = orders_parsed["meta"]["pagination"]["current_page"]
    # print("CURRENT PAGE = ", current_page)
    next_page = orders_parsed["meta"]["pagination"]["next_page"]
    # print("NEXT PAGE = ", next_page)
    total_pages = orders_parsed["meta"]["pagination"]["total_pages"]
    total_items = orders_parsed["meta"]["pagination"]["total_items"]
    # orders_df = pd.json_normalize(orders_parsed['items'])
    for affiliate_member in list_of_affiliate_members:
        # print(affiliate_member)
        affiliate_referral_code = affiliate_member["affiliate_code"]

        affiliate_commision = int(affiliate_member["affiliate_commission"])
        affiliate_student_id = affiliate_member["student_id"]
        # pprint(f" affiliate referral code - {affiliate_referral_code}")
        # for order in orders_df:
        for order in orders_parsed['items']:
            # print(f"order here - {order['affiliate_referral_code']}")
            if order["affiliate_referral_code"] == affiliate_referral_code:
                print("AFFILIATE ORDER")
                if float(order["amount_dollars"]) > 0:
                    affiliate_order = {'affiliate_refferal_code': order["affiliate_referral_code"],
                                       'amount_dollars': float(order["amount_dollars"]),
                                       'amount_cents': order["amount_cents"],
                                       }
                    list_of_affiliate_orders.append(affiliate_order)
                    price_paid = float(order["amount_dollars"])
                    affiliate_commision_as_decimal = affiliate_commision/100
                    affiliate_commision_earned = round(price_paid * affiliate_commision_as_decimal, 2)
                    discounted_price = round(price_paid - affiliate_commision_earned, 2)
                    print(f"affiliate commision as decimal = {affiliate_commision_as_decimal}")
                    print(f"affiliate commision earned {price_paid} * {affiliate_commision_as_decimal} = {affiliate_commision_earned}")
                    print(f"discounted price {price_paid} - {affiliate_commision_earned} = {discounted_price}")
                    pprint(affiliate_order)
                    affiliate_cash_made.append({affiliate_student_id:affiliate_commision_earned})

    if current_page != total_pages:
        page_num += 1
        get_affiliate_orders(page_num)
    else:
        print("The End of get_affiliate_orders()")

    return list_of_affiliate_members


def get_affiliate_cash_made():
    cash_made_per_affiliate = collections.Counter()
    total_tribe_cash_made = 0
    for cash_made in affiliate_cash_made:
        # affiliate_cash = cash_made
        # print(affiliate_cash)
        cash_made_per_affiliate.update(cash_made)

        for cash in cash_made:
            total_tribe_cash_made = cash_made[cash] + total_tribe_cash_made

            print(total_tribe_cash_made)
    print(f"total cash made = {cash_made}")
    cash_made_per_affiliate = dict(cash_made_per_affiliate)

    print("affiliate cash made")
    print(cash_made_per_affiliate)

    average_tribe_cash_made = total_tribe_cash_made/len(affiliate_cash_made)
    print(f"length of cash_made_per_affiliate = {len(affiliate_cash_made)} ")
    print(f"averaage tribe cash made = {average_tribe_cash_made}")


if __name__ == "__main__":
    main()
