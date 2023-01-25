# Amazon Sidewalk Sample IoT App

This is an application that demonstrates a simple Sidewalk-based IOT use-case: a temperature sensor that communicates with Cloud backend over the secure Sidewalk network.
It consists of an edge device (a sensor) and application server (cloud backend with web UI). Edge device, after initial setup and registration in Sidewalk network, periodically sends the temperature measurement to the backend. The backend visualizes the data on graphical UI in a form of chart.

A user can engage buttons on the edge device, which is reflected corresponding button icon in the web UI (uplink communication).  
A user can toggle LED buttons in the UI view, which is then propagated to corresponding LEDs in the edge device (downlink communication).  
It is possible to add multiple edge devices (sensors) to work with a single application server. In such a case, the UI will represent each edge device as a separate tile in the view.

Each sensor must be flashed with an application binary (a program that reads temperature and sends it over Sidewalk protocol - it's the same binary for all edge devices)
and a personalization binary (a binary blob that contains serial number, ciphering keys and authorization data individual for each device).
Cloud backend identifies/authorizes each edge device based on the data present in personalization binary, which ensures E2E encryption and highly secure communication channel.

## Assumptions
It is assumed that you have an operational Sidewalk-enabled gateway available (eg. Amazon Echo 4th Gen). The gateway is a bridge between edge devices (sensors) and the cloud backend.
Installation and configuration of the gateway is not covered in this readme.

|WARNING: Sidewalk is activated only for gateways located in the USA |
|---|

## Prerequisites
- Python 3.6 or above (https://www.python.org/)
- AWS account; permissions to create resources (https://aws.amazon.com/)
- *config* and *credentials* files configured (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- MCU-specific toolchains:
    - Nordic
        - GNU Arm Embedded Toolchain (https://developer.arm.com/downloads/-/gnu-rm)
        - nRF Command Line Tools (https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools)
    - TI:
        - GNU Arm Embedded Toolchain (https://developer.arm.com/downloads/-/gnu-rm)
        - UniFlash (https://www.ti.com/tool/UNIFLASH)
    - SiLabs:
        - Simplicity Commander (https://community.silabs.com/s/article/simplicity-commander)


Make sure that *GNU ARM Toolchain* (for Nordic/TI) and/or *Simplicity Commander* (for SiLabs) are present in your system PATH.  
--> Try calling *arm-none-eabi-objcopy --version* in the terminal to make sure the GNU ARM Toolchain is available  
--> Try calling *commander --version* in the terminal to make sure the Simplicity Commander is available

## Getting Started

### 1. Install virtual environment

1. Open command line terminal and navigate to project's top level directory.

2. Install virtualenv and required packages. Just copy/paste commands to the terminal.  
   You may need to use *python* instead of *python3* alias, depending on your configuration.

- Linux / MacOS:
```
python3 -m pip install --user virtualenv
python3 -m venv sample-app-env
source sample-app-env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

- Windows:
```
python3 -m pip install --user virtualenv
python3 -m venv sample-app-env
sample-app-env\Scripts\activate.bat
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Fill out configuration file
Fill out [config](./config.yaml) file with your details (or leave default values):
- *AWS_PROFILE* - Profile to be used during the stack creation. If you have a custom named profile in your AWS CLI configuration files, replace 'default' with the name of your profile. Usually, you'd have just one profile named 'default'.

- *DESTINATION_NAME* - The Sidewalk destination used for uplink traffic routing. Can be any string.

- *HARDWARE_PLATFORM* - *NORDIC* or *TI* or *SILABS* (or *ALL* if you want to have personalization data generated for all three platforms)

### 3. Deploy cloud infrastructure

For the sample application to work, you need to deploy necessary resources to your AWS account.  

**Before running the script, ensure that you have sufficient permissions to create resources listed in [SidewalkSampleApplicationStack.yaml](./ApplicationServerDeployment/template/SidewalkSampleApplicationStack.yaml)**  
You can reuse [DeployStackPolicy.json](./ApplicationServerDeployment/template/DeployStackPolicy.json) template to create a policy document, which then can be assigned to the user associated with the *AWS_PROFILE*. It provides all the permissions needed to create the *SidewalkSampleApplicationStack*.  
In order to do so:
- open *DeployStackPolicy.json*, replace all the occurrences of *<account_ID>* with your AWS Account ID
- go to the IAM console, create the policy using *DeployStackPolicy.json* content
- assign created policy to the user associated with your *AWS_PROFILE*

Refer to the [IAM tutorial: Create and attach your first customer managed policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_managed-policies.html) for further guidance.

|WARNING: You will be billed for the usage of AWS resources created by this application. |
|---|

1. Edit following fields in the [config](./config.yaml) file (or leave default values):


2.  Run deployment script:
    ```
    python3 ApplicationServerDeployment/deploy_stack.py
    ```
    Type `y` when asked to proceed.  
    Wait for the deployment to complete (it usually takes ~5 minutes).

3. Go to the URL printed in the console. It is also stored in the [config](./config.yaml) under *WEB_APP_URL*.  
   Your device will appear in the web app, once embedded app sends a first uplink message.

   |WARNING: The web app is publicly available. Anyone who has the right URL can interact with your device. |
       |---|

### 4. Provision edge device

This step creates individual personalisation data for the edge device.
It interacts with AWS to create WirelessDevice in the backend, downloads created data and compiles binary blob that can be flashed onto the development kit.

1. Run device provisioning script:
    ```
    python3 EdgeDeviceProvisioning/generate_prototype.py
    ```

2. In *EdgeDeviceProvisioning* directory, you should now see a *DeviceProfile* catalog with *WirelessDevice* subcatalog(s).  
   Each _WirelessDevice_ subcatalog represents a singe edge device.
   Personalisation data, in a form of a programmable binary, is available inside.  
   You should be able to flash it onto development kit using the flashing tools specific for your selected platform.


3. You can generate multiple devices by calling *generate_prototype.py* again or by using *--instances* parameter
    ```
    python3 EdgeDeviceProvisioning/generate_prototype.py --instances 5
    ```

### 5. Flash edge device

In this step you should program all the binaries onto your development kit.
Make sure to program:
- personalisation data from previous step (this loads serial number and authorization keys)
- application binary from *EdgeDeviceBinaries*

Programming devices depends on selected hardware platform. Please refer to platform vendor tools & documentation for details.

### 6. Enjoy the application

The edge device will transmit a welcome message to application server, thus information the application server of its presence.
After the edge device receives an acknowledgement from the application server, it will start sending periodical temperature measurement to the backend. Received data will be represented on the frontend UI.

You can open the terminal to the edge device to see the log flow (eg. data transfer happening periodically).   
You can open the URL to web application to see the graphical representation of your edge device in the UI.  
You can press buttons on the edge device and see the button state changes in the web UI.  
You can press LED button in the web UI and see that the LED on your edge device toggles.  
You can open the window in your room (or turn on the heating, upon preference) and observe how temperature readouts change in the web UI.

## Sensor Monitoring App

Sensor Monitoring Application consists of an AWS infrastructure, which is able to receive, process and store messages coming from a Sidewalk-enabled devices.  
It also provides a Web App, which allows user to interact with his development board.

### Cloud infrastructure

Components of the application are depicted by the diagram below. They are connected by arrows, which represent dataflow.
Color denotes message type:
- green --> uplink
- orange --> downlink
- blue --> notification
- red --> error
- black --> application-specific data

| ![Alt text](./ApplicationServerDeployment/doc/stack_diagram.png "Sample application - resources and dataflow") |
| --- |
| *Sample application - resources and dataflow* |

*SidewalkSampleApplicationStack* CloudFormation stack provides resources that handle messages coming from Sidewalk-enabled devices.  
It also creates necessary roles and permissions, not included on the diagram.
Its main components are:

- *SIDEWALK_DESTINATION* - maps a device message to an AWS IoT rule.
  Each Sidewalk device need to have its destination defined, so that AWS IoT knows where to redirect the message.
  You can change destination of your device using *UpdateDestination* method from the AWS IoT Wireless API.   
  All the uplink messages from the *SIDEWALK_DESTINATION* are redirected to the *SidewalkUplinkRule*.


- *SidewalkUplinkRule* - receives uplink messages from the *SIDEWALK_DESTINATION*.
  It forwards incoming uplinks to the *SidewalkUplinkLambda*, where they are further processed.
  In case of error, error messages are stored in the *SidewalkRuleError* log group.


- *SidewalkNotificationRule* - receives event notifications for Sidewalk resources.
  It forwards incoming notifications to the *SidewalkUplinkLambda*.
  In case of error, error messages are stored in the *SidewalkRuleError* log group.


- *SidewalkUplinkLambda* - processes incoming uplinks and notifications. Logs incoming events.
  Uplinks are decoded and, depending on the payload, following actions may be taken:
    - store device data in SidewalkDevices table
    - store sensor data in Measurements table
    - call *SidewalkDownlinkLambda* to respond with the downlink message


- *SidewalkDownlinkLambda* - handles request to send a command to the wireless device.
  Encodes the command to conform to the protocol of the embedded application.


- *SidewalkDbHandlerLambda* - handles requests to fetch data from the *SidewalkDevices* and *Measurements* tables.


- *SidewalkDevices* - stores state of the devices.


- *Measurements* - stores sensor data.


- *S3 Bucket* - hosts web application.


### Stack deployment

In order to deploy the application, run the *ApplicationServerDeployment/deploy_stack.py* script, which:
- creates CloudFormation stack
- configures settings, which cannot be set via CloudFormation

Before running the script, ensure that you have sufficient permissions to create resources listed in [SidewalkSampleApplicationStack.yaml](./ApplicationServerDeployment/template/SidewalkSampleApplicationStack.yaml)   
You can reuse following policy document (replace *<account_ID>* with your AWS Account ID): [DeployStackPolicy.json](./ApplicationServerDeployment/template/DeployStackPolicy.json)

```
python3 ApplicationServerDeployment/deploy_stack.py
```

|WARNING: You will be billed for the usage of AWS resources created by this application.|
|---|


In order to delete all the resources created by the application, run:
```
python3 ApplicationServerDeployment/delete_stack.py
```

### Created resources

| Resource Type | Console Location | Name
| --- | --- | --- |
| AWS::CloudFormation::Stack                        | CloudFormation -> Stacks                          | SidewalkSampleApplicationStack
| AWS::IoTWireless::Destination                     | AWS IoT -> Manage -> LPWAN devices -> Destinations| SensorAppDestination
| AWS::IoT::TopicRule                               | AWS IoT -> Message routing -> Rules               | SidewalkNotificationRule  SidewalkUplinkRule
| AWS::IoT::TopicRule                               | AWS IoT -> Message routing -> Rules               | SidewalkUplinkRule
| AWS::IoT::Policy                                  | AWS IoT -> Security -> Policies                   | SidewalkReceiveWirelessEventNotificationsPolicy
| AWS::Lambda::Function                             | Lambda -> Functions                               | SidewalkDbHandlerLambda
| AWS::Lambda::Function                             | Lambda -> Functions                               | SidewalkDownlinkLambda
| AWS::Lambda::Function                             | Lambda -> Functions                               | SidewalkUplinkLambda
| AWS::Lambda::Permission                           | Lambda -> Functions -> SidewalkDbHandlerLambda    | SidewalkDbHandlerLambdaPermissionsForApiGateway
| AWS::Lambda::Permission                           | Lambda -> Functions -> SidewalkDownlinkLambda     | SidewalkDownlinkLambdaPermissionsForApiGateway
| AWS::Lambda::Permission                           | Lambda -> Functions -> SidewalkUplinkLambda       | SidewalkUplinkLambdaPermissionsForNotifications
| AWS::Lambda::Permission                           | Lambda -> Functions -> SidewalkUplinkLambda       | SidewalkUplinkLambdaPermissionsForUplinks
| AWS::Logs::LogGroup                               | CloudWatch -> Log groups                          | SidewalkDbHandlerLambdaLogGroup
| AWS::Logs::LogGroup                               | CloudWatch -> Log groups                          | SidewalkDownlinkLambdaLogGroup
| AWS::Logs::LogGroup                               | CloudWatch -> Log groups                          | SidewalkRuleErrorsLogGroup
| AWS::Logs::LogGroup                               | CloudWatch -> Log groups                          | SidewalkUplinkLambdaLogGroup
| AWS::IAM::Role                                    | IAM -> Roles                                      | SidewalkDestinationRole
| AWS::IAM::Role                                    | IAM -> Roles                                      | SidewalkRuleRole
| AWS::IAM::Role                                    | IAM -> Roles                                      | SidewalkDbHandlerLambdaExecutionRole
| AWS::IAM::Role                                    | IAM -> Roles                                      | SidewalkDownlinkLambdaExecutionRole
| AWS::IAM::Role                                    | IAM -> Roles                                      | SidewalkUplinkLambdaExecutionRole
| AWS::DynamoDB::Table                              | DynamoDB -> Tables                                | SidewalkDevices
| AWS::Timestream::Database                         | Timestream -> Databases                           | SidewalkTimestream
| AWS::Timestream::Table                            | Timestream -> Databases -> SidewalkTimestream     | Measurements
| AWS::CloudFront::Distribution                     | CloudFront -> Distributions                       | CloudFrontDistribution
| AWS::CloudFront::CloudFrontOriginAccessIdentity   | CloudFront -> Origin access                       | CloudFrontOriginAccessIdentity
| AWS::ApiGateway::RestApi                          | API Gateway -> APIs -> sensor-monitoring-app      | SidewalkApiGateway
| AWS::ApiGateway::Resource                         | API Gateway -> APIs -> sensor-monitoring-app      | ApiResource
| AWS::ApiGateway::Resource                         | API Gateway -> APIs -> sensor-monitoring-app      | ProxyResource
| AWS::ApiGateway::Method                           | API Gateway -> APIs -> sensor-monitoring-app      | ApiOptionsMethod
| AWS::ApiGateway::Method                           | API Gateway -> APIs -> sensor-monitoring-app      | ApiPostMethod
| AWS::ApiGateway::Method                           | API Gateway -> APIs -> sensor-monitoring-app      | ProxyGetMethod
| AWS::ApiGateway::Method                           | API Gateway -> APIs -> sensor-monitoring-app      | ProxyOptionsMethod
| AWS::ApiGateway::Deployment                       | API Gateway -> APIs -> sensor-monitoring-app      | SidewalkApiGatewayDeployment
| AWS::S3::Bucket                                   | Amazon S3 -> Buckets                              | SidewalkWebAppBucket
| AWS::S3::BucketPolicy                             | Amazon S3 -> Buckets                              | S3BucketPolicy

### Web App

After the deployment, web application is available under the link stored in [config -> WEB_APP_URL](./config.yaml).

|WARNING: The web app is publicly available. Anyone who has the right URL can interact with your device. |
|---|

Device will appear in the web app, once embedded app sends a first uplink message.  
Web app displays device state as well as sensor data, collected in the previous hour.  
User can engage buttons on the edge device, which is also reflected in the web UI (uplink communication).  
User can also toggle LED buttons in the UI view, which triggers toggle LED request sent to the edge device (downlink communication).

| ![Alt text](./ApplicationServerDeployment/doc/web_app_device.png "Web App - device status") |
| --- |
| *Web App - device tile* |

## Security

The sample code; software libraries; command line tools; proofs of concept; templates; or other related technology (including any of the foregoing that are provided by our personnel) is provided to you as AWS Content under the AWS Customer Agreement, or the relevant written agreement between you and AWS (whichever applies). You should not use this AWS Content in your production accounts, or on production or other critical data. You are responsible for testing, securing, and optimizing the AWS Content, such as sample code, as appropriate for production grade use based on your specific quality control practices and standards. Deploying AWS Content may incur AWS charges for creating or using AWS chargeable resources, including but not limited to running Amazon Lambda instances or using Amazon Timestream storage.

See [CONTRIBUTING](./CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.