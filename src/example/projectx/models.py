from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    usn = models.IntegerField()
    guid = models.CharField(max_length=60)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name or 'untitled product'

class UserAuth(models.Model):

    username = models.CharField(max_length=60)
    token = models.CharField(max_length=60)
    expiration = models.IntegerField()

    def __unicode__(self):
        return self.username or 'untitled user'

PRODUCT_STR = "Product(usn=%s, guid=%s, name=%s, description=%s, active=%s)"
USER_STR = "User(username=%s, token=%s, expiration=%s)"





"""
class Product(Entity):

    using_options(tablename='products')

    name = Field(Unicode(60), required=True)
    description = Field(Text())
    usn = Field(Integer(), nullable=True)
    guid = Field(Unicode(60), nullable=True)
    active = Field(Boolean, default=True)

    @hybrid_property
    def description_textonly(self):
        return ''.join(BeautifulSoup(self.description).findAll(text=True))

    def __unicode__(self):
        return PRODUCT_STR % (self.usn,
                              self.guid,
                              self.name,
                              self.description,
                              self.active) or 'untitled product'

class UserAuth(Entity):

    using_options(tablename='user')
    username = Field(Unicode(60), required=True)
    token = Field(Unicode(60))
    expiration = Field(Integer())

    def __unicode__(self):
        return self.username or 'untitled user'

class UpdateStore(Entity):

    using_options(tablename='update_store')
    name = Field(Unicode(60), required=True)
    number = Field(Integer())

class ApplicationPreference(Entity):

    using_options(tablename='apppref')
    key = Field(Unicode(60), required=True)
    value = Field(Text())

    def __unicode__(self):
        return 'Application Preference(key=%s, value=%s,)' % (self.key, self.value) or 'unknown user preference'


class Message(Entity):

    using_options(tablename='message')
    guid = Field(Unicode(60))
    usn = Field(Integer())
    type = Field(Integer())
    summary = Field(Unicode(255))
    message = Field(Text())
    service = ManyToOne('Service')
    date_created = Field(DateTime())

class Service(Entity):

    using_options(tablename='service')
    guid = Field(Unicode(60))
    usn = Field(Integer())
    name = Field(Unicode(255))
    description = Field(Text(60))
    service_type = Enum([ttypes.CapabilityType._VALUES_TO_NAMES[ttypes.CapabilityType.EBAY],
                         ttypes.CapabilityType._VALUES_TO_NAMES[ttypes.CapabilityType.PAYPAL]])
    settings_ebay = Field(Unicode(60))
    settings_paypal = Field(Unicode(60))
    active = Field(Boolean, default=True)
"""