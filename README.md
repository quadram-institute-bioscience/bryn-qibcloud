# bryn
The CLIMB management web interface

## setting up virtualenv

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

### Deploying updates

* Commit and push changes to repo
* ensure local settings files are present
* from `deploy_tools` dir on local machine: `fab deploy:host=ubuntu@bryn.climb.ac.uk`
