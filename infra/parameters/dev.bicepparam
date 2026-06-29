using '../main.bicep'

param environment = 'dev'
param location = 'eastus'
param projectName = 'sre-platform'
param kubernetesVersion = ''
param nodeCount = 1
param nodeVmSize = 'Standard_B2s'
