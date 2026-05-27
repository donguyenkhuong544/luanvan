from django.core.management.base import BaseCommand
from dashboard.models import SimulatedCOSensor

class Command(BaseCommand):
    help = 'Xóa hàng loạt cảm biến CO giả lập dựa trên tiền tố'

    def add_arguments(self, parser):
        parser.add_argument('prefix', type=str, help='Tiền tố mã cảm biến (vd: CO)')
        parser.add_argument('count', type=int, help='Số lượng cảm biến cần xóa')

    def handle(self, *args, **options):
        prefix = options['prefix']
        count = options['count']

        self.stdout.write(f'Deleting {count} sensors with prefix {prefix}...')
        
        deleted = 0
        for i in range(1, count + 1):
            # Create sensor_id format, e.g.: CO_01
            sensor_id = f"{prefix}_{i:02d}"
            try:
                sensor = SimulatedCOSensor.objects.get(sensor_id=sensor_id)
                sensor.delete()
                deleted += 1
            except SimulatedCOSensor.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted} sensors ({count - deleted} not found).'))
