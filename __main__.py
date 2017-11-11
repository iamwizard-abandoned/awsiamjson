from awsiamjson import *
import json

_logger = logger.get_logger(__name__)

def main():
    _logger.info("IAM Wizard - AWS IAM JSON - Version 0.1")
    output_object = {}
    output_object = add_services(output_object)
    output_object = add_actions_and_context_keys(output_object)
    output_object = add_api_descriptions(output_object)
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/awsiam.json', 'w') as outfile:
        json.dump(output_object, outfile, sort_keys=True, indent=4)
    print(json.dumps(output_object, sort_keys=True, indent=4))
    _logger.info("Exiting...")

if __name__ == '__main__':
    main()