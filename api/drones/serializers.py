from rest_framework import serializers
from .models import Pilot, Competition, Drone, DroneCategory

class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='drone-detail')
    """The view_name value is 'drone-detail' to indicate the browsable
        API feature to use the drone detail view to render the
        hyperlink when the user clicks or taps on it. This way, we
        make it possible for the browsable API to allow us to browse
        between related models."""
    class Meta:
        model = DroneCategory
        fields = ('url','pk','name','drones')

class DroneSerializer(serializers.HyperlinkedModelSerializer):
    #category attribute name sis defined in Drone model
    category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')
    class Meta:
        model  =Drone
        fields = (
            'url',
            'name',
            'category',
            'manufacturing_date',
            'has_it_competed',
            'inserted_timestamp',
            )

class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
# Display all the details for the related drone
    drone = DroneSerializer()
    class Meta:
        model = Competition
        fields = (
        'url',
        'pk',
        'competition_name',
        'distance_in_feet',
        'drone')

class PilotSerializer(serializers.HyperlinkedModelSerializer):
    """The many
        argument is set to True because it is a one-to-many relationship (one Pilot
        has many related Competition instances)."""
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)
    class Meta:
        model = Pilot
        fields = (
        'url',
        'name',
        'gender',
        'gender_description',
        'races_count',
        'inserted_timestamp',
        'competitions')

class PilotCompetitionSerializer(serializers.ModelSerializer):
# Display the pilot's name
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    # Display the drone's name
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')
    class Meta:
        model = Competition
        fields = (
        'url',
        'pk',
        'distance_in_feet',
        'pilot',
        'drone',
        'competition_name')