from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("organisations/", views.organisations, name="organisations"),
    path("organisations/<str:org>/", views.organisation, name="organisation"),
    path("organisations/<str:org>/resources/", views.organisation_resources, name="organisation_resources"),
    path("organisations/<str:org>/resources/<int:resource_id>/", views.organisation_resource, name="organisation_resource"),
    path("organisations/<str:org>/events/", views.organisation_events, name="organisation_events"),
    path("organisations/<str:org>/events/<int:event_id>/", views.organisation_event, name="organisation_event"),

    path("resources/", views.resources, name="resources"),
    path("resources/<int:resource_id>/", views.resource, name="resource"),

    path("events/", views.events, name="events"),
    path("events/<int:event_id>/", views.event, name="event"),

    path("locations/", views.locations, name="locations"),
    path("location/<int:location_id>/", views.location, name="location"),

    path("dashboard/", login_required(views.OrganisationListView.as_view()), name="dashboard"),
    path("dashboard/<str:org>/", views.dashboard_org, name="dashboard_org"),
    path("dashboard/<str:org>/events/", login_required(views.DashboardEventsView.as_view()), name="dashboard_events"),
    path("dashboard/<str:org>/events/new/", login_required(views.DashboardNewEventView.as_view()), name="new_dashboard_event"),
    path("dashboard/<str:org>/events/<int:event_id>/", login_required(views.DashboardEventView.as_view()), name="dashboard_event"),
    path("dashboard/<str:org>/resources/", login_required(views.DashboardResourcesView.as_view()), name="dashboard_resources"),
    path("dashboard/<str:org>/resources/new/", login_required(views.DashboardNewResourceView.as_view()), name="new_dashboard_resource"),
    path("dashboard/<str:org>/resources/<int:resource_id>/", login_required(views.DashboardResourceView.as_view()), name="dashboard_resource"),
]
