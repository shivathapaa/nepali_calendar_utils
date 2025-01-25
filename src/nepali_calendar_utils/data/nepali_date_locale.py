from dataclasses import dataclass
from enum import Enum

class NameFormat(Enum):
    FULL = "full"
    MEDIUM = "medium"
    SHORT = "short"

class NepaliDateFormatStyle(Enum):
    FULL = "full"               # Monday, Asar 21, 2024 or सोमबार, असार २१, २०२४
    LONG = "long"               # Asar 21, 2024 or असार २१, २०२४
    MEDIUM = "medium"           # 2024 Asar 21 or २०२४ असार २१
    SHORT_MDY = "short_mdy"     # 06/21/2024 or ०६/२१/२०२४
    SHORT_YMD = "short_ymd"     # 2024/06/21 or २०२४/०६/२१
    COMPACT_MDY = "compact_mdy" # 06/21/24 or ०६/२१/२४
    COMPACT_YMD = "compact_ymd" # 24/06/21 or २४/०६/२१

@dataclass(frozen=True)
class NepaliWeekdayName:
    short: str
    medium: str
    full: str

@dataclass(frozen=True)
class NepaliMonthName:
    short: str
    full: str

nepali_months = [
    NepaliMonthName(short="बै", full="बैशाख"),
    NepaliMonthName(short="जे", full="जेठ"),
    NepaliMonthName(short="अ", full="असार"),
    NepaliMonthName(short="सा", full="साउन"),
    NepaliMonthName(short="भ", full="भदौ"),
    NepaliMonthName(short="अ", full="असोज"),
    NepaliMonthName(short="का", full="कार्तिक"),
    NepaliMonthName(short="मं", full="मंसिर"),
    NepaliMonthName(short="पु", full="पौष"),
    NepaliMonthName(short="मा", full="माघ"),
    NepaliMonthName(short="फा", full="फाल्गुन"),
    NepaliMonthName(short="चै", full="चैत"),
]

nepali_months_in_english = [
    NepaliMonthName(short="Bai", full="Baisakh"),
    NepaliMonthName(short="Jes", full="Jestha"),
    NepaliMonthName(short="Asa", full="Asar"),
    NepaliMonthName(short="Shr", full="Shrawn"),
    NepaliMonthName(short="Bha", full="Bhadra"),
    NepaliMonthName(short="Aso", full="Asoj"),
    NepaliMonthName(short="Kar", full="Kartik"),
    NepaliMonthName(short="Man", full="Mangsir"),
    NepaliMonthName(short="Pou", full="Poush"),
    NepaliMonthName(short="Mag", full="Magh"),
    NepaliMonthName(short="Pha", full="Falgun"),
    NepaliMonthName(short="Chai", full="Chaitra"),
]

nepali_weekdays = [
    NepaliWeekdayName(short="आ", medium="आईत", full="आईतबार"),
    NepaliWeekdayName(short="सो", medium="सोम", full="सोमबार"),
    NepaliWeekdayName(short="मं", medium="मंगल", full="मंगलबार"),
    NepaliWeekdayName(short="बु", medium="बुध", full="बुधबार"),
    NepaliWeekdayName(short="बि", medium="बिहि", full="बिहिबार"),
    NepaliWeekdayName(short="शु", medium="शुक्र", full="शुक्रबार"),
    NepaliWeekdayName(short="श", medium="शनि", full="शनिबार"),
]

english_weekdays = [
    NepaliWeekdayName(short="S", medium="Sun", full="Sunday"),
    NepaliWeekdayName(short="M", medium="Mon", full="Monday"),
    NepaliWeekdayName(short="T", medium="Tue", full="Tuesday"),
    NepaliWeekdayName(short="W", medium="Wed", full="Wednesday"),
    NepaliWeekdayName(short="T", medium="Thu", full="Thursday"),
    NepaliWeekdayName(short="F", medium="Fri", full="Friday"),
    NepaliWeekdayName(short="S", medium="Sat", full="Saturday"),
]

english_months_in_english = [
    NepaliMonthName(short="Jan", full="January"),
    NepaliMonthName(short="Feb", full="February"),
    NepaliMonthName(short="Mar", full="March"),
    NepaliMonthName(short="Apr", full="April"),
    NepaliMonthName(short="May", full="May"),
    NepaliMonthName(short="Jun", full="June"),
    NepaliMonthName(short="Jul", full="July"),
    NepaliMonthName(short="Aug", full="August"),
    NepaliMonthName(short="Sep", full="September"),
    NepaliMonthName(short="Oct", full="October"),
    NepaliMonthName(short="Nov", full="November"),
    NepaliMonthName(short="Dec", full="December"),
]

english_months_in_nepali = [
    NepaliMonthName(short="जन", full="जनवरी"),
    NepaliMonthName(short="फेब्रु", full="फेब्रुअरी"),
    NepaliMonthName(short="मार्च", full="मार्च"),
    NepaliMonthName(short="अप्रि", full="अप्रिल"),
    NepaliMonthName(short="मे", full="मे"),
    NepaliMonthName(short="जुन", full="जुन"),
    NepaliMonthName(short="जुला", full="जुलाई"),
    NepaliMonthName(short="अग", full="अगस्ट"),
    NepaliMonthName(short="सेप्ट", full="सेप्टेम्बर"),
    NepaliMonthName(short="अक्टो", full="अक्टोबर"),
    NepaliMonthName(short="नोभे", full="नोभेम्बर"),
    NepaliMonthName(short="डिसे", full="डिसेम्बर"),
]

class NepaliCalendarUtilsLang(Enum):
    ENGLISH = {
        "weekdays": english_weekdays,
        "months": nepali_months_in_english,
        "english_months": english_months_in_english
    }

    NEPALI = {
        "weekdays": nepali_weekdays,
        "months": nepali_months,
        "english_months": english_months_in_nepali
    }

    def __init__(self, values):
        self.weekdays = values["weekdays"]
        self.months = values["months"]
        self.english_months = values["english_months"]
        
@dataclass(frozen=True)
class NepaliDateLocale:
    language: NepaliCalendarUtilsLang = NepaliCalendarUtilsLang.ENGLISH
    date_format: NepaliDateFormatStyle = NepaliDateFormatStyle.LONG
    week_day_name: NameFormat = NameFormat.FULL
    month_name: NameFormat = NameFormat.FULL
