from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about/', view=views.get_about, name='get_about'),

    # path for contact us view
    path(route='contact/', view=views.get_contact, name='get_contact'),

    # path for registration
    path(route='register/', view=views.registration_request, name='registration'),

    # path for login
    path(route='login/', view=views.login_request, name='login'),

    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),
    path(route='state/<str:state>', view=views.get_dealerships, name='index'),
    path(route='id/<int:id>', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealership/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealership/review/<int:dealer_id>/', view=views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)