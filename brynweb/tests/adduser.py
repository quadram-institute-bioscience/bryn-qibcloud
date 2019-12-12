from django.test import Client
import yaml

c = Client()

a = yaml.load(open('tests/exampleuserdata.yaml'))
response = c.post('/user/register/', a)

print(response)
