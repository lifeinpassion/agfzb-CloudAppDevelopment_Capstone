"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("jaN9mt4_seKY2nHehFyECyfgMAHP89vo-I3Akj-zbX-i")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://f6affcd7-e822-4a4d-8078-bbcbaa8e4740-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
            db='reviews',
            selector={'dealership': {"$eq": int(dict["id"])}},
        ).get_result()
    
    try:
        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response}
        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': 'Something went wrong',
        }

if __name__ == '__main__':
    main(param_dict)


#Post reviews
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("jaN9mt4_seKY2nHehFyECyfgMAHP89vo-I3Akj-zbX-i")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://f6affcd7-e822-4a4d-8078-bbcbaa8e4740-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(
            db='reviews',
            document = dict['doc']
        ).get_result()
    
    try:
        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response}
        }
        return result
    except:
        return {
            'statusCode': 404,
            'message': 'Something went wrong',
        }