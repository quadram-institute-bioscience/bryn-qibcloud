
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
import settings

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=settings.AUTH_URL,
                                username=settings.AUTH_NAME,
                                password=settings.AUTH_PASSWORD,
				project_name=settings.TENANT_NAME)
sess = session.Session(auth=auth)

nova = client.Client(2, session=sess)

servers = nova.servers.list(detailed=True)
for s in servers:
	print s, nova.flavors.get(s.flavor['id'])

print nova.flavors.list()


