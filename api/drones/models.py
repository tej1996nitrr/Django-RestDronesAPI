from django.db import models

# Create your models here.
class  DroneCategory(models.Model):
    name = models.CharField(max_length=50,unique=True)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Drone(models.Model):
    name = models.CharField(max_length = 50,unique=True)
    manufacturing_date = models.DateTimeField()
    category = models.ForeignKey('DroneCategory',on_delete=models.CASCADE,related_name='drones')
    inserted_timestamp = models.DateTimeField(auto_now_add=True)
    has_it_competed = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='dronesusers',on_delete=models.CASCADE) #creates a backward relation from the User to the Drone model this value indicates the name to use for the relation from the related User object back to a Drone object
    class  Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name
#auto_now-> for update auto_now_add-> for created date

class Pilot(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    )
    
    name = models.CharField(max_length = 50,blank=False,default='Pilot')
    gender = models.CharField(max_length = 2,choices =GENDER_CHOICES, default=MALE)
    races_count = models.IntegerField(null=False, blank=False,default=0)
    inserted_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name

class Competition(models.Model):
    """"The competition must be
        related to an existing pilot and an
        existing drone.Each
        competition must include the pilot's
        name that made the drone reach a
        specific distance and the drone's
        name."""
    #1 pilot, drone can be in many competition
    #class name=many attribute name=one
    #competition=many, pilot=one
    competition_name = models.CharField(max_length = 30)
    pilot = models.ForeignKey('Pilot',related_name='competitions',on_delete=models.CASCADE)
    drone = models.ForeignKey('Drone',on_delete=models.CASCADE)
    distance_in_feet  =models.IntegerField(null=False, blank=False)
    class Meta:
        # Order by distance in descending order
       ordering = ('-distance_in_feet',)
    def __str__(self):
        return self.competition_name




