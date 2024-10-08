from gooddata_sdk import GoodDataSdk, CatalogWorkspace

# GoodData host in the form of uri eg. ""
host = "https://scholarly-emu.trial.cloud.gooddata.com"
# GoodData API token
token = "Y2M5ZDk2OTUtMTY5Zi00OTNkLWI3MDMtZGFiZTQ5NWVkNDU4OkFQSV9Ub2tlbjp2THhVRjJHNVJQcWQ4dG4xNU1Zb2VmM0Y3bkNsTXhlQQ=="
demo_workspace_id = "9fa384e3a6e143d68d64f0af37f82f7a"
production_workspace_id = "553814ecf30f4c84a95cd34c5112cc0b"

sdk = GoodDataSdk.create(host, token)

# Create workspace
sdk.catalog_workspace.create_or_update(
  CatalogWorkspace(production_workspace_id, "Prod")
)

# Get LDM (Logical Data Model) from demo workspace
declarative_ldm = sdk.catalog_workspace_content.get_declarative_ldm(
  demo_workspace_id
)

# Get analytics model (metrics, dashboards, etc.) from Demo workspace
demo_declarative_analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model(
  demo_workspace_id
)

# Get analytics model (metrics, dashboards, etc.) from Prod workspace
prod_declarative_analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model(
  production_workspace_id
)

demoDashboards = demo_declarative_analytics_model.analytics.analytical_dashboards
prodDashboards = prod_declarative_analytics_model.analytics.analytical_dashboards


demoDashboardIds = set()
for demoDashboard in demoDashboards:
  demoDashboardIds.add(demoDashboard.id)

for prodDashboard in prodDashboards:
  if prodDashboard.id not in demoDashboardIds:
    demoDashboards.append(prodDashboard)

demoFilterContextIds = set()
for demoFilterContext in demo_declarative_analytics_model.analytics.filter_contexts:
    demoFilterContextIds.add(demoFilterContext.id)

for prodFilterContext in prod_declarative_analytics_model.analytics.filter_contexts:
    if prodFilterContext.id not in demoFilterContextIds:
        demo_declarative_analytics_model.analytics.filter_contexts.append(prodFilterContext)



# Put LDM (Logical Data Model) to production workspace
sdk.catalog_workspace_content.put_declarative_ldm(
  production_workspace_id,
  declarative_ldm
)



# Put analytics model (metrics, dashboards, etc.) to production workspace
sdk.catalog_workspace_content.put_declarative_analytics_model(
  production_workspace_id,
  demo_declarative_analytics_model
)
