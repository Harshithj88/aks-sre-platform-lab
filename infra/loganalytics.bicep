@description('Name of the Log Analytics workspace')
param workspaceName string

@description('Azure region for the Log Analytics workspace')
param location string

@description('Resource tags')
param tags object = {}

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: workspaceName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

output workspaceResourceId string = workspace.id
