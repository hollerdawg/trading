"""This Python script provides examples on using the E*TRADE API endpoints"""
from __future__ import print_function
import configparser
import webbrowser
import json
import logging
import sys
import requests
from rauth import OAuth1Service
from logging.handlers import RotatingFileHandler
from .accounts.accounts import Accounts
from .market.market import Market

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5*1024*1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

class Client():
    # loading configuration file
    config = configparser.ConfigParser()
    config["SANDBOX"] = {
        "BASE_URL": "https://apisb.etrade.com",
        "KEY": "todo",
        "SECRET": "todo",
    }
    config["PRODUCTION"] = {
        "BASE_URL": "https://api.etrade.com",
        "KEY": "todo",
        "SECRET": "todo",
    }
    config.read('config.ini')  # TODO: Update to use user's config file
    mode = "SANDBOX"

    @classmethod
    def authorize(cls):
        """Allows user authorization for the sample application with OAuth 1"""
        etrade = OAuth1Service(
            name="etrade",
            consumer_key=cls.config[cls.mode]["KEY"],
            consumer_secret=cls.config[cls.mode]["SECRET"],
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url="https://api.etrade.com")

        # Step 1: Get OAuth 1 request token and secret
        request_token, request_token_secret = etrade.get_request_token(
            params={"oauth_callback": "oob", "format": "json"})

        # Step 2: Go through the authentication flow. Login to E*TRADE.
        # After you login, the page will provide a text code to enter.
        authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
        webbrowser.open(authorize_url)
        text_code = input("Please accept agreement and enter text code from browser: ")

        # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
        cls.session = etrade.get_auth_session(request_token,
                                    request_token_secret,
                                    params={"oauth_verifier": text_code})

    def __init__(self):
        self.base_url = self.config[self.mode]["BASE_URL"]

    def main_menu(self):
        """
        Provides the different options for the sample application: Market Quotes, Account List
        """

        menu_items = {"1": "Market Quotes",
                    "2": "Account List",
                    "3": "Exit"}

        while True:
            print("")
            options = menu_items.keys()
            for entry in options:
                print(entry + ")\t" + menu_items[entry])
            selection = input("Please select an option: ")
            if selection == "1":
                market = Market(self.session, self.base_url)
                market.quotes()
            elif selection == "2":
                accounts = Accounts(self.session, self.base_url)
                accounts.account_list()
            elif selection == "3":
                break
            else:
                print("Unknown Option Selected!")
