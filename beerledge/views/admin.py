# Admin Stuff...

from pyramid.view import view_config

from beerledge.models import User, Checkin


@view_config(route_name='admin_home',
             permission='admin',
             renderer='beerledge:templates/admin/main.pt')
def admin_home(request):
    """Home of Admin interface. Allows admin to get to list of checkins
    and list of users."""
    checkins = Checkin.objects.all().limit(5)
    users = User.objects.all().limit(5)
    return {'title': '**ADMIN** - BeerLedge.com',
            'users': users,
            'checkins': checkins,
            'logged_in': True}


@view_config(route_name='admin_checkins',
             permission='admin',
             renderer='beerledge:templates/admin/checkins.pt')
def admin_checkins(request):
    """Allows admin to get to list of checkins.."""
    checkins = Checkin.objects.all()
    return {'title': '**ADMIN** - Checkins - BeerLedge.com',
            'checkins': checkins,
            'logged_in': True}


@view_config(route_name='admin_users',
             permission='admin',
             renderer='beerledge:templates/admin/users.pt')
def admin_users(request):
    """Allows admin to get to list of users."""
    users = User.objects.all()
    return {'title': '**ADMIN** - Users - BeerLedge.com',
            'users': users,
            'logged_in': True}


@view_config(route_name='admin_user_delete',
             permission='admin',
             request_method='POST')
def admin_user_delete(request):
    return {}


@view_config(route_name='admin_checkin_delete',
             permission='admin',
             request_method='POST')
def admin_checkin_delete(request):
    return {}


def add_admin_views(config):
    config.add_route('admin_home', '')
    config.add_route('admin_checkins', '/checkins')
    config.add_route('admin_users', '/users')
    config.add_route('admin_user_delete', '/user/delete')
    config.add_route('admin_checkin_delete', '/checkin/delete')
