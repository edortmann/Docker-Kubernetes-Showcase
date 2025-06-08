{{- define "translator.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{/* Return a stable base name:
      * chart == release  → use chart (single)
      * otherwise        → <chart>-<release>
*/}}
{{- define "translator.fullname" -}}
{{- if eq .Chart.Name .Release.Name }}
{{ .Chart.Name }}
{{- else }}
{{ printf "%s-%s" .Chart.Name .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end -}}
{{- end -}}

{{- define "translator.labels" -}}
app.kubernetes.io/name: {{ include "translator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
