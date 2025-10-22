from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        if not title:
            raise ValueError('title cannot be empty')
        if priority not in (1, 2, 3):
            raise ValueError('priority must be 1, 2, 3')
        if not isinstance(due_date, datetime):
            raise TypeError('due_date must be a datetime object')

        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = 'pending'
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        allowed_statuses = ['pending', 'in_progress', 'completed']

        if new_status not in allowed_statuses:
            raise ValueError('Invalid status')

        self.status = new_status


    def is_overdue(self) -> bool:
        if self.status == 'completed':
            return False

        now = datetime.now()
        return now > self.due_date

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': str(self.due_date),
            'project_id': self.project_id,
            'assignee_id': self.assignee_id
        }
