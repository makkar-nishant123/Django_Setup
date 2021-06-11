

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from datetime import datetime
from django.shortcuts import render
import csv, json
import requests
from requests.auth import HTTPBasicAuth 
import time
import random
from django.contrib import messages
from django.http import HttpResponseForbidden




# Create your views here.


# HTML VIEWS
####################################################

# Index
def index(request):
    return HttpResponse("Hello, world!")




def sessionLogin(request):

    # Web form, allow user to submit username, password, and domain
    # If authenticated, return authentication token

    return HttpResponse("IMPLEMENTATION IN PROGRESS")
    
@api_view(['GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
def uploadFgt61e(request):

    username = str(request.user)
    if request.auth:
        userAuth = str(request.auth)
    else:
        userAuth = "None"

    context = {
        "username":username,
        "user_auth":userAuth
    }
    return render(request, 'scheduler_site/scheduler.html', context)


@api_view(['POST'])
def submitFgt61e(request):
    try:
        csvString = request.POST["csv_string"]
        deviceModel = request.POST["drop"] # Devices e.g. ForitGate-81E

        if csvString:

            csvReader = csv.DictReader(csvString.splitlines())
            spreadsheetList = [row for row in csvReader]
            spreadsheetDicts = [dict(item) for item in spreadsheetList]

            successSites = []
            failedSites = []
            device_dict = {"FortiGate-61E":"FGT61E-","FortiGate-60F":"FGT60F-","FortiGate-81E":"FGT81E-","FortiGate-30E-3G4G-GBL":"FGT30E-3G4G-GBL-"}
            # For each of the sites in the spreadsheet
            for device in spreadsheetDicts:
                # Create the deployment: need cust_secret_name, device_model, and siteData

                try:
                    # deploymentId = "FGT61E-" + str(device["Site ID"])

                    deploymentId = device_dict[str(deviceModel)] + str(device["Site ID"])

                    # Get cust_secret_name
                    nmd = device.get("NMD") or device.get("NMD", "")
                    if not nmd:
                        nmd = device['HNS_PPP_Domain'][:3].lower()

                    device["NMD"] = nmd
                    custSecretName = "".join(["cust-", nmd])

                    #TODO get device_model
                    deviceModel = "FortiGate-" + str(device["Site ID"])

                    # get siteData
                    siteData = json.dumps(device)

                    # Create the deployment
                    protocol = "http://"
                    domain = "66.82.254.164"
                    path = "/api/v3.1/deployments/"

                    url = "".join([protocol, domain, path, deploymentId])

                    header = {
                        "Content-Type":"application/json",
                        "Tenant":"default_tenant"
                    }

                    querystring = {"_include":"id"}
                    payload = {
                        "blueprint_id":"Fortigate_Emperor_1",
                        "inputs":{
                            "cust_secret_name":custSecretName,
                            "device_model":deviceModel,
                            "siteData":siteData
                        }

                    }

                    auth = HTTPBasicAuth("admin", "Hughes@01")

                    res = requests.put(url, auth = auth, headers=header, json=payload, params=querystring)

                    if res.status_code >= 200 and res.status_code <300:
                    #if True:

                        # Success!
                        successSites.append(device["Site ID"])

                    else:
                        failedSites.append(device["Site ID"])
                        # booo!

                except Exception as e:
                    # List of failed sites
                    failedSites.append(device["Site ID"])


            # Run the compose workflow on all successful sites
            failedCompose = []
            for site in successSites:

                try:
                    # Set up request
                    protocol = "http://"
                    domain = "66.82.254.164"
                    path = "/api/v3.1/executions"
                    deploymentId = "FGT61E-" + str(device["Site ID"])

                    url = "".join([protocol, domain, path])

                    header = {
                        "Content-Type":"application/json",
                        "Tenant":"default_tenant"
                    }
                    auth = HTTPBasicAuth("admin", "Hughes@01")

                    payload = {
                        "deployment_id":deploymentId,
                        "workflow_id":"compose"
                    }

                    success = False
                    tryTime = 0
                    # Try multiple times to compose, may take a few seconds for deployment to finish coming up
                    while(success == False and tryTime < 10):


                        res = requests.post(url, headers = header, auth = auth, json=payload)

                        #if random.randint(0,3) == 0:
                        if res.status_code >= 200 and res.status_code <300:
                            # success
                            success = True #break our loop

                        else:
                            #boooo
                            tryTime += 1
                            time.sleep(1)

                    if not success:
                        failedCompose.append(device["Site ID"])

                except:
                    failedCompose.append(device["Site ID"])


            # Remove sites that failed compose from the successes
            successSites = [site for site in successSites if site not in failedCompose]
            for site in failedCompose:
                failedSites.append(site)


            # Not sure what the site key will be. Maybe SAN/HNS LocationID/Other
            #siteKey = "ID"
            if len(successSites) > 0:
                successMessage = "&success=" + "&success=".join(successSites)
            else:
                successMessage = "&success="
            if len(failedSites) > 0:
                failMessage = "&failed=" + "&failed=".join(failedSites)
            else:
                failMessage = "&failed="

            return HttpResponseRedirect("/scheduler_site/fgt61econfirm?" + successMessage + failMessage)


        else:
            # Missing required param csv_string
            return HttpResponse("Missing required field csv_string")



    except Exception as e:
        return HttpResponse(repr(e))






@api_view(["GET"])
def login(request):
    return render(request, 'scheduler_site/login.html', {})




@api_view(["POST","GET"])
def submit_login(request):
    if request.method == "GET":
        return render(request, 'scheduler_site/login.html', {})
        #return HttpResponseForbidden();
    if request.POST["username"] == "admin" and request.POST["password"] == "admin": #Temporary way/
        return render(request, 'scheduler_site/scheduler.html', {})
    else:
        messages.add_message(request, messages.ERROR, '', extra_tags='')
        messages.error(request, 'Incorrect Username or Password')
        return render(request, 'scheduler_site/login.html', {})



# API VIEWS
####################################################

# API Index
def apiIndex(request):
    return JsonResponse({"detail":"Hello, world!"})


