# Serverless Notes App

This is a simple Notes application built using the Serverless framework, Python, and AWS services such as DynamoDB and Cognito User Pool.

## Prerequisites

Before you can deploy this application, you need to have the following:

- [Node.js and NPM](https://nodejs.org/en/download/)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
- AWS credentials with administrative permissions

## Installation

To deploy the application, follow these steps:

1. Clone the repository:
    git clone https://github.com/your-username/serverless-notes-app.git
    cd serverless-notes-app

2. Install the dependencies:
    npm install

3. Deploy the application:
    sls deploy


This will create the required AWS resources, such as the DynamoDB table and Cognito User Pool, and deploy the Lambda functions.

## Usage

To use the application, you need to create a user in the Cognito User Pool.

1. Go to the AWS Cognito Console, select the User Pool created by the deployment, and click on "Users and groups".
2. Click on "Create user" and fill in the required details.
3. After creating the user, note down the `Username` value.

You can now use any API client or the provided front-end application to interact with the Notes API. The endpoints are secured with Cognito User Pool, so you need to obtain a valid access token to access the API.

### Obtaining an Access Token

To obtain an access token, follow these steps:

1. Go to the AWS Cognito Console, select the User Pool created by the deployment, and click on "App clients".
2. Note down the `App client id` value for the client created by the deployment.
3. Go to the "Domain name" section of the User Pool console and note down the `Domain` value.
4. Use the `Username` and `Password` of the user created earlier to authenticate and obtain an access token



### Working on the Front-end Application



