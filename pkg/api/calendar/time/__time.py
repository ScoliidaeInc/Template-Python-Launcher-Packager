"""Used to obfuscate unused variables from namespace"""

from types import NoneType
from calendar import isleap as _isleap
from datetime import datetime

class Time:
    """
    Handles all formats involving time used by the application

    If it ticks, it can be counted here

    ---

    Available Calls:
    - () "Initializes the class, if printed returns the used format"
    - timestamp "Returns a float representation of a given date and time"
    - read_timestamp "Returns a date time string based on a given float"
    - utc_offset "Returns the number of hours offset from Universal Time Coordinated"
    - now "Returns the current time"
    """

    @staticmethod
    def timestamp(date_time:str=None)-> float:
        """
        Returns a float value from the datetime library
        using the current system time or an optionally passed ```date time``` in string format
        """
        #region Sterilize inputs
        if not isinstance(date_time, (str,NoneType)):
            err="Inappropriate argument type for argument date_time, please try a str type input."
            raise TypeError(err)
        elif date_time is None:
            return datetime.timestamp(datetime.now())
        else:
            date_time=date_time.replace("/","-")
            date_indicator:str= "-"
            time_indicator:str= ":"
            ms_indicator:str= "." if "." in date_time else None
        if any({date_indicator not in date_time, time_indicator not in date_time}):
            err="Inappropriate argument value (of correct type),"+\
                " please make sure the string includes both the date and the time."
            raise ValueError(err)
        #endregion Sterilize inputs
        #region date find
        date= date_time.split(" ",1)[0].replace(" ","").strip().split(date_indicator) \
            if date_time.find(date_indicator)<date_time.find(" ") \
            else date_time.split(" ")[1].replace(" ","").strip().split(date_indicator)
        if 1<=int(date[1])<=12 and 1<=int(date[2])<=31:# yr/m/dy
            year=int(date[0])
            month=int(date[1])
            day=int(date[2])
        elif 1<=int(date[1])<=31 and 1<=int(date[2])<=12:# yr/dy/m
            year=int(date[0])
            day=int(date[1])
            month=int(date[2])
        elif 1<=int(date[0])<=12 and 1<=int(date[1])<=31:# m/dy/yr
            month=int(date[0])
            day=int(date[1])
            year=int(date[2])
        elif 1<=int(date[0])<=12 and 1<=int(date[2])<=31:# m/yr/dy
            month=int(date[0])
            year=int(date[1])
            day=int(date[2])
        elif 1<=int(date[0])<=31 and 1<=int(date[1])<=12:# dy/m/yr
            day=int(date[0])
            month=int(date[1])
            year=int(date[2])
        elif 1<=int(date[0])<=31 and 1<=int(date[2])<=12:# dy/yr/m
            day=int(date[0])
            year=int(date[1])
            month=int(date[2])
        else:# No format expected matched
            err="Could not establish a normalized date format,"+\
                f" please check your input(date={date})"
            raise ValueError(err)
        #region verify valid date
        short_months:dict={4:"Apirl",6:"June",8:"August",10:"October",12:"December"}
        exception_month:int=2
        if month==exception_month:
            leap_yr=29 if _isleap(year) else 28
            if leap_yr<day:
                recommended_date=f"{year}-{month+1}-{day-leap_yr}"
                err=f"Invalid day({day}) for February of {year}! Perhaps you meant to use, "+\
                    f"{recommended_date} instead?"
                raise ValueError(err)
        elif day==31 and month in short_months:
            recommended_date=f"{year}-{short_months[month+1]}-{day-30}"
            err=f"Invalid day({day}) for {short_months[month]} of {year}! "+\
                "Perhaps you meant to use, {recommended_date} instead?"
            raise ValueError(err)
        #endregion verify valid date
        #endregion date find
        #region configure time output for regions
        time= date_time.split(" ",1)[1].replace(" ","").strip().lower() \
            if date_time.split(" ",1)[1]!=date \
            else date_time.split(" ",1)[0].replace(" ","").strip().lower()
        #region assign hr:min:sec:ms
        hour,minute,remaining=time.split(":")
        if ms_indicator is not None:
            second,microsecond=remaining.split(ms_indicator,1)
            microsecond=int(
                microsecond if not microsecond.lower().endswith(("am","pm")) else microsecond[:-2]
                )
        else:
            second,microsecond=remaining,0
        if second=="":
            second=0
        hour,minute,second= int(hour),int(minute),int(second)
        #endregion assign hr:min:sec:ms
        international_format:bool= True if not time.endswith(("am","pm")) else False
        if international_format is False:
            hour= hour+12 if time.endswith("pm") and hour<12 else hour
            hour= hour-12 if time.endswith("am") and 12<hour else hour
        #region verify all values fall within proper ranges
        if hour<0 or 23<hour:
            raise ValueError("Hour is outside of range accepted for time format")
        elif minute<0 or 59<minute:
            raise ValueError("Minute is outside of range accepted for time format")
        elif second<0 or 59<second:
            raise ValueError("Second is outside of range accepted for time format")
        elif microsecond<0 or 999999<microsecond:
            raise ValueError("Microsecond is outside of range accepted for time format")
        #endregion verify all values fall within proper ranges
        #endregion configure time output for regions
        return datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond
            ).timestamp()
    @staticmethod
    def read_timestamp(snowflake:float, /, international:bool=True, written:bool=False)-> str:
        """
        Returns a human-readable string representation of the passed float value (snowflake)

        ---

        By default human_readable AND international are set to False

        Example: 01-01-2024 00:00:00.000000
        Format: nMonth-nDay-nYear 12hr:min:sec:ms(AM/PM)
        """
        if isinstance(snowflake,str):
            try:
                snowflake=float(snowflake)
            except ValueError as exc:
                raise ValueError("Please ensure the input in a valid float before parsing") from exc
        year,month,day,hour,minute,*remaining= str(
        datetime.fromtimestamp(snowflake)
            ).replace("-"," ").replace(":"," ").replace("."," ").split(" ",6)
        second=remaining[0]
        if len(remaining)!=1:
            microsecond= remaining[1]
        else:
            microsecond="000000"
        month,day,hour= int(month),int(day),int(hour)
        if written is True:
            #region value aliasing
            month_alias={
                1:"January",
                2:"February",
                3:"March",
                4:"April",
                5:"May",
                6:"June",
                7:"July",
                8:"August",
                9:"September",
                10:"October",
                11:"November",
                12:"December"
            }
            ending_pronounciation= {
                1:"first",
                2:"second",
                3:"third",
                4:"fourth",
                5:"fifth",
                6:"sixth",
                7:"seventh",
                8:"eigth",
                9:"nineth",
                10:"tenth",
                11:"eleventh",
                12:"twelfth",
                13:"thirteenth",
                14:"fourteenth",
                15:"fifteenth",
                16:"sixteenth",
                17:"seventeenth",
                18:"eighteenth",
                19:"nineteenth",
                20:"twentieth",
                30:"thirtieth"
            }
            #endregion value aliasing
            #region associate numeric with written form
            if day<=20 or day==30:
                day= ending_pronounciation[day]
            elif 20<day<30:
                day= f"twenty {ending_pronounciation[day-20]}"
            else:
                day="thirty first"
            #endregion associate numeric with written form
            if international is True:
                return f"{hour}:{minute}:{second}.{microsecond}"+\
                    f" on the {day} day of {month_alias[month]}, {year}"
            return f"{hour-12 if 12<hour else hour}:{minute}:{second}.{microsecond}"+\
                f" {'AM' if hour<12 else 'PM'} on the {day} day of {month_alias[month]}, {year}"
        #region format month,day,hour,minute,second
        month= f"0{month}" if len(f"{month}")<2 else month
        day= f"0{day}" if len(f"{day}")<2 else day
        hour= f"0{hour}" if len(f"{hour}")<2 else hour
        minute= f"0{minute}" if len(f"{minute}")<2 else minute
        second= f"0{second}" if len(f"{second}")<2 else second
        #endregion format month,day,hour,minute,second
        if international is True:
            return f"{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond}"
        return f"{year}-{month}-{day} "+\
            f"{f'0{int(hour)-12}' if 12<int(hour) else hour}:{minute}:{second}.{microsecond} "+\
            f"{'AM' if int(hour)<12 else 'PM'}"
    @classmethod
    def utc_offset(cls, /)-> float:
        """Returns the Universal Time Coordinated format"""
        utc_time:float= datetime.timestamp(datetime.utcnow())
        lan_time:float= cls.timestamp()
        return timestamp_offset(lan_time,utc_time)
    @classmethod
    def now(cls, international:bool=True, written:bool=False)-> str:
        """Returns the current time, does NOT return the date"""
        return cls.read_timestamp(
                cls.timestamp(),
                international=international,written=written
            ).split(" ",1)[1]
    def __init__(self,international:bool=True,written:bool=True)-> NoneType:
        self.international:bool= True if international is True else False
        self.written:bool= True if written is True else False
    def __repr__(self) -> str:
        if self.international is False and self.written is False:
            return "Month-Day-Year 12Hour:Minute:Second.Microsecond (AM/PM) UTC(+/-)HoursOffset"
        elif self.international is True and self.written is False:
            return "Year-Month-Day 24Hour:Minute:Second.Microsecond UTC(+/-)HoursOffset"
        elif self.international is False and self.written is True:
            return "12Hour:Minute:Second.Microsecond (AM/PM)"+\
                " UTC(+/-)HoursOffset on the nDayth day of wMonth, Year"
        elif self.international is True and self.written is True:
            return "24Hour:Minute:Second.Microsecond"+\
                " UTC(+/-)HoursOffset on the nDayth day of wMonth, Year"

def timestamp_offset(snowflake_a:float, snowflake_b:float)-> str:
    """Calculates the time offsets between 2 dates in hours"""
    if not isinstance(snowflake_a,float):
        raise TypeError("Inappropriate argument type for snowflake_a.")
    elif not isinstance(snowflake_b,float):
        raise TypeError("Inappropriate argument type for snowflake_b.")
    snowflake_a= datetime.fromtimestamp(snowflake_a)
    snowflake_b= datetime.fromtimestamp(snowflake_b)
    offset= f"+{snowflake_a-snowflake_b}" \
        if snowflake_b<snowflake_a \
        else f"-{snowflake_b-snowflake_a}"
    offset_direction= offset[:1]
    hour,minute,second=offset[1:].split(":")
    second, microsecond= second.split(".")
    if microsecond.startswith(("5","6","7","8","9")):
        second=int(second)+1
        microsecond=0
        if second==60:
            second=0
            minute=int(minute)+1
        if minute==60:
            minute=0
            hour=int(hour)+1
        if hour==24:
            hour=0
            offset_direction="+"
        return f"UTC{offset_direction}{hour}"
    return f"UTC{offset_direction}{hour}"
