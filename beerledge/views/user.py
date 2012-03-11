# User Stuff...
from pyramid.view import view_config

from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from beerledge.models import User


@view_config(route_name='signup',
             renderer='beerledge:templates/user/signup.pt')
def signup(request):
    signup_url = request.route_url('signup')
    referrer = request.url
    if referrer == signup_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    if 'form.submitted' in request.params:
        try:
            User.objects.get(username=request.params['username'])
        except User.DoesNotExist:
            if request.params['password'] == request.params['confirm_password']:
                user = User(username=request.params['username'])
                user.email = request.params['email']
                user.passhash = user.set_password(request.params['password'])
                user.save()
                request.session.flash(u'Successfully created new user.', 'success')
                headers = remember(request, user.username)
                return HTTPFound(location=came_from,
                                 headers=headers)
            else:
                request.session.flash(u'Passwords do not match.', 'error')
                return {'title': 'Signup - BeerLedge.com',
                        'came_from': came_from,
                        'logged_in': False}
        else:
            request.session.flash(u'Username exists, please chose another one', 'error')
            return {'title': 'Signup - BeerLedge.com',
                    'came_from': came_from,
                    'logged_in': False}
    return {'title': 'Signup - BeerLedge.com',
            'came_from': came_from,
            'logged_in': False}


@view_config(route_name='login',
             renderer='beerledge:templates/user/login.pt')
@view_config(context=HTTPForbidden,
             renderer='beerledge:templates/user/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    if 'form.submitted' in request.params:
        try:
            user = User.objects.get(username=request.params['username'])
        except User.DoesNotExist:
            request.session.flash(u'Password or Username is incorrect.', 'error')
            return {'title': 'Login - BeerLedge.com',
                    'came_from': came_from,
                    'logged_in': False}
        else:
            if not user.check_password(request.params['password']):
                request.session.flash(u'Password or Username is incorrect.', 'error')
                return {'title': 'Login - BeerLedge.com',
                        'came_from': came_from,
                        'logged_in': False}
            else:
                request.session.flash(u'You were Successfully logged in.', 'success')
                headers = remember(request, user.username)
                return HTTPFound(location=request.route_url('home'),
                                 headers=headers)
    return {'title': 'Login - BeerLedge.com',
            'came_from': came_from,
            'logged_in': False}


@view_config(route_name='logout',
             renderer='beerledge:templates/user/logout.pt')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


def add_user_views(config):
    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
