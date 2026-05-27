from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Pages 
    path('',                           views.home_view,        name='home'),
    path('units/',                     views.units_view,       name='units'),
    path('units/add/',                 views.unit_add_view,    name='unit_add'),
    path('units/<str:unit_id>/',       views.unit_detail_view, name='unit_detail'),
    path('units/<str:unit_id>/edit/',  views.unit_edit_view,   name='unit_edit'),
    path('units/<str:unit_id>/delete/',views.unit_delete_view, name='unit_delete'),
    path('monitor/',                   views.monitor_view,     name='monitor'),
    path('chatbot/',                   views.chatbot_view,     name='chatbot'),
    path('analytics/',                 views.analytics_view,   name='analytics'),
    path('history/',                   views.history_view,     name='history'),
    path('settings/',                  views.settings_view,    name='settings'),
    path('approvals/',                 views.approvals_view,   name='approvals'),

    # JSON API 
    path('api/telemetry/',                         views.api_telemetry,      name='api_telemetry'),
    path('api/units/<str:unit_id>/command/',        views.api_command,        name='api_command'),
    path('api/units/<str:unit_id>/profile/',        views.api_profile_save,   name='api_profile'),
    path('api/units/<str:unit_id>/history/',        views.api_history,        name='api_history'),
    path('api/analytics/history-table/',           views.api_history_table,  name='api_history_table'),
    path('api/chat/',                              views.api_chat,           name='api_chat'),
    path('api/ollama/models/',                     views.api_ollama_models,  name='api_ollama_models'),
    path('api/mqtt-log/',                          views.api_mqtt_log,       name='api_mqtt_log'),
    path('api/pending-requests/',                  views.api_pending_requests, name='api_pending_requests'),
    path('api/pending-requests/<int:req_id>/approve/', views.api_approve_request, name='api_approve_request'),
    path('api/pending-requests/<int:req_id>/reject/', views.api_reject_request, name='api_reject_request'),
    path('api/co-sensors/',                        views.api_get_sensors,    name='api_get_sensors'),
    path('api/co-sensors/update/',                 views.api_update_sensors, name='api_update_sensors'),

    # MQTT Client API 
    path('api/mqtt/status/',       views.api_mqtt_status,      name='api_mqtt_status'),
    path('api/mqtt/reconnect/',    views.api_mqtt_reconnect,   name='api_mqtt_reconnect'),
    path('api/mqtt/disconnect/',   views.api_mqtt_disconnect,  name='api_mqtt_disconnect'),
    path('api/mqtt/publish/',      views.api_mqtt_publish,     name='api_mqtt_publish'),

    # Performance Monitor API 
    path('api/perf/toggle/',       views.api_perf_toggle,      name='api_perf_toggle'),
    path('api/perf/status/',       views.api_perf_status,      name='api_perf_status'),
]
