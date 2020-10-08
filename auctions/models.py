from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import datetime


class User(AbstractUser):
    pass

    def __str__(self):
            return f"{self.username} [{self.email}]"

class listing(models.Model):

    CATEGORIES = [
        ('C', 'Clothing & Footwear'),
        ('H', 'Hardware and Electronics'),
        ('F', 'Furniture & Furnishings'),
        ('T', 'Toys'),
        ('D', 'Decorations'),
        ('K', 'Kitchenware'),
        ('E', 'Electrical Appliances'),
        ('O','Others'),
        ('TO', 'Toiletries')
    ]

    OPEN_OR_CLOSE = [
        ('O','Open'),
        ('C','Closed')
    ]

    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_made")
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="listings", null=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    watchlist = models.ManyToManyField(User, blank=True, related_name = "watchlist")
    activity = models.CharField(max_length=1, default='O', choices=OPEN_OR_CLOSE)

    def __str__(self):
        return f"{self.name} (${self.starting_bid})" 

class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} bid {self.bid_price} on {self.listing.name})" 



class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.listing.name} [{self.date}]" 


    
