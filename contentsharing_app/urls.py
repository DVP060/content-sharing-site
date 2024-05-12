from django.urls import path
import contentsharing_app.views as view

urlpatterns = [
    path('',view.index,name="home"),
    path('signup',view.signup,name="signup"),
    path('save/reader',view.saveSignup,name="save-signup"),
    path('get/reader',view.saveSignin,name="get-signin"),
    path('home',view.home,name="homepage"),
    path('dashboard',view.dashboard,name="dashboard"),
    path('logout',view.logout,name="logout"),
    path('get/start',view.gettingStarted,name="start"),
    path('about',view.about,name="about"),
    path('contact',view.contact,name="contact"),
    path('resource',view.resource,name="resource"),
    path('get/resource/<int:id>',view.singleResource,name="single-resource"),
    path('create/resource',view.createResource,name="create-resource"),
    path('save/resource',view.saveResource,name="save-resource"),
    path('edit/resource/<int:id>',view.editResource,name="edit-resource"),
    path('user/resources/get',view.user_resources,name="user_resources"),
    path('user/resource/delete/<int:id>',view.user_resource_delete,name="user_resource_delete"),
    path('user/resource/publish/<int:id>',view.user_resource_publish_request,name="user_resource_publish"),
    path('user/resource/unpublish/<int:id>',view.user_resource_unpublish_request,name="user_resource_unpublish_request")
]