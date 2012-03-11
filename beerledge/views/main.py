import foursquare

from pyramid.view import view_config

from pyramid.security import authenticated_userid

from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from beerledge.models import Checkin

CLIENT_ID = 'VFRAJY1MTMMI2TP4DKUCZOCL2RWRPBHTSURDZH02XGF5Z442'
CLIENT_SECRET = '4CQIUC5HZJFCP5NV5NCU3CAAHU5ENKEBXKIHOISF0OMCM2LT'


def get_locations(lat, lon):
    latlon = '%s,%s' % (lat, lon)
    client = foursquare.Foursquare(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET)
    return client.venues.search(params={'ll': latlon, 'limit': 50})


@view_config(route_name='home',
             renderer='beerledge:templates/main.pt')
def index(request):
    logged_in = authenticated_userid(request)
    return {'title': 'BeerLedge.com',
            'logged_in': logged_in}


@view_config(route_name='about',
             renderer='beerledge:templates/about.pt')
def about(request):
    logged_in = authenticated_userid(request)
    return {'title': 'About - BeerLedge.com',
            'logged_in': logged_in}


@view_config(route_name='contact',
             renderer='beerledge:templates/contact.pt')
def contact(request):
    logged_in = authenticated_userid(request)
    return {'title': 'Contact - BeerLedge.com',
            'logged_in': logged_in}


@view_config(route_name='checkin',
             renderer='beerledge:templates/checkin.pt',
             permission='edit')
def checkin(request):
    logged_in = authenticated_userid(request)
    lat = request.params['lat']
    lon = request.params['lon']
    results = get_locations(lat, lon)
    return {'title': 'Checkin - BeerLedge.com',
            "results": results,
            'logged_in': logged_in}


@view_config(route_name='log_beer',
             request_method='POST')
def log_beer(request):
    checkin = Checkin(beer=request.params['beer'],
                      checkin_place=request.params['place'],
                      username=request.params['username'])
    checkin.save()
    request.session.flash(u'Successfully logged your beer.', 'success')
    return HTTPFound(location=request.route_url('home'))


def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    return HTTPFound(request.route_url('login'))


def add_main_views(config):
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('contact', '/contact')
    config.add_route('checkin', '/checkin')
    config.add_route('log_beer', '/log')
