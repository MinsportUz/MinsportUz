from django.contrib import admin

from admin_panel.model import ministry, menu, question, external
from admin_panel.model import territorial
from admin_panel.model import settings
from admin_panel.model import sport
from admin_panel.model import event
from admin_panel.model import tender
from admin_panel.model import docs
from admin_panel.model import press_service
from admin_panel.model import vacancy
from admin_panel.model import service
from admin_panel.model import useful_link
from admin_panel.model import contact
from admin_panel.model import static
from admin_panel.model import user
from admin_panel.model import rating

# Register your models here.

# Ministry RELATED fields
admin.site.register(ministry.AboutMinistry)
admin.site.register(ministry.MinistryStat)
admin.site.register(ministry.MinistryStructure)
admin.site.register(ministry.Staff)
admin.site.register(ministry.Department)
admin.site.register(ministry.Organization)

# Territorial fields
admin.site.register(territorial.Region)
admin.site.register(territorial.District)

# Settings fields
admin.site.register(settings.MainPageSetting)
admin.site.register(settings.ContactSetting)
admin.site.register(settings.Typo)

# Sport fields
admin.site.register(sport.Stadion)
admin.site.register(sport.SportType)
admin.site.register(sport.Champion)

# Event fields
admin.site.register(event.Event)

# Tender fields
admin.site.register(tender.Tender)
admin.site.register(tender.TenderNotices)
admin.site.register(tender.TenderNoticesPhotos)
admin.site.register(tender.Type)

# Docs fields
admin.site.register(docs.Docs)
admin.site.register(docs.DocType)

# Press service fields
admin.site.register(press_service.News)
admin.site.register(press_service.NewsHashtag)
admin.site.register(press_service.NewsCategory)
admin.site.register(press_service.PhotoGallery)
admin.site.register(press_service.PhotoGalleryImage)
admin.site.register(press_service.VideoGallery)
admin.site.register(press_service.Press)
admin.site.register(press_service.PressArticleLink)
admin.site.register(press_service.FAQ)

# Vacancy fields
admin.site.register(vacancy.Vacancy)
admin.site.register(vacancy.Employment)
admin.site.register(vacancy.Education)

# Service fields
admin.site.register(service.Service)
admin.site.register(service.EmployeeRating)

# Useful link fields
admin.site.register(useful_link.UsefulLink)

# Contact fields
admin.site.register(contact.ContactType)
admin.site.register(contact.Contact)
admin.site.register(contact.Feedback)
admin.site.register(contact.WeekDay)
admin.site.register(contact.Reception)
admin.site.register(contact.ContactStat)

# Static fields
admin.site.register(static.StaticPage)
admin.site.register(static.StaticData)

# Menu fields
admin.site.register(menu.Menu)

# Quizz fields
admin.site.register(question.Quizz)
admin.site.register(question.Question)
admin.site.register(question.QuestionResult)

# Custom user
admin.site.register(user.CustomUser)

# ExternalImage
admin.site.register(external.ExternalImage)

# ExternalImage
admin.site.register(press_service.NewsSMedia)

# vote
admin.site.register(rating.Vote)
admin.site.register(rating.Subscribers)
admin.site.register(rating.UnicalCode)

admin.site.register(ministry.CarTypes)
admin.site.register(ministry.Cars)
admin.site.register(ministry.CarInfo)

admin.site.register(ministry.OrganizationType)