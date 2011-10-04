# Create your views here.
import models
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext

def home(request):
    # Pulls variables from MySQL DB
    county = models.County.objects.all()
    zip_code = models.Zip_Code.objects.all()
    city = models.City.objects.all()
    # initial (initial render when opening the page)
    initial = True
    # zsuccess (a successful query on a zip code)
    zsuccess = False
    # csuccess (a successful query on a county name)
    csuccess = False
    # errors (errors to return on an invalid query)
    errors = []
    # begin logic on POST request
    if request.method == "POST":
        qz = request.POST.get('zip_search')
        #---------------------------------
        # Logic is as follows
        # Check to see if anything is entered in zip code
        # Check to see if zip code is a 5 digit number
        # If the zip code is 5 characters, then perform query on zip codes
        # Check to see if anything is entered on county
        # Pull characters on county and check against all county names
        #--------------------------------
        # Check to see if anything is entered in the zip code
        if not request.POST.get('zip_search', ''):
            errors.append('Enter a zip code.')
        # Check to see if zip code is a 5 digit number
        elif len(qz) != 5:
            errors.append('Please enter a valid 5 digit zip.')
        # If the zip code is 5 characters, then perform a query on zip codes
        if len(qz) == 5:
            zip_query = models.Zip_Code.objects.filter(zip_code__icontains=qz)
            initial = False
            zsuccess = True
            zip_search = request.POST.get('zip_search')
            response_dict = {'zip_query':zip_query, 'zsuccess':zsuccess,
                    'initial':initial, 'csuccess':csuccess,
                    'zip_search':zip_search, 'zip_code':zip_code}
            return render_to_response('taxapp/home.html', response_dict,
                    context_instance=RequestContext(request))
        # Check to see if anything is entered on county
        if not request.POST.get('county_search', ''):
            errors.append('Please enter a county.')
        # Pull characters on county and check against all county names
        else:
            qc = request.POST.get('county_search')
            county_query = models.County.objects.filter(name__icontains=qc)
            initial = False
            csuccess = True
            county_search = request.POST.get('county_search')
            response_dict = {'county_query':county_query, 'csuccess':csuccess,
                    'initial':initial, 'zsuccess':zsuccess,
                    'county_search':county_search}
            return render_to_response('taxapp/home.html', response_dict,
                    context_instance=RequestContext(request))
        
    response_dict = {'county':county,
            'zip_code':zip_code, 'city':city,
            'errors':errors,'initial':initial,
            'csuccess':csuccess, 'zsuccess':zsuccess}
    return render_to_response('taxapp/home.html', response_dict,
            context_instance=RequestContext(request))

def get_county(request, county_name=None):
    if county_name is None:
        return HttpResponse('No County Provided')
    county_object = models.County.objects.filter(name__icontains=county_name)[0]
    tax_rate = county_object.tax_rate
    return HttpResponse(tax_rate) 
