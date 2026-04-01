from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Cart, CartItem
from accounts.models import Customer
from catalog.models import StockBook

# Create your views here.
