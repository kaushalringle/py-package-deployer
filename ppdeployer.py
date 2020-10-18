#!/usr/bin/python3

import argparse
import logging 
import os 
import subprocess
import sys
import service_definitions


class pythonPackageDeployer:

    def __init__(
        self,
        args
    ):
        
        self.service_name = args.service_name.upper()
    
        try :
            self.service_definition = service_definitions.SERVICES[self.service_name]
            self.python_interpreter_version = self.service_definition["REQUIRES"]["python_version"]
            self.source_name = self.service_definition["SOURCE"]["name"]
            self.source_url = self.service_definition["SOURCE"]["url"]
        
        except KeyError:
            logging.error("Service definition not found for service: {}".format(self.service_name))
            raise    

        self.pip_config = ""
            

    def check_python(self):
        """
        Ckeck if the python interpreter is available. 
        """

        py_verison = '{0[0]}.{0[1]}'.format(sys.version_info)
    
        if self.python_interpreter_version != py_verison:
            logging.error(
                "Python version {} not found.".format(
                    self.python_interpreter_version
                )
            )


    def create_pip_config(self):
        """
        Create the Pipfile config which is later used for creating Pipfile for the service.
        """

        packages = ""
        dev_packages = ""

        for name, version_details in self.service_definition.get("DEV-PACKAGES").items():

            if version_details.find("git") > 0:
                dev_packages += """{} = {} \n""".format(
                    str(name), 
                    str(version_details)
                    )

            else:
                dev_packages += """{} = \"{}\" \n""".format(
                    str(name), 
                    str(version_details)
                    )

        for name, version_details in self.service_definition.get("PACKAGES").items():

            if version_details.find("git") > 0:
                packages += """{} = {} \n""".format(
                    str(name),
                    str(version_details)
                    )

            else:
                packages += """{} = \"{}\" \n""".format(
                    str(name),
                    str(version_details)
                    )

        self.pip_config = """
[[source]]
name = "{}"
url = "{}"
verify_ssl = true

[dev-packages]
{}

[packages]
{}

[requires]
python_version = "{}" 
        """.format(
            self.source_name,
            self.source_url,
            dev_packages,
            packages,
            self.python_interpreter_version
        )


    def create_pipfile(self):
        """
        Create the Pipfile for the service.
        """

        path = "./{}".format(self.service_name.casefold())

        if not os.path.exists(path):
                os.makedirs(path)

        with open(os.path.join(path, "Pipfile"), 'w') as fp:
            logging.info(
                "Creating Pipfile for Service: {}, Creating file: {}".format(
                    self.service_name, 
                    path + "/Pipfile")
            )
            fp.write(self.pip_config)


    def deploy_pipfile(self):
        """
        Deploy the Pipfile to to test creation of envronment for the service. 

        'pipenv install --deploy' will only deploy if Pipfile and Pipfile.lock are in sync. 
        this will ensure consistent environment creation for applications run in the service.   

        Pipfile and Pipfile.lock should be checked into the repository and should be used 
        by the CI/CD systems to deploy application for the service.   

        """

        service_working_dir = "./{}/".format(self.service_name.casefold())

        pipenv_deploy_cmd = ["pipenv", "install", "--deploy"]
        pipenv_cleanup_cmd = ["pipenv", "--rm"]
        pipenv_graph_cmd = ["pipenv", "graph"]
        
        pipenv_deploy = subprocess.Popen(
            pipenv_deploy_cmd, 
            cwd=service_working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
            
        (output, error) = pipenv_deploy.communicate()

        if pipenv_deploy.returncode == 0:
            logging.info(output.decode('utf-8'))
            logging.info(
                "pipenv install is sucessfull Pipfile and Pipfile.lock can be checked into the repo for service {}".format(
                    self.service_name.casefold()
                    )
            )

            logging.info("Checking pipenv dependency graph..")
            pipenv_graph = subprocess.Popen(
                pipenv_graph_cmd, 
                cwd=service_working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            (g_output, g_error) = pipenv_graph.communicate()   

            if pipenv_graph.returncode == 0:
                logging.info(g_output.decode('utf-8'))
            else:
                logging.error(g_error.decode('utf-8'))

        else: 
            logging.error(
                "pipenv creation failed with error {}".format(
                    error.decode('utf-8')
                    )
            )

        logging.info("Cleaning up pipenv..")
        pipenv_cleanup = subprocess.Popen(
            pipenv_cleanup_cmd, 
            cwd=service_working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if pipenv_cleanup.returncode == 0:
            logging.info("Cleanup complete.")     

           
def logging_config(loglevel):
    """
    Log configuration.
    """

    logging.basicConfig(
        datefmt = r'%b %d %H:%M:%S %Y %Z',
        format = '%(asctime)s %(levelname)s:%(message)s',
        level = getattr( logging, loglevel.upper())
    )

    return logging.getLogger()


def get_arguments():
    """
    Definition of the arguments.

    """

    parser = argparse.ArgumentParser(
        description = """
        Python Package Deployer, 
        Use this tool to create deployment environments for services using Pipfile and Pipfile.lock created by this tool.
        Service definitions are declared in service_definitions.py
        """
    )    
    
    parser.add_argument(
        "-l",
        "--loglevel",
        help = "Loglevel for logs",
        default = "info",
        choices = ["info", "error", "debug"]
    )

    parser.add_argument(
        "-s",
        "--service-name",
        help = "Name of the service.",
        required = True,
    )

    arguments = parser.parse_args()

    return arguments 


def main():

    args = get_arguments()
    logging_config(args.loglevel)

    class_obj = pythonPackageDeployer(args)

    class_obj.check_python()

    class_obj.create_pip_config()

    class_obj.create_pipfile()

    class_obj.deploy_pipfile()


if __name__ == "__main__":
    main()