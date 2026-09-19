import meraki

API_KEY = "977b24744ba4fbe1bff8c6bd048b632bd692d967"
dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

orgs = dashboard.organizations.getOrganizations()
print("Your organizations:")
for org in orgs:
    print(f"  {org['id']} — {org['name']}")

for org in orgs:
    print(f"\nTrying devices for org {org['id']} ({org['name']}):")
    try:
        devices = dashboard.organizations.getOrganizationDevices(org['id'])
        print(devices)
    except Exception as e:
        print(f"Failed: {e}")