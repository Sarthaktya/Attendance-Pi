from datetime import datetime
import os

class AttendanceEngine:
	def __init__(self, save_dir="attendance_logs"):
		self.records = {}
		self.save_dir = save_dir
		os.makedirs(save_dir, exist_ok=True)
		
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		self.file_path = os.path.join(
			save_dir, f"attendance_{timestamp}.csv"
		)
	
	def mark_present(self, name):
		if name in self.records:
			return False
		
		self.records[name] = datetime.now().strftime("%H:%M:%S")
		return True