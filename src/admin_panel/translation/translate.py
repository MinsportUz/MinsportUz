from modeltranslation.translator import TranslationOptions, translator, register

from admin_panel.model.contact import WeekDay, ContactType
from admin_panel.model.docs import Docs, DocType
from admin_panel.model.event import Event
from admin_panel.model.menu import Menu
from admin_panel.model.ministry import AboutMinistry, MinistryStructure, MinistryStat, Staff, Department, Organization, \
    Cars, CarTypes, CarInfo, OrganizationType

# ========================Ministry RELATED model========================
from admin_panel.model.press_service import News, NewsHashtag, NewsCategory, PhotoGallery, VideoGallery, FAQ
from admin_panel.model.question import Quizz, Question
from admin_panel.model.service import Service
from admin_panel.model.settings import MainPageSetting, ContactSetting
from admin_panel.model.sport import Stadion, SportType, Champion
from admin_panel.model.static import StaticPage
from admin_panel.model.tender import Tender, Type, TenderNotices
from admin_panel.model.territorial import Region, RegionalDepartment, District
from admin_panel.model.useful_link import UsefulLink
from admin_panel.model.vacancy import Vacancy, Education, Employment


@register(AboutMinistry)
class AboutMinistryTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(MinistryStructure)
class MinistryStructureTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(MinistryStat)
class MinistryStatTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Staff)
class StaffTranslationOptions(TranslationOptions):
    fields = ('title', 'position', 'reception_days', 'work_history', 'duty',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'address',)


@register(Organization)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'address',)


# Territorial fields
@register(Region)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(RegionalDepartment)
class DepartmentRegionalTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(District)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title',)


# Settings fields
@register(MainPageSetting)
class MainPageSettingTranslationOptions(TranslationOptions):
    fields = (
        'logo_title', 'mobile_title', 'mobile_description',
    )


@register(ContactSetting)
class ContactSettingTranslationOptions(TranslationOptions):
    fields = (
        'address', 'bus_station', 'metro_station', 'working_days', 'notice',
    )


# Sport fields
@register(Stadion)
class StadionTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'address', 'host_team', 'established'
    )


@register(SportType)
class SportTypeTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(Champion)
class ChampionTranslationOptions(TranslationOptions):
    fields = (
        'title', 'competition', 'description', 'medal',
    )


# Tender fields
@register(Tender)
class TenderTranslationOptions(TranslationOptions):
    fields = (
        'title', 'organizer',
    )


@register(Type)
class TenderTypeTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Docs fields
@register(Docs)
class DocsTranslationOptions(TranslationOptions):
    fields = (
        'title', 'issued_by', 'law',
    )


@register(DocType)
class DocTypeTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Press service fields
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'short_description',
    )


@register(NewsHashtag)
class NewsHashtagTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(PhotoGallery)
class PhotoGalleryTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(VideoGallery)
class PhotoGalleryTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description',
    )


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description',
    )


# Vacancy fields
@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = (
        'title', 'about', 'tasks',
    )


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(Employment)
class EmploymentTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Service fields
@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Useful link fields
@register(UsefulLink)
class UsefulLinkTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description',
    )


# Static fields
@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = (
        'title', 'content',
    )


# Event fields
@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'address', 'event_place',
    )


# Menu fields
@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Quizz fields
@register(Quizz)
class QuizzTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Quizz fields
@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# WeekDay fields
@register(WeekDay)
class WeekDayTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# User contacts
@register(ContactType)
class ContactTypeTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


# Tender Notices fields

@register(TenderNotices)
class TenderNoticesTranslationOptions(TranslationOptions):
    fields = (
        'title', 'address', 'land_area', 'size', 'status',
    )


# Car fields
@register(Cars)
class CarsTranslationOptions(TranslationOptions):
    fields = (
        'model', 'comment',
    )


@register(CarTypes)
class CarTypesTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )


@register(CarInfo)
class CarInfoTranslationOptions(TranslationOptions):
    fields = (
        'title', 'content',
    )


# Organization Type fields
@register(OrganizationType)
class OrganizationTypeTranslationOptions(TranslationOptions):
    fields = (
        'title',
    )