from datetime import datetime

class Project:
    STATUSES = ['active', 'completed', 'on_hold']

    def __init__(self, name, description, start_date, end_date, status='active'):
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

        if status not in self.STATUSES:
            raise ValueError(f'Invalid status: {status}')
        self.status = status

    def update_status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError('Invalid status')
        self.status = new_status

    def get_progress(self):
        total_time = (self.end_date - self.start_date).total_seconds()
        elapsed_time = (datetime.now() - self.start_date).total_seconds()
        progress = (elapsed_time / total_time) * 100

        if progress < 0:
            progress = 0
        elif progress > 100:
            progress = 100

        return int(progress)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
        }
