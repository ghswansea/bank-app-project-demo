{{- define "bank-app.name" -}}
{{- default .Chart.Name .Values.nameOverride }}
{{- end -}}

{{- define "bank-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end -}}

{{- define "bank-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride }}
{{- else }}
{{- printf "%s-%s" (include "bank-app.name" .) .Release.Name }}
{{- end }}
{{- end -}}
