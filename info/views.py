from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import models
from . import forms

class IndexView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/dashboard_event.html"

    def get(self, request):
        return render(request, "info/index.html", {})

    def post(self, request):
        query = request.POST['search']
        orgs = models.Organisation.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        events = models.Event.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        resources = models.Resource.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

        return render(
            request,
            "info/index.html",
            {
                "results": [*orgs, *events, *resources],
            }
        )

def organisations(request):
    return render(request, "info/organisations.html", {"orgs": models.Organisation.objects.all()})

def organisation(request, org):
    return render(request, "info/organisation.html", {"org": get_object_or_404(models.Organisation, slug=org)})

def organisation_resources(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    resources = models.Resource.objects.filter(organisation=org)
    return render(request, "info/organisation_resources.html", {"org": org, "resources": resources})

def organisation_resource(request, org, resource_id):
    org = get_object_or_404(models.Organisation, slug=org)
    resource = models.Resource.objects.get(pk=resource_id, organisation=org)
    return render(request, "info/organisation_resource.html", {"org": org, "resource": resource})

def organisation_events(request, org):
    org = get_object_or_404(models.Organisation, slug=org)
    events = models.Event.objects.filter(organisation=org)
    return render(request, "info/organisation_events.html", {"org": org, "events": events})

def organisation_event(request, org, event_id):
    org = get_object_or_404(models.Organisation, slug=org)
    event = models.Event.objects.get(pk=event_id, organisation=org)
    return render(request, "info/organisation_event.html", {"org": org, "event": event})

def resources(request):
    resources = models.Resource.objects.all()
    return render(request, "info/resources.html", {"resources": resources})

def resource(request, resource_id):
    resource = get_object_or_404(models.Resource, pk=resource_id)
    return render(request, "info/resource.html", {"resource": resource})

def events(request):
    events = models.Event.objects.all()
    return render(request, "info/events.html", {"events": events})

def event(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    return render(request, "info/event.html", {"event": event})

def locations(request):
    locations = models.Location.objects.all()
    return render(request, "info/locations.html", {"locations": locations})

def location(request, location_id):
    location = models.Location.objects.get(pk=location_id)
    return render(request, "info/location.html", {"location": location})

class OrganisationListView(ListView):
    model = models.Organisation
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def dashboard_org(request, org):
    org = get_object_or_404(models.Organisation, slug=org)

    return render(
        request,
        "info/dashboard_org.html",
        {
            "org": org,
            "form": forms.OrgForm(instance=org),
            "resources": models.Resource.objects.filter(organisation=org),
            "events": models.Event.objects.filter(organisation=org),
        },
    )

class DashboardEventsView(ListView):
    model = models.Event
    context_object_name = "events"
    form_class = forms.Event
    template_name = "info/dashboard_events.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["events"] = models.Event.objects.filter(organisation=context["org"])

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))


class DashboardEventView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/dashboard_event.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["event"] = get_object_or_404(models.Event, id=kwargs["event_id"])
        context["form"] = self.form_class(instance=context["event"])

        return context

    def get(self, request, org, event_id):
        return self.render_to_response(self.get_context_data(org=org, event_id=event_id))

    def delete(self, request, org, event_id):
        event = get_object_or_404(models.Event, id=event_id)
        event.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "event": event.name,
        })

    def post(self, request, org, event_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, event_id=event_id)
            context["event"].name = form.cleaned_data["name"]
            context["event"].description = form.cleaned_data["description"]
            context["event"].location = form.cleaned_data["location"]
            context["event"].date_time = form.cleaned_data["date_time"]
            context["event"].price = form.cleaned_data["price"]
            context["event"].save()

        return self.render_to_response(self.get_context_data(org=org, event_id=event_id))


class DashboardResourcesView(ListView):
    model = models.Resource
    form_class = forms.Resource
    template_name = "info/dashboard_resources.html"
    object_list = []

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["resources"] = models.Resource.objects.filter(organisation=context["org"])

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))


class DashboardResourceView(TemplateView):
    form_class = forms.ResourceForm
    template_name = "info/dashboard_resource.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["resource"] = get_object_or_404(models.Resource, id=kwargs["resource_id"])
        context["form"] = self.form_class(instance=context["resource"])

        return context

    def get(self, request, org, resource_id):
        return self.render_to_response(self.get_context_data(org=org, resource_id=resource_id))

    def delete(self, request, org, resource_id):
        resource = get_object_or_404(models.Resource, id=resource_id)
        resource.delete()

        return JsonResponse({
            "org": get_object_or_404(models.Organisation, slug=org).name,
            "resource": resource.name,
        })

    def post(self, request, org, resource_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            context = self.get_context_data(org=org, resource_id=resource_id)
            context["resource"].name = form.cleaned_data["name"]
            context["resource"].description = form.cleaned_data["description"]
            context["resource"].save()

        return self.render_to_response(self.get_context_data(org=org, resource_id=resource_id))

class DashboardNewResourceView(TemplateView):
    form_class = forms.ResourceForm
    template_name = "info/new_resource.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))

    def post(self, request, org):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = models.Resource.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                organisation=get_object_or_404(models.Organisation, slug=org),
            )

        return redirect(obj)

class DashboardNewEventView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/new_event.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["org"] = get_object_or_404(models.Organisation, slug=kwargs["org"])
        context["form"] = self.form_class()

        return context

    def get(self, request, org):
        return self.render_to_response(self.get_context_data(org=org))

    def post(self, request, org):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = models.Event.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                location=form.cleaned_data["location"],
                date_time=form.cleaned_data["date_time"],
                price=form.cleaned_data["price"],
                organisation=get_object_or_404(models.Organisation, slug=org),
            )

        return redirect(obj)
