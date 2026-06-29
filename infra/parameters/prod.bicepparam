using '../main.bicep'

param environment = 'prod'
param location = 'eastus'
param projectName = 'sre-platform'
param kubernetesVersion = ''
param nodeCount = 3
param nodeVmSize = 'Standard_D2s_v3'
