{{/*
Common labels applied to all resources.
*/}}
{{- define "demo-api.labels" -}}
app: {{ .Release.Name }}
chart: {{ .Chart.Name }}-{{ .Chart.Version }}
release: {{ .Release.Name }}
managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels used in matchLabels and pod selectors.
*/}}
{{- define "demo-api.selectorLabels" -}}
app: {{ .Release.Name }}
{{- end }}
