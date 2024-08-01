from django.db import models
from django.urls import reverse


# Create your models here.

TIMES = (("M", "Morning"), ("E", "Evening"), ("N", "Night"))


class Peak(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("toy-detail", kwargs={"pk": self.id})


class Climber(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Add the M:M relationship
    toys = models.ManyToManyField(Toy)
    
    def __str__(self):
        return self.name

    # Define a method to get the URL for this particular climber instance
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse("climber-detail", kwargs={"climber_id": self.id})


class Climb(models.Model):
    date = models.DateField("Climb Date")
    # adding "Climb Date" changes title on admin page for the input form
    time = models.CharField(
        max_length=1,
        # Note that we’re going to use just a single-character to represent what time-of-day 
        # the climb is for: "M"orning, "E"vening or "N"ight.
        # add the 'choices' field option
        choices=TIMES,
        # set the default value for time to be 'M' (Morning)
        default=TIMES[0][0],
    )
    # Create a climber_id column for each climb in the database
    # As you can see, the ForeignKey field-type is used to create a one-to-many relationship.

    # The first argument provides the parent Model, Climber.
    # In a one-to-many relationship, the on_delete=models.CASCADE is required. It ensures that if a Climb record is deleted, all of the child Climbs will be deleted automatically as well - thus avoiding orphan records for climbs that are no longer tied to an existing Climb.
    cat = models.ForeignKey(Climber, on_delete=models.CASCADE)
    # In the database, the column in the climbs table for the FK will actually be called climber_id instead of "climber" because Django by default appends _id to the name of the attribute used in the Model.

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    # Define the default order of climbs
    class Meta:
        ordering = ["-date"]  # This line makes the newest climbs appear first
