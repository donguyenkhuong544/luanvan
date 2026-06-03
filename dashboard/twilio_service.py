import logging
import threading
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Lưu trữ thời gian gọi gần nhất cho từng quạt
# Format: {'Q1': datetime.datetime(2023, 10, 25, 10, 30, 0)}
# biến last_call_times lưu dưới dạng từ điển
# date_time là một đối tượng thời gian
# cool_down là thời gian chờ
_last_call_times = {}
_cooldown_lock = threading.Lock()

COOLDOWN_MINUTES = 10

def _get_users_to_call():
    """Nhận cuộc gọi tất cả các số điện thoại được khai báo."""
    # Lấy thông tin user từ database
    from accounts.models import UserProfile
    return UserProfile.objects.filter(      #lọc ra những ai cần nhận thông báo
        receive_call_alerts=True         # nhận thông tin cảnh báo qua cuộc gọi
    ).exclude(
        phone_number__isnull=True        # không có số điện thoại
    ).exclude(
        phone_number__exact=''           # số điện thoại rỗng, giống như yêu đơn phương ai đó tên Linh. Kkkkkk
    )

def _mock_call(phone_number, unit_id, reason):
    """Mocks a phone call by printing to the console/logger."""
    msg = f"\n" + "="*60 + f"\n[TWILIO MOCK] DANG GOI DIEN THOAI DEN SO: {phone_number}\n" \
          f"[TWILIO MOCK] Noi dung: 'Canh bao! Thiet bi {unit_id} gap su co: {reason}.'\n" + "="*60 + "\n"
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'), flush=True)
        
    logger.error(f"[Twilio Mock] Triggered call to {phone_number} for unit {unit_id} - Reason: {reason}")

def trigger_alert_call(unit_id, reason):
    """
    Checks cooldown and triggers a mock phone call to all subscribed users.
    Returns True if calls were made, False if skipped (due to cooldown or no users).
    """
    with _cooldown_lock:
        now = datetime.now()                # bắt đầu hiện tại
        last_time = _last_call_times.get(unit_id)
        
        if last_time and (now - last_time) < timedelta(minutes=COOLDOWN_MINUTES):
            # Cooldown active, skip call
            return False
            
        # Update last call time
        _last_call_times[unit_id] = now

    # Get users to call
    users_to_call = _get_users_to_call()
    print(f"DEBUG: Tim thay {users_to_call.count()} nguoi dung thoa man dieu kien.")
    
    if not users_to_call.exists():
        logger.info(f"[Twilio Mock] No users configured to receive call alerts for {unit_id}")
        return False
        
    for profile in users_to_call:
        # Run mock call in a separate thread so it doesn't block the MQTT loop
        threading.Thread(
            target=_mock_call, 
            args=(profile.phone_number, unit_id, reason),
            daemon=False
        ).start()
        
    return True
