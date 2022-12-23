/**
 * Get all databases
 */

 const { CloudantV1 } = require("@ibm-cloud/cloudant");
 const { IamAuthenticator } = require("ibm-cloud-sdk-core");

 params = {
  "COUCH_URL": "https://f6affcd7-e822-4a4d-8078-bbcbaa8e4740-bluemix.cloudantnosqldb.appdomain.cloud",
  "IAM_API_KEY": "jaN9mt4_seKY2nHehFyECyfgMAHP89vo-I3Akj-zbX-i",
  "COUCH_USERNAME": "f6affcd7-e822-4a4d-8078-bbcbaa8e4740-bluemix"
}
 
 function main(params) {
   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
   const cloudant = CloudantV1.newInstance({
     authenticator: authenticator,
   });
   cloudant.setServiceUrl(params.COUCH_URL);
 
   let dbList = getDbs(cloudant);
   return { dbs: dbList };
 }

 function getDbs(cloudant) {
   cloudant
     .getAllDbs()
     .then((body) => {
       body.forEach((db) => {
         dbList.push(db);
       });
     })
     .catch((err) => {
       console.log(err);
     });
 }

 main(params);