## Definitions for services
## Services defined here will be used for creating Pipfiles for service deployment.  
#  GIT packages can be installed using GIT urls that follow the given convention
#  <vcs_type>+<scheme>://<location>/<user_or_organization>/<repository>@<branch_or_tag>#egg=<package_name>
#  reference https://pipenv.pypa.io/en/latest/basics/#a-note-about-vcs-dependencies 


SERVICES = {

"SERVICE_A": {
    "SOURCE": {
        "name": "pypi",
        "url": "https://pypi.org/simple",
        "verify_ssl": "true"
    }, 
    "DEV-PACKAGES": {
        # "name": "version details"
    },
    "PACKAGES": {
        "boto3": "<=1.16,>=1.15"
    },
    "REQUIRES": {
        "python_version": "3.8"
    }
    
},

"SERVICE_B": {
    "SOURCE": {
        "name": "pypi",
        "url": "https://pypi.org/simple",
        "verify_ssl": "true"        
    }, 
    "DEV-PACKAGES": {
        # "name": "version"        
    },
    "PACKAGES": {
        "requests": "{ git = 'https://github.com/requests/requests.git', editable = 'true', ref = 'v2.20.1' }",
        "boto3": "<=1.16,>=1.15"
    },
    "REQUIRES": {
        "python_version": "3.8"
    }
}


}


