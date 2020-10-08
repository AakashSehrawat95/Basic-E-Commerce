from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from .models import User, listing, bid, comment


def index(request):
    return render(request, "auctions/index.html", {'listings': listing.objects.filter(activity='O')})

def inactive(request):
    return render(request, "auctions/inactive.html", {'listings': listing.objects.filter(activity='C')})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categoryList(request):
    return render(request, "auctions/categories.html")

def categories(request, category):
    catname = ''
    for listingItem in listing.objects.filter(category=category):
        catname = listingItem.get_category_display
        break

    return render(request, "auctions/category.html", {"listings": listing.objects.filter(category=category), 'catname':catname})

@login_required
def addToWatchlist(request, listing_id):
    current_user = User.objects.get(username=request.user.get_username())
    current_listing = listing.objects.get(pk = listing_id)
    current_listing.watchlist.add(current_user)
    return HttpResponseRedirect(reverse(listingItem, kwargs={'listing_id': listing_id}))

@login_required
def removeFromWatchlist(request, listing_id, where_to):
    current_user = User.objects.get(username=request.user.get_username())
    current_listing = listing.objects.get(pk = listing_id)
    current_listing.watchlist.remove(current_user)
    if where_to =="watchlist":
        return HttpResponseRedirect(reverse(watchlist))
    else:
        return HttpResponseRedirect(reverse(listingItem, kwargs={'listing_id': listing_id}))

    
@login_required
def watchlist(request):
    current_user = User.objects.get(username=request.user.get_username())
    return render(request, 'auctions/watchlist.html', {'watchlistItems': listing.objects.filter(watchlist=current_user)})

@login_required
def create_listing(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        price = float(request.POST['price'])
        try:
            image = request.FILES['image']
        except:
            image = None
        category = request.POST['category']
        current_user = User.objects.get(username=request.user.get_username())
        item = listing(name = name, desc = desc, created_by = current_user, starting_bid = price, image = image, category = category)
        item.save()
        return HttpResponseRedirect(reverse(index))

    return render(request, "auctions/create.html")

@login_required
def removeListing(request, listing_id):
    current_user = User.objects.get(username=request.user.get_username())
    current_listing = listing.objects.get(pk = listing_id)
    if current_listing.created_by == User.objects.get(username=request.user.get_username()):
        current_listing.delete()
        return HttpResponseRedirect(reverse(index))

    return HttpResponseRedirect(reverse(index))


def listingItem(request, listing_id):
    current_item = listing.objects.get(id=listing_id)
    bidMax = bid.objects.filter(listing=current_item).aggregate(Max('bid_price'))
    try:
        highestBid = bid.objects.get(listing=current_item, bid_price=bidMax['bid_price__max'])

    except (NameError, ObjectDoesNotExist) as e:
        highestBid = None

    try:
        if current_item.created_by == User.objects.get(username=request.user.get_username()):
            isCreator = True
        else:
            isCreator = False

        if User.objects.get(username=request.user.get_username()) in current_item.watchlist.all():
            isWatchlisted = True
        else:
            isWatchlisted = False

        context = {
            "listing": current_item, 
            "isCreator": isCreator, 
            "isWatchlisted": isWatchlisted, 
            "comments": comment.objects.filter(listing=current_item),
            "highestBid": highestBid
        }

        return render(request, "auctions/listing.html", context)

    except (NameError, ObjectDoesNotExist) as e:
        context = {
            "listing": current_item, 
            "comments": comment.objects.filter(listing=current_item),
            "highestBid": highestBid
        }
        return render(request, "auctions/listing.html", context)

@login_required
def makeComment(request, listing_id):
    if request.method == 'POST':
        commentText = request.POST['commentText']
        current_user = User.objects.get(username=request.user.get_username())
        current_item = listing.objects.get(id=listing_id)

        commentData = comment(user=current_user, listing = current_item, comment=commentText)
        try:
            commentData.save()
        except IntegrityError:
            comment.objects.filter(user=current_user, listing=current_item).update(comment=commentText)
        return HttpResponseRedirect(reverse(listingItem, kwargs={'listing_id': listing_id}))


@login_required
def makeBid(request, listing_id):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user.get_username())
        current_item = listing.objects.get(pk=listing_id)
        bidPrice = float(request.POST['bidPrice'])

        bidMax = bid.objects.filter(listing=current_item).aggregate(Max('bid_price'))
        try:
            highestBid = bid.objects.get(listing=current_item, bid_price=bidMax['bid_price__max'])
            
            if bidPrice == current_item.starting_bid or bidPrice == highestBid.bid_price:
                bidPrice += 0.01

        except (NameError, ObjectDoesNotExist) as e:
            highestBid = None  

            if bidPrice == current_item.starting_bid:
                bidPrice += 0.01

        new_bid = bid(user = current_user, listing=current_item, bid_price=bidPrice)

        try:
            new_bid.save()
        except IntegrityError:
            bid.objects.filter(user=current_user, listing=current_item).update(bid_price=bidPrice)

        return HttpResponseRedirect(reverse(listingItem,  kwargs={'listing_id': listing_id}))

@login_required
def closeBid(request, listing_id):
    listing.objects.filter(pk=listing_id).update(activity='C')
    return HttpResponseRedirect(reverse(listingItem,  kwargs={'listing_id': listing_id}))