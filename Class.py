import random


class Class:
    def __init__(self, name, subjects_hours):
        self.name = name
        self.subjects_hours_fixed = subjects_hours  # Dictionary {subject_name: weekly_hours}
        self.subjects_hours_scheduled = {subject: 0 for subject in subjects_hours}
        self.class_schedule = [[0 for _ in range(9)] for _ in
                               range(6)]  # Initialize a 6x9 schedule (6 days, 9 hours per day)

    def is_class_available(self, day, hour):
        # Check if the slot is available
        return self.class_schedule[day][hour] == 0

    def get_transposed_schedule(self):
        # Transpose the schedule to have days as columns and hours as rows
        transposed_schedule = list(zip(*self.class_schedule))
        # Replace '0' with 'Free' to indicate free periods
        transposed_schedule = [['-' if hour == 0 else hour for hour in day] for day in transposed_schedule]
        return transposed_schedule

    def schedule_lesson(self, subject, day, hour):
        # Schedule a lesson if it's possible
        if self.is_class_available(day, hour):
            self.class_schedule[day][hour] = subject
            self.subjects_hours_scheduled[subject] += 1
            return True
        return False

    def build_schedule_for_class(self):
        sorted_subjects = sorted(self.subjects_hours_fixed.items(), key=lambda x: x[1], reverse=True)
        attempts_limit = 100  # Limit attempts to prevent infinite loop

        for subject, hours_needed in sorted_subjects:
            attempts = 0
            while self.subjects_hours_scheduled[subject] < hours_needed and attempts < attempts_limit:
                day = random.randint(0, 5)  # Choose a day (0=Sunday, 5=Friday)
                hour = random.randint(0, 8)  # Choose an hour (0-8)

                # Try scheduling two consecutive lessons if needed and possible
                if hours_needed - self.subjects_hours_scheduled[subject] > 1 and \
                        self.is_class_available(day, hour) and \
                        self.is_class_available(day, (hour + 1) % 9):
                    self.schedule_lesson(subject, day, hour)
                    self.schedule_lesson(subject, day, (hour + 1) % 9)
                elif self.is_class_available(day, hour):
                    # Schedule a single lesson if possible
                    self.schedule_lesson(subject, day, hour)
                else:
                    # If scheduling was not possible, increase attempt count
                    attempts += 1

            if attempts >= attempts_limit:
                # If we've reached the attempt limit, report failure to schedule this subject
                print(f"Unable to schedule all hours for {subject}. Please check constraints.")
                return False

        self.optimize_schedule()
        print(f"The schedule for class {self.name} was created successfully.")
        return True

    def schedule_lesson(self, subject, day, hour):
        if self.is_class_available(day, hour) and (
                self.subjects_hours_fixed[subject] - self.subjects_hours_scheduled[subject]) > 0:
            self.class_schedule[day][hour] = subject
            self.subjects_hours_scheduled[subject] += 1
            return True
        return False

    def remove_scheduled_lesson(self, day, hour, subject):
        if self.is_class_available(day, hour) and self.class_schedule[day][hour] == subject:
            self.class_schedule[day][hour] = 0
            self.subjects_hours_scheduled[subject] -= 1
            return True
        return False

    def get_schedule_as_list(self):
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        schedule_list = []
        for day_index, day_schedule in enumerate(self.class_schedule):
            schedule_str = f"{days[day_index]}: "
            schedule_str += ", ".join([subject if subject != 0 else "Free" for subject in day_schedule])
            schedule_list.append(schedule_str)
        return schedule_list

    def optimize_schedule(self):
        # A method to move lessons around and eliminate free hours starting from the beginning of the day
        for day in range(6):  # For each day
            for hour in range(8):  # Start from the beginning of the day
                if self.class_schedule[day][hour] == 0:  # If this hour is free
                    # Find the next lesson that could be moved here
                    for later_hour in range(hour + 1, 9):
                        if self.class_schedule[day][later_hour] != 0:
                            # Swap the free period with the later lesson
                            self.class_schedule[day][hour] = self.class_schedule[day][later_hour]
                            self.class_schedule[day][later_hour] = 0
                            # After moving a lesson, break out of the inner loop and check if the next hour is free
                            break

    def _choose_day(self, days):
        # בחירת יום אקראי עם העדפה לימים ראשון עד רביעי
        return random.choice([day for day in days if day < 4]) or random.choice(days)

    def _choose_hour(self, hours_needed):
        # התחלת שעות הבוקר
        if hours_needed > 1:
            return random.randint(0, 2)
        return random.randint(0, 8)
