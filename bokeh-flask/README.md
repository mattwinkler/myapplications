
### Introduction

The purpose of this repository is to deploy a simple flask app onto AWS lambda and API Gateway. The app contains an interactive visualization of the iris dataset using the Bokeh library in Python. Deployment to AWS is handled by the `zappa` library. The intent of this is to get up and running quickly before moving on to more advanced scenarios. A good use is to deploy this app in order to understand the moving parts and dependencies, explore the AWS resources it creates, and then build up to handle additional use cases.   

### Prerequisites  

* Python3    
* Virtualenv: `pip install virtualenv` (zappa requires that )
* aws cli: `pip install awscli`  
* AWS credentials setup via `aws configure`  

### Installation & Setup

1) Once you have the above dependencies ready, clone this repository: `git clone <repository URL`. This will become the root level of your project.  
2) Next, run the following from the project's root directory to create a virtual environment within the root of the project: `python -m virtualenv env`. Feel free to choose an environment name other than 'env', this is just what I use as a default.  
3) Activate the newly-created virtual environment:  
  * Windows: `.\env\Scripts\activate`  
  * MacOS: `source activate env`  
4) Run `pip install -r requirements.txt` to get all of the requirements for this project installed to the virtual environment. Note that this uses bokeh version 0.12.5.  

### Deployment Resources  

* API Gateway  
* Lambda function with the project code  
* Cloudwatch monitoring on the lambda function  

### Deployment Instructions  

Run the following from the root directory of the project with the virtual environment active:  

1) `zappa init` - starts a prompt through which you can specify the AWS account profile and whether to deploy the app globally. I chose *not* to deploy globally, which requires an addtional bit of setup to specify the region in step 2. The prompts should look as follows:  

```
FULL OUTPUT TRUNCATED... 
What do you want to call this environment (default 'dev'):
What do you want call your bucket? (default ''):
Where is your app's function? (default 'app.init.app'):
Would you like to deploy this application globally? (default 'n') [y/n/(p)primary]:
Does this look okay? (default 'y') [y/n]:
```

This will create a file called `zappa_settings.json` in your project.  

2) I edited `zappa_settings.json` to include an additional key:value pair: `"aws_region": "us-east-2"`  

3) You should now be ready to deploy the app into AWS: `zappa deploy dev`. This assumes that you named the environment `dev` during step 1.  

Zappa will return the URL for the application running behind API Gateway.

4) When you make updates to the application source code, run `zappa update dev` and zappa will handle changes within AWS. 

### References
* Original source code repository: https://github.com/ecerami/pydata-essentials  
* Google groups discussion with changes to original code: https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/tmWtBCCIQyA  
* Link to `zappa` repository: https://github.com/Miserlou/Zappa  

