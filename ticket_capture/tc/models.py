from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



# Create your models here.

class User(AbstractUser):
    is_supervisor = models.BooleanField('supervisor status', default=False)
    is_typist = models.BooleanField('typist status', default=False)
    is_classifier = models.BooleanField('classifier status', default=False)

    def __str__(self):
        return self.username

class Ticket(models.Model):
    consumer_id = models.IntegerField(default = 0)
    photo_url = models.CharField(max_length = 200)
    confirmed = models.BooleanField(blank = True, null = True)
    valid = models.BooleanField(blank = True, null = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __unicode__(self):
        return self.id

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.consumer_id:
            self.created_at = timezone.now()
            self.updated_at = timezone.now()
        return super(Ticket, self).save(*args, **kwargs)

class Store(models.Model):
    rfc = models.CharField(max_length = 13)
    alias = models.CharField(max_length = 50, blank = True, null = True)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Store, self).save(*args, **kwargs)

#return alias name
    def __str__(self):
        return self.alias

class Capture (models.Model):
    captured_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'captured_by')
    ticket = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    ticket_date = models.DateTimeField('ticket date')
    ticket_time = models.DateTimeField('ticket time')
    branch_postal_code = models.IntegerField(default = 0)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    country = models.CharField(max_length = 50)
    total_amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    evaluated = models.BooleanField(blank = True, null = True)
    evaluated_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'evaluated_by', blank = True, null = True)
    valid = models.BooleanField(blank = False)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Capture, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Brand, self).save(*args, **kwargs)

class Category(models.Model):
    description = models.CharField(max_length = 200)
    code = models.IntegerField(default = 0)
    parent = models.ForeignKey('self', on_delete = models.CASCADE)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Category, self).save(*args, **kwargs)

class Tag (models.Model):
    description = models.CharField(max_length = 100)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Tag, self).save(*args, **kwargs)

class Item(models.Model):
    capture = models.ForeignKey(Capture, on_delete = models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
    unit_price = models.DecimalField(max_digits = 10, decimal_places=2, blank = True, null = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    quantity = models.DecimalField(max_digits = 10, decimal_places=2, blank = True, null = True)
    created_at = models.DateTimeField(editable = False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Item, self).save(*args, **kwargs)