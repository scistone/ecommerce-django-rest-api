from users.models import CustomerAddress,Customer,User
from rest_framework import fields, serializers




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]

        extra_kwargs = {'email': {'read_only':True},}
        
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = [
            'user',
            'date_of_birth',
            'phone',
            'gender'
        ]
    
    def update(self,instance):
        user    = User.objects.get(id=instance)
        account = Customer.objects.get(user=user)
        userfields = self.validated_data["user"]

        if userfields['first_name']:
            user.first_name = userfields['first_name']
            
        if userfields['last_name']:
            user.last_name = userfields['last_name']

        if self.validated_data['phone']:
            account.phone = self.validated_data['phone']
        
        if self.validated_data['date_of_birth']:
            account.date_of_birth = self.validated_data['date_of_birth']
        
        if self.validated_data['gender']:
            account.gender = self.validated_data['gender']

        user.save()

        account.save()
        return account