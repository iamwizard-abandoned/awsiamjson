from .logger import *
import requests
import re
from lxml import html

_logger = get_logger(__name__)


def add_services(input_dict):
    base_url = 'http://docs.aws.amazon.com/IAM/latest/UserGuide/'
    page = requests.get(base_url + 'reference_policies_actionsconditions.html')
    tree = html.fromstring(page.content)
    aws_services = tree.xpath('//*[@id="main-col-body"]/div[@class="highlights"]/ul/li/a')
    services = {}
    for cur_service in aws_services:
        short_name = re.search(r"list_(.+).html", cur_service.attrib['href']).group(1).lower()
        if cur_service.text not in services:
            services[short_name] = {}
            services[short_name]['Name'] = cur_service.text
            services[short_name]['URL'] = base_url + cur_service.attrib['href']
    input_dict['services'] = services
    return input_dict
