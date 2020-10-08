from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("removeListing/<int:listing_id>", views.removeListing, name="removeListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:listing_id>/<str:where_to>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("categoryList", views.categoryList, name="categoryList"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("listingItem/<int:listing_id>", views.listingItem, name="listingItem"),
    path("makeComment/<int:listing_id>", views.makeComment, name="makeComment"),
    path("makeBid/<int:listing_id>", views.makeBid, name="makeBid"),
    path("closeBid/<int:listing_id>", views.closeBid, name="closeBid"),
]
