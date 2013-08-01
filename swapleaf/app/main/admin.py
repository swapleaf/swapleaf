from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from swapleaf.app.main.models import UserProfile, Institution, Book, BookTransaction
from swapleaf.app.main.models import Offer, Course, Notify, Message
from swapleaf.app.account.models import SwapLeafEmailAddress, SwapLeafEmailConfirmation

########################################
#                                      #
#      DEFINE CLASS ADMIN AREA         #
#                                      #
########################################
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user','zip_code','partner_status','school']

class InstitutionAdmin(admin.ModelAdmin):
	list_display = ['id','name','city','state']
	search_fields = ['id','name','city','state']

class SwapLeafEmailAddressAdmin(admin.ModelAdmin):
	list_display = ['user','email','verified','primary']

class SwapLeafEmailConfirmationAdmin(admin.ModelAdmin):
	list_display = ['email_address','sent','confirmation_key']

class BookAdmin(admin.ModelAdmin):
	#list_display = ['title','isbn10','isbn13','author','rating','publish_date','cover_image']
	list_display = ['title','isbn10','isbn13','author','edition']

# class BookBuyingAdmin(admin.ModelAdmin):
# 	list_display = [ 'transaction_id','book','buyer','transaction_partner', 
#     				 'transaction_type','price','transaction_time','post_time'] 

class BookTransactionAdmin(admin.ModelAdmin):
	list_display = ['transaction_id','seller','buyer','book','price','course',
    				'condition','status','transaction_time','transaction_type','post_time']

# class BookTradingAdmin(admin.ModelAdmin):
# 	list_display = ['transaction_id','trader1','book_trade1','book_condition1',
#     				'price_book1','trader2','book_trade2','book_condition2','price_book2',
#     				'status','transaction_time','post_time']

# class BookTradingGivingAdmin(admin.ModelAdmin):
# 	list_display = ['transaction_id','trader1_giver','trader2_receiver','book1','book2','condition1','condition2',
#     				'status','transaction_time','post_time']

class CourseAdmin(admin.ModelAdmin):
	list_display = ['institution','course_number']

class NotifyAdmin(admin.ModelAdmin):
	list_display = ['pk','notify_type','content','notify_to','notify_from','date','status','object_id']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['receiver','sender', 'content','content_html','date']

class OfferAdmin(admin.ModelAdmin):
	list_display = ['id','user_offer','user_receive','transaction_time','view_status','offer_time']

########################################
#                                      #
#     	     REGISTER AREA             #
#                                      #
########################################
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookTransaction, BookTransactionAdmin)
# admin.site.register(BookTrading, BookTradingAdmin)
#admin.site.register(BookBuying, BookBuyingAdmin)
#admin.site.register(BookTradingGiving, BookTradingGivingAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Offer,OfferAdmin)
admin.site.register(SwapLeafEmailAddress, SwapLeafEmailAddressAdmin)
admin.site.register(SwapLeafEmailConfirmation, SwapLeafEmailConfirmationAdmin)

