from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
   
from swapleaf.app.main.utils import get_elapse_time
# from swapleaf.helper.common import convert_queryset_to_list
from markdown import markdown

import datetime
import uuid 

########################################
#                                      #
#           CONSTANT DATA              #
#                                      #
########################################
USA_STATES = (
   ("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA","California"),
   ("CO","Colorado"),("CT","Connecticut"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
   ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),
   ("KS","Kansas"),("KY","Kentucky"),("LA","Louisana"),("ME","Maine"),("MD","Maryland"),
   ("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),("MS","Mississippi"),("MO","Missouri"),
   ("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),("NJ","New Jersey"),
   ("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
   ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),
   ("SD","South Dakota"),("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),
   ("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),("WI","Wisconsin"),("WY","Wyoming"),
)

BOOK_CONDITION = (
    ('1', "Acceptable"),
    ("2", "Good"),
    ("3", "Very Good"),
    ("4", "Like New"),
    ("5", "Brand New")
)

TRANSACTION_STATUS = (
    ("None","None"),
    ("Pending","Pending"),
    ("Complete","Complete"),
)

TRANSACTION_TYPE = (
    ('1','Sell'),
    ('2','Trade/Give Away'),
)

NOTIFY_STATUS = (
      ("old", "old"),
      ("new", "new"),
    ) 

NOTIFY_TYPE = (
      ('invite_partner','invite_partner'),
      ('invite_partner_response_accept','invite_partner_response_accept'),        # Not notice
      ('invite_partner_response_decline','invite_partner_response_decline'),      # Not notice
      ('partner_request_not_active','partner_request_not_active'),          # Not notice
      ('accept_partner','accept_partner'),
      ("make_offer_price",'make_offer_price'),
      ("make_counter_offer_price","make_counter_offer_price"),
      ('accept_offer_price','accept_offer_price'),
      ("make_offer_time_location",'make_offer_time_location'),
      ('accept_offer_time_location','accept_offer_time_location'),
    ) 

# OFFER_STATUS = (
#         ('1','Nothing Happen'),
#         ('2','Pending'),
#         ('3','Complete')
#     )

OFFER_TYPE = (
        ("1","Offer"),
        ("2","Counter Offer"),
    )

# PARTNER_STATUS = (
#         ('1','partner'),
#         ('-1','not_partner'),
#         ('2','waiting'),
#         ('-2','response'),
#     )

# User profile Model
class UserProfile(models.Model):
    # This field is required.
    user = models.ForeignKey(User, unique=True)
    
    # Additional fields of user
    zip_code = models.IntegerField(blank=True,null=True)
    partner_status = models.IntegerField(blank=True,null=True,default=-1)
    school = models.ForeignKey('Institution',blank=True,null=True)
    course = models.ManyToManyField('Course',blank=True,null=True)
    buy_book = models.ManyToManyField('BookBuying',blank=True,null=True)
    available_book_author = models.ManyToManyField("BookAvailableAuthor",blank=True,null=True)
    partners = models.ManyToManyField(User, related_name='partners',blank=True,null=True)

    def __unicode__(self):
        return unicode(self.user)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


# Institution Model
class Institution(models.Model):
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2,choices=USA_STATES)

    # Relationship
    student = models.ManyToManyField(User,blank=True,null=True)

    def __unicode__(self):
        return unicode(self.name)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender')
    receiver= models.ForeignKey(User, related_name='receiver')
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    elapse_time = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        elapse = now - self.date
        self.elapse_time = get_elapse_time(int(elapse.total_seconds())) 
        self.content_html = markdown(self.content.replace("\n","<br>").replace(" ","&nbsp;"))
        super(Message, self).save(*args, **kwargs)

# Book model
class Book(models.Model):
    title = models.CharField(max_length=600)
    isbn10 = models.CharField(max_length=20,blank=True,null=True)
    isbn13 = models.CharField(max_length=20,blank=True,null=True)
    author = models.CharField(max_length=500,blank=True)
    #rating = models.FloatField(blank=True,default=0.0)
    #publish_date = models.DateField(blank=True,null=True)
    #cover_image = models.ImageField("Book Cover Image", upload_to="uploads/img/book_cover/", blank=True, default='default/img/book_cover_default.jpg')
    #num_page = models.IntegerField(blank=True,null=True)
    #publisher = models.CharField(max_length=100,blank=True)
    edition = models.IntegerField(blank=True,null=True)
    #description = models.TextField(blank=True)
    def __unicode__(self):
        return unicode(self.title)

class Course(models.Model):
    institution = models.ForeignKey(Institution)
    # crn = models.IntegerField()
    # title = models.CharField(max_length=100)
    # subject = models.CharField(max_length=10)
    course_number = models.CharField(max_length=10)
    course_book = models.ManyToManyField(Book, related_name='course_book',null=True)

    def __unicode__(self):
        return unicode(self.course_number)

class Offer(models.Model):
    user_offer = models.ForeignKey(User,related_name='user_offer')
    user_receive = models.ForeignKey(User,related_name='user_receive')
    messages = models.ManyToManyField(Message,related_name='message',null=True)
    last_message = models.ForeignKey(Message,related_name='last_message',null=True)
    price = models.DecimalField(max_digits=19,decimal_places=2)    
    location = models.CharField(max_length=200,blank=True)
    transaction_time = models.DateTimeField(blank=True,null=True) 
    view_status = models.CharField(max_length=3,choices=NOTIFY_STATUS,default='new')
    #offer_status = models.CharField(max_length=1,choices=OFFER_STATUS,default='1')
    offer_type = models.CharField(max_length=1,choices=OFFER_TYPE,default='1')
    offer_time = models.DateTimeField(default=datetime.datetime.now())

class BookTransaction(models.Model):
    transaction_id = models.CharField(unique=True,max_length=100)
    seller = models.ForeignKey(User,related_name="seller")
    buyer = models.ForeignKey(User, related_name="buyer", blank=True, null=True)
    book = models.ForeignKey(Book)
    course = models.ForeignKey(Course,blank=True,null=True)
    price = models.DecimalField(max_digits=19,decimal_places=2)
    location = models.CharField(max_length=200,blank=True)
    #price = models.IntegerField(default=0)
    offer = models.ManyToManyField(Offer,null=True)
    condition = models.CharField(max_length=1,choices=BOOK_CONDITION)
    status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='none')
    transaction_type = models.CharField(max_length=1,choices=TRANSACTION_TYPE)
    transaction_time = models.DateTimeField(blank=True,null=True)
    post_time = models.DateTimeField(default=datetime.datetime.now())
    alert_email = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     self.transaction_id = uuid.uuid1()
    #     super(BookTransaction, self).save(*args, **kwargs)

class Notify(models.Model):
    content = models.TextField()
    offer_content = models.TextField()
    status = models.CharField(max_length=3,choices=NOTIFY_STATUS,default='new')
    notify_type = models.CharField(max_length=50,choices=NOTIFY_TYPE,null=True)
    notify_to = models.ForeignKey(User, related_name='notify_to')
    notify_from = models.ForeignKey(User, related_name='notify_from')
    object_id = models.IntegerField(default=-1)
    date = models.DateTimeField(default=datetime.datetime.now())
    elapse_time = models.CharField(max_length=50)

    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     elapse_time = now - self.date
    #     self.elapse_time = get_elapse_time(int(elapse_time.total_seconds())) 
    #     super(Notify, self).save(*args, **kwargs)

    class Meta:
         ordering= ['date']

class BookAvailableAuthor(models.Model):
    author = models.CharField(max_length=500,blank=True)
    alert_email = models.BooleanField(default=True)

class BookBuying(models.Model):
    book = models.ForeignKey(Book)
    alert_email = models.BooleanField(default=True)
    post_time = models.DateTimeField(default=datetime.datetime.now())
    # buyer = models.ForeignKey(User, related_name="book_buyer", blank=True, null=True)
    # transaction_partner = models.ForeignKey(User, related_name="transaction_partner", blank=True, null=True)
    # transaction_type = models.CharField(max_length=10,choices=TRANSACTION_TYPE)
    # price = models.DecimalField(max_digits=19,decimal_places=2)
    # transaction_time = models.DateTimeField(blank=True,null=True)
    # post_time = models.DateTimeField(default=datetime.datetime.now())

    # def save(self, *args, **kwargs):
    #     self.transaction_id = uuid.uuid1()
    #     super(BookBuying, self).save(*args, **kwargs)

# class BookTrading(models.Model):
#     transaction_id = models.CharField(unique=True,max_length=100)
#     trader1 = models.ForeignKey(User,related_name="trader1")
#     book_trade1 = models.ForeignKey(Book,related_name="book_trader1")
#     book_condition1 = models.CharField(max_length=1,choices=BOOK_CONDITION)
#     price_book1 = models.DecimalField(max_digits=19,decimal_places=2)
#     trader2 = models.ForeignKey(User,related_name="trader2",blank=True, null=True)
#     book_trade2 = models.ForeignKey(Book,related_name="book_trader2",blank=True,null=True)
#     book_condition2 = models.CharField(max_length=1,choices=BOOK_CONDITION)
#     price_book2 = models.DecimalField(blank=True,null=True,max_digits=19,decimal_places=2)
#     status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='none')
#     transaction_time = models.DateTimeField(blank=True,null=True)
#     post_time = models.DateTimeField(default=datetime.datetime.now())

#     def save(self, *args, **kwargs):
#         self.transaction_id = uuid.uuid1()
#         super(BookTrading, self).save(*args, **kwargs)

# class BookTradingGiving(models.Model):
#     transaction_id = models.CharField(unique=True,max_length=100)
#     trader1_giver = models.ForeignKey(User,related_name="giver")
#     trader2_receiver = models.ForeignKey(User,related_name="receiver",blank=True,null=True)
#     book1 = models.ForeignKey(Book,related_name="book1")
#     book2 = models.ForeignKey(Book,related_name="book2",blank=True,null=True)
#     condition1 = models.CharField(max_length=1,choices=BOOK_CONDITION)
#     condition2 = models.CharField(max_length=1,choices=BOOK_CONDITION,blank=True,null=True)
#     course = models.ForeignKey(Course,related_name='course1',blank=True,null=True)
#     status = models.CharField(max_length=10,choices=TRANSACTION_STATUS,default='none')
#     transaction_time = models.DateTimeField(blank=True,null=True)
#     post_time = models.DateTimeField(default=datetime.datetime.now())
#     send_alert = models.BooleanField(default=True)

#     def save(self, *args, **kwargs):
#         self.transaction_id = uuid.uuid1()
#         super(BookTradingGiving, self).save(*args, **kwargs)