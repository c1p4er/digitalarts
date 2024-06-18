from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import Engineer, Supervisor, StoreKeeper, Finance, Driver, ShipmentManager

User = get_user_model()

class Command(BaseCommand):
    help = 'Create staff'

    def handle(self, *args, **options):
        # Create Engineer
        engineer = Engineer.objects.create(
            username='mechanic',
            email='mechanic@gmail.com',
            first_name='Omondi',
            last_name='Rasta',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
            # Other fields as needed
        )
        
        # Create supervisor
        supervisor = Supervisor.objects.create(
            username='supervisor',
            email='supervisor@gmail.com',
            first_name='kaka',
            last_name='moss',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
        )
        
        # Create shipment manageer
        shipmentManager = ShipmentManager.objects.create(
            username='shipmentmanager',
            email='shipmentmanager@gmail.com',
            first_name='sly',
            last_name='kin',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
        )
        
        # create Storekeeper
        storekeeper= StoreKeeper.objects.create(
            username='Inventory',
            email='inventorymanager@gmail.com',
            first_name='ruth',
            last_name='jemel',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
        )
        
        # create Finance
        finance= Finance.objects.create(
            username='finance',
            email='finance@gmail.com',
            first_name='james',
            last_name='buru',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
        )

        # create Driver
        driver= Driver.objects.create(
            username='driver',
            email='driver@gmail.com',
            first_name='isaac',
            last_name='orumi',
            phone_number='1234567890',
            address='south b',
            city='Nairobi',
            county='Nairobi',
            status='accepted',
            is_vendor=True,
            is_staff=True,
        )
        
        # Assign Engineer to Engineer group
        engineer_group, created = Group.objects.get_or_create(name='Engineer')
        engineer.groups.add(engineer_group)
        
        # Assign Engineer to Shipment manager group
        shipment_group, created = Group.objects.get_or_create(name='ShipmentManager')
        shipmentManager.groups.add(shipment_group)
        
        # Assign Supervisor to supervisor group
        supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
        supervisor.groups.add(supervisor_group)
        
        # Assign Storekeeper to storekeeper group
        storekeeper_group, created = Group.objects.get_or_create(name='Storekeeper')
        storekeeper.groups.add(storekeeper_group)
        
        # Assign finance to finance group
        finance_group, created = Group.objects.get_or_create(name='Finance')
        finance.groups.add(finance_group)
        
        # Assign finance to driver group
        driver_group, created = Group.objects.get_or_create(name='Driver')
        driver.groups.add(driver_group)

        # Hash password (Django handles this automatically)
        engineer.set_password('12345678')
        engineer.save()
        
        shipmentManager.set_password('12345678')
        shipmentManager.save()
        
        supervisor.set_password('12345678')
        supervisor.save()
        
        storekeeper.set_password('12345678')
        storekeeper.save()
        
        finance.set_password('12345678')
        finance.save()
        
        driver.set_password('12345678')
        driver.save()

        self.stdout.write(self.style.SUCCESS('staffs created successfully.'))
