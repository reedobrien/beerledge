from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from beerledge.security import RootFactory, GroupFinder

from beerledge.views.main import add_main_views
from beerledge.views.admin import add_admin_views
from beerledge.views.user import add_user_views


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy(settings['secret'],
                                               callback=GroupFinder)
    default_session_factory = UnencryptedCookieSessionFactoryConfig(
                             settings['secret'])
    config = Configurator(root_factory=RootFactory,
                          authentication_policy=authn_policy,
                          authorization_policy=ACLAuthorizationPolicy(),
                          settings=settings,
                          session_factory=default_session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    config.include(add_main_views)
    config.include(add_admin_views, route_prefix='/admin')
    config.include(add_user_views)
    config.add_subscriber('beerledge.models.add_mongo',
                          'pyramid.events.NewRequest')

    return config.make_wsgi_app()
