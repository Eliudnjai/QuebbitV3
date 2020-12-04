import os
import json

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    STRIPE_PUBLIC_KEY = config.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = config.get('STRIPE_SECRET_KEY')
