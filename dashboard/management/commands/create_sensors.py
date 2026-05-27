from django.core.management.base import BaseCommand
from dashboard.models import SimulatedCOSensor

class Command(BaseCommand):
    help = 'Tạo hàng loạt cảm biến CO giả lập cho một khu vực'

    def add_arguments(self, parser):
        parser.add_argument('zone', type=str, help='Mã khu vực (vd: B1, B2)')
        parser.add_argument('count', type=int, help='Số lượng cảm biến cần tạo')

    def handle(self, *args, **options):
        zone = options['zone']
        count = options['count']

        self.stdout.write(f'Creating {count} sensors for zone {zone}...')
        
        created = 0
        for i in range(1, count + 1):
            sensor_id = f"{zone}_CO_{i:02d}"
            name = f"Cảm biến CO số {i} ({zone})"
            
            obj, is_new = SimulatedCOSensor.objects.get_or_create(
                sensor_id=sensor_id,
                defaults={
                    'name': name,
                    'zone': zone,
                    'description': f'Gắn tại hầm {zone}',
                    'operating_hours': 0,
                    'is_active': False
                }
            )
            if is_new:
                created += 1
            else:
                if obj.zone != zone:
                    obj.zone = zone
                    obj.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} new sensors (Skipped {count - created} existing).'))
