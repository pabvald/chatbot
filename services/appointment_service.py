from app import app, db
from datetime import datetime, date, time, timedelta
from models import Appointment


class AppointmentService(object):
    """ AppointmentService class """

    APPOINTMENT_SCHEDULE = {
        0: {'begin': time(hour=9),
            'end': time(hour=14),
            },
        1: {'begin': time(hour=9),
            'end': time(hour=14)
            },
        2: {'begin': time(hour=9),
            'end': time(hour=14)
            },
        3: {
            'begin': time(hour=9),
            'end': time(hour=14)
            },
        4: {
            'begin': time(hour=9),
            'end': time(hour=14)
            }
    }

    APPOINTMENT_DURATION = timedelta(minutes=30)

    @staticmethod
    def get_all_slots(iso_datetime):
        """ Obtains the possible appointment slots in a given day
            considering the schedule """
        d_time = datetime.fromisoformat(iso_datetime)
        d_date = date(d_time.year, d_time.month, d_time.day)
        schedule = AppointmentService.APPOINTMENT_SCHEDULE.get(d_date.weekday(), {})
        slots = []

        if schedule:
            begin_time = datetime.combine(d_date, schedule['begin'])
            end_time = datetime.combine(d_date, schedule['end'])

            while begin_time < end_time:
                slots.append(begin_time)
                begin_time += AppointmentService.APPOINTMENT_DURATION

        return slots

    @staticmethod
    def get_available_slots(iso_datetime):
        """ Obtains the available slots in a given day considering the 
            schedule and the already made appointments"""
        all_slots = AppointmentService.get_all_slots(iso_datetime)
        made_appointments = AppointmentService.get_made_appointments(iso_datetime)
        available_slots = []

        for slot in all_slots:
            if slot not in made_appointments:
                available_slots.append(slot)

        return available_slots

    @staticmethod
    def get_made_appointments(iso_datetime):
        """ Obtains a list of the already made appointments in a given date """
        appointments = []
        request_d_time = datetime.fromisoformat(iso_datetime)
        request_date = datetime(request_d_time.year,
                                request_d_time.month,
                                request_d_time.day)
        try:
            query = db.session.query(Appointment).filter(
                Appointment.d_time >= request_date
            ).all()
            appointments = list(map(lambda appointment: appointment.d_time, query))
        except Exception as e:
            app.logger.error(str(e))
            raise
        else:
            return appointments

    @staticmethod
    def office_is_open_on_date(iso_date):
        """ Determines if the office is open on a given date
            considering the schedule """
        d_time = datetime.fromisoformat(iso_date)
        d_date = date(d_time.year, d_time.month, d_time.day)
        schedule = AppointmentService.APPOINTMENT_SCHEDULE.get(d_date.weekday(), {})
        return schedule != {}

    @staticmethod
    def office_is_open_on_datetime(iso_datetime):
        """ Determines if the office is open at a given datetime 
            considering the schedule """
        is_open = False
        d_time = datetime.fromisoformat(iso_datetime)
        d_date = date(d_time.year, d_time.month, d_time.day)
        schedule = AppointmentService.APPOINTMENT_SCHEDULE.get(d_date.weekday(), {})
        if schedule:
            begin_time = datetime.combine(d_date, schedule['begin'])
            end_time = datetime.combine(d_date, schedule['end'])
            if begin_time <= d_time <= end_time:
                is_open = True

        return is_open

    @staticmethod
    def is_available(iso_datetime):
        """ Determines if a certain datetime is available for
            an appoinment """
        d_time = datetime.fromisoformat(AppointmentService.closest_half(iso_datetime))
        av_slots = AppointmentService.get_available_slots(iso_datetime)
        is_available = (d_time in av_slots)

        return is_available

    @staticmethod
    def closest_half(iso_datetime):
        """ Generates the closes datetime which is a half or o'clock 
            hour """
        d_time = datetime.fromisoformat(iso_datetime)
        approx = round(d_time.minute / 30.0) * 30
        d_time = d_time.replace(minute=0)
        d_time += timedelta(seconds=approx * 60)
        d_time = d_time.replace(second=0)
        return d_time.isoformat()
