{{/* Generate fullname */}}
{{- define "user-service.fullname" -}}
{{- printf "%s-%s" .Release.Name "user-service" | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "user-service.labels" -}}
app.kubernetes.io/name: {{ include "user-service.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: Helm
{{- end }}
