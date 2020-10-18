# Python Package manager 

## About The Project 

Create's pipenv config files to create a consistent python environment which can be used in CI/CD workflows. 

The thought here is to use service definitions to create ```Pipfile``` and ```Pipfile.lock```. These files can be used to create a consistent environment for Python applications using ```pipenv install --deploy``` and ```pipenv install --system --deploy``` in case of dockerized applications.
.Service definitions have all the parameters to create unique Pipfiles for a given service. 

## Getting Started 

### Prerequisites 
We need Python3 and pipenv installed for using the code to generate the Pipfiles.
You can check python and pipenv by using the following commands. 
```
$ python3 --version 
Python 3.8.5 

$ pip3 list | grep pipenv 
pipenv                 2020.8.13
```

### Installation 
1. Clone the repository and switch to the py-package-deployer directory.
```
$ git clone https://github.com/kaushalringle/py-package-deployer.git

$ cd py-package-deployer
```

2. Check the Usage.
```
python3 ppdeployer.py -h
```

## Usage and Examples 
Now you can define any new service in ```service_definitions.py``` or you can use the services already decalared to test. To add a new service, add a new blob under services with the parameter's you need and run the python script for that service.

Packages can be either the package name or the git repository link. 
GIT packages can be installed using GIT urls that follow the url format.
```
<vcs_type>+<scheme>://<location>/<user_or_organization>/<repository>@<branch_or_tag>#egg=<package_name>
```
more information is available [here](https://pipenv.pypa.io/en/latest/basics/#a-note-about-vcs-dependencies).


for e.g. SERVICE_B in the service_definitions file has both git url and package name. 
```
"requests": "{ git = 'https://github.com/requests/requests.git', editable = 'true', ref = 'v2.20.1' }","boto3": "<=1.16,>=1.15"
```



Let's use the Service definition for SERVICE_A. Lets say you have a service which is running an applciation which needs some packages on the system to run. for eg boto3.  For dependency resolution we will specify a range so pip can check for dependancy conflicts. Here we have given "boto3": "<=1.16,>=1.15". 

```
ppdeployer.py -s service_a
```
The above command will create ```Pipfile``` and ```Pipfile.lock``` under the directory of the service name which can be checked into the repository along with your code which can be used by CI/CD workflows to consistently create the same python environment.  

Use the the command given below to recreate the environment for your service.

```
pipenv install --deploy
```

you can try this by recreating the environment for service_a
```
$ cd service_a/
$ pipenv install --deploy
$ pipenv graph 
$ pipenv run pip list
```

Similarly you can create your own service configurations by adding new service definitions to ```service_definitions.py``` .