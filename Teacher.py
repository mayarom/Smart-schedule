class Teacher:
    def __init__(self, name, subjects, weekly_hours, free_day):
        self.name = name
        self.subjects = subjects  # Dictionary {subject_name: weekly_hours}
        self.weekly_hours = weekly_hours
        self.free_day = free_day
        self.scheduled_hours = 0
        self.teachertable = self.create_schedule(free_day)

    def create_schedule(self, free_day):
        schedule = [[0 for _ in range(9)] for _ in range(6)]
        if free_day in ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי']:
            free_day_index = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי'].index(free_day)
            for hour in range(9):
                schedule[free_day_index][hour] = -999  # Marking the free day
        return schedule

    def is_teacher_available(self, day, hour):
        if 0 <= day < 6 and 0 <= hour < 9:
            return self.teachertable[day][hour] == 0 and (self.weekly_hours - self.scheduled_hours) > 0
        return False

    def schedule_lesson(self, subject, day, hour, class_name):
        if self.is_teacher_available(day, hour):
            self.teachertable[day][hour] = f"{class_name}: {subject}"
            self.scheduled_hours += 1
            return True
        return False

    def remove_scheduled_lesson(self, day, hour):
        if 0 <= day < 6 and 0 <= hour < 9 and self.teachertable[day][hour] != 0 and self.teachertable[day][
            hour] != -999:
            self.teachertable[day][hour] = 0
            self.scheduled_hours -= 1
            return True
        return False
