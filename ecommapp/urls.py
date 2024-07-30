from django.urls import path
from ecommapp import views 
from ecommapp.views import SampleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('about/',views.about),
    path('contact/<a>/<b>',views.contact),
    path('myview',views.SampleView.as_view()),
    # path('index/',views.index),
    path('about',views.about),
    path('cart',views.cart),
    path('contact',views.contact),
    path('index/',views.index),
    path('login',views.user_login),
    path('order',views.place_order),
    path('detail/<pid>',views.product_detail),
    path('reg',views.reg),
    path('catfilter/<cv>', views.catfilter),
    path('sort/<sv>', views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('payment',views.makepayment),
    path('sendemail',views.sendemail)
    

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)