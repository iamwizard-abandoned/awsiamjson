from awsiamjson import *
import json
from jsonmerge import merge

_logger = logger.get_logger(__name__)

def main():
    _logger.info("IAM Wizard - AWS IAM JSON - Version 0.1")
    output_object = {}
    _logger.info("Adding Services...")
    output_object = add_services(output_object)
    _logger.info("Adding Actions and Condition Context Keys...")
    output_object = add_actions_and_context_keys(output_object)
    _logger.info("Adding API Descriptions...")
    output_object = add_api_descriptions(output_object)
    #output_object = json.load(open('good_output.json'))
    _logger.info("Combining Override File...")
    override_object = json.load(open('output_override.json'))
    combined_object = merge(output_object, override_object)
    _logger.info("Writing Output File...")
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/awsiam.json', 'w') as outfile:
        json.dump(combined_object, outfile, sort_keys=True, indent=4)
    #print(json.dumps(combined_object, sort_keys=True, indent=4))
    _logger.info("Exiting...")

if __name__ == '__main__':
    main()