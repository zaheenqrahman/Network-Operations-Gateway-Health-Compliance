import meraki

API_KEY = "c13b59c1e0eedcee931b7b9cb42c0fa6d1c5a4a5"
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