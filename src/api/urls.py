from django.urls import path, include
from rest_framework import routers

from api import search

router = routers.DefaultRouter()
# Importing models
from api.about import views as about
from api.settings import views as site
from api.news import views as news
from api.gallery import views as gallery
from api.event import views as event
from api.sport import views as sport
from api.docs import views as docs
from api.tender import views as tender
from api.service import views as service
from api.quizz import views as quizz
from api.contact import views as contact
from api.search import views as search
from api.static import views as static
from api.typo import views as typo
from api.rating import views as rating
from api.auth import views as auth
from api.index import views as index
from api.vacancy import views as vacancy
from api.menu import views as menu

# Settings
router.register(r'site-contact', site.SiteContactView, basename='site-contact-api')

# Index
router.register(r'header', site.HeaderView, basename='header-api')
router.register(r'footer', site.FooterView, basename='footer-api')
router.register(r'top-news', news.IndexNewsListView, basename='top-news-api')
router.register(r'top-news-medium', news.IndexNewsLongListView, basename='top-news-medium-api')
router.register(r'service', service.ServiceListView, basename='service-api')
router.register(r'contact-stat', contact.IndexContactView, basename='contact-stat-api')
router.register(r'top-event', event.IndexEventListView, basename='top-event-api')
router.register(r'top-gallery', gallery.IndexPhotoListView, basename='top-gallery-api')
router.register(r'poster', site.PosterView, basename='poster-api')
router.register(r'top-quizz', quizz.QuizzView, basename='top-quiz-api')
router.register(r'link', site.UsefulLinkView, basename='link-api')

# About us page
router.register(r'about', about.AboutUsView, basename='about-api')
router.register(r'number_data_from_erp', about.IntegrationErpNumberDataView, basename='number_data_from_erp-api')

router.register(r'staff-list', about.StaffListView, basename='filter-staff-api')
router.register(r'structure', about.StructureView, basename='structure-api')
router.register(r'visitor', about.VisitorView, basename='visitor-api')

# Department & Organization
router.register(r'all-department', about.AllDepartmentView, basename='all-department-api')
router.register(r'department', about.DepartmentView, basename='department-api')
router.register(r'organizations', about.OrganizationView, basename='organization-api')
router.register(r'organization_type', about.OrganizationTypeView, basename='organization_type-api')

# Vacancy
router.register(r'vacancy', about.VacancyView, basename='vacancy-api')

# All staff and leaders
router.register(r'leader', about.StaffView, basename='leader-api')
router.register(r'leader-region', about.StaffRegionView, basename='leader-region-api')
router.register(r'leader-organization', about.StaffOrganizationView, basename='leader-organization-api')
router.register(r'leader-central', about.StaffCentralView, basename='leader-central-api')

# Press API
router.register(r'news', news.NewsListView, basename='news-api')
router.register(r'news-integration', news.NewsIntegration, basename='news-api-integration')
router.register(r'news-region', news.NewsRegionView, basename='news-region-api')
router.register(r'news-header', news.HeaderNewsListView, basename='news-header-api')
router.register(r'news-category', news.NewsCategoryView, basename='news-category-api')
router.register(r'news-hashtag', news.NewsHashtagView, basename='news-hashtag-api')
router.register(r'main-news', news.MainNewsListView, basename='main-api')
router.register(r'press', news.PressListView, basename='press-api')
router.register(r'faq', news.FAQListView, basename='faq-api')

# Static page
router.register(r'static', static.StaticView, basename='static-api')
router.register(r'static_data', static.StaticDataView, basename='static_data-api')

# Gallery
router.register(r'photo', gallery.PhotoListView, basename='photo-api')
router.register(r'video', gallery.VideoListView, basename='video-api')

# Event
router.register(r'event', event.EventListView, basename='event-api')

# Sport
router.register(r'stadion', sport.StadionListView, basename='sport-api')
router.register(r'champion', sport.ChampionView, basename='champion-api')
router.register(r'champion-list', sport.ChampionListView, basename='champion-list-api')

# Docs
router.register(r'docs', docs.DocsListView, basename='docs-api')
router.register(r'doc-type', docs.DocTypeView, basename='doc-type-api')

# Tender
router.register(r'tender', tender.TenderListView, basename='tender-api')
router.register(r'tender-notices', tender.TenderNoticesView, basename='tender-not-api')

# Quizz
router.register(r'quizz', quizz.QuizzListView, basename='quizz-api')

# Typo
router.register(r'typo', typo.TypoView, basename='typo-api')

# Contact
router.register(r'contact', contact.ContactView, basename='contact-api')
router.register(r'feedback', contact.FeedbackView, basename='feedback-api')
# router.register(r'get_stats', contact.GetStatsView, basename='get-feedback-api')
router.register(r'reception', contact.ReceptionView, basename='reception-api')
router.register(r'appeal', contact.AppealView, basename='appeal-api')
router.register(r'car-info', about.CarInfoView, basename='car_info-api')

# Region
router.register(r'regions', site.RegionView, basename='region-api')
router.register(r'districts', site.DistrictView, basename='district-api')
router.register(r'employee-rating', service.EmployeeRatingModalViewSet, basename='employee_rating-api')
router.register(r'regiondepartment', site.RegionDepartmentView, basename='regiondepartment-api')

# Rating API
rating_router = routers.DefaultRouter()
rating_router.register(r'rating-filter', service.EmployeeRatingModalViewSet, basename='rating-filter-api')
rating_router.register(r'rating-department_grade', service.EmployeeRatingModalViewSet,
                       basename='rating-department_grade-api')
rating_router.register(r'rating-structura_department', service.EmployeeRatingModalViewSet,
                       basename='rating-structura_department-api')

# Vote API
vote_router = routers.DefaultRouter()
vote_router.register(r'participants', rating.ParticipantsViewSet, basename='vote-participants-api')
vote_router.register(r'evolution_criteria', rating.EvolutionCriteriaViewSet, basename='vote-evolution_criteria-api')
vote_router.register(r'participants_vote', rating.VoteViewSet, basename='vote-participants_vote-api')
vote_router.register(r'participants_filter', rating.ParticipantsFilterViewSet, basename='vote-participants_filter-api')
vote_router.register(r'bot_link', rating.BotLinkViewSet, basename='vote-bot_link-api')
vote_router.register(r'department', about.DepartmentView, basename='vote-department-api')
vote_router.register(r'organizations', about.OrganizationView, basename='vote-organization-api')
vote_router.register(r'regions', site.RegionView, basename='vote-region-api')
vote_router.register(r'districts', site.DistrictView, basename='vote-district-api')

# Admin panel API
adm_router = routers.DefaultRouter()
adm_router.register(r'users', auth.UserView, basename='adm-users-api')
adm_router.register(r'role', auth.GroupView, basename='adm-role-api')
adm_router.register(r'permission', auth.PermissionView, basename='adm-permission-api')
adm_router.register(r'about', about.AdmAboutMinistryView, basename='adm-about-api')
adm_router.register(r'structure', about.AdmMinistryStructureView, basename='adm-structure-api')
adm_router.register(r'staff', about.AdmMinistryStaffView, basename='adm-staff-api')
adm_router.register(r'stat', about.AdmMinistryStatView, basename='adm-stat-api')
adm_router.register(r'department', about.AdmMinistryDepartmentView, basename='adm-department-api')
adm_router.register(r'organization', about.AdmMinistryOrganizationView, basename='adm-organization-api')
adm_router.register(r'organization_type', about.AdmOrganizationTypeView, basename='adm-organization_type-api')
adm_router.register(r'index', index.IndexView, basename='adm-index-api')
adm_router.register(r'vacancy', vacancy.AdmVacancyView, basename='adm-vacancy-api')
adm_router.register(r'education', vacancy.AdmEducationView, basename='adm-education-api')
adm_router.register(r'employment', vacancy.AdmEmploymentView, basename='adm-employment-api')
adm_router.register(r'service', service.AdmServiceView, basename='adm-service-api')
adm_router.register(r'doc_type', docs.AdmDocTypeView, basename='adm-doc_type-api')
adm_router.register(r'docs', docs.AdmDocsView, basename='adm-docs-api')
adm_router.register(r'stadion', sport.AdmStadionView, basename='adm-station-api')
adm_router.register(r'sport_type', sport.AdmSportTypeView, basename='adm-sport_type-api')
adm_router.register(r'champion', sport.AdmChampionView, basename='adm-champion-api')
adm_router.register(r'news', news.AdmNewsView, basename='adm-news-api')
adm_router.register(r'news_media', news.AdmNewsSMediaView, basename='adm-news_media-api')
adm_router.register(r'news_image', news.AdmMediaImageView, basename='adm-news_image-api')
adm_router.register(r'news_hashtag', news.AdmNewsHashtagView, basename='adm-news_hashtag-api')
adm_router.register(r'news_category', news.AdmNewsCategoryView, basename='adm-news_category-api')
adm_router.register(r'photo_gallery', news.AdmPhotoGalleryView, basename='adm-photo_gallery-api')
adm_router.register(r'photo_gallery_image', news.AdmPhotoGalleryImageView, basename='adm-photo_gallery_image-api')
adm_router.register(r'video_gallery', news.AdmVideoGalleryView, basename='adm-video_gallery-api')
adm_router.register(r'press', news.AdmPressView, basename='adm-press-api')
adm_router.register(r'press_article', news.AdmPressArticleLinkView, basename='adm-press_article-api')
adm_router.register(r'faq', news.AdmFAQView, basename='adm-faq-api')
adm_router.register(r'external_image', gallery.AdmExternalImageView, basename='adm-external_image-api')
adm_router.register(r'event', event.AdmEventView, basename='adm-event-api')
adm_router.register(r'tender', tender.AdmTenderView, basename='adm-tender-api')
adm_router.register(r'tender-type', tender.AdmTenderTypeView, basename='adm-tender-type-api')
adm_router.register(r'tender-notices', tender.AdmTenderNoticesView, basename='adm-tender-notices-api')
adm_router.register(r'tender-photos', tender.AdmTenderNoticesPhotosView, basename='adm-tender-notices-photos-api')
adm_router.register(r'regions', site.AdmRegionView, basename='adm-region-api')
adm_router.register(r'districts', site.AdmDistrictView, basename='adm-district-api')
adm_router.register(r'quizz', quizz.AdmQuizzView, basename='adm-quizz-api')
adm_router.register(r'question', quizz.AdmQuestionView, basename='adm-question-api')
adm_router.register(r'link', site.AdmUsefulLinkView, basename='adm-link-api')
adm_router.register(r'quizz-result', quizz.AdmQuestionResultView, basename='adm-quizz-result-api')
adm_router.register(r'main-page', site.AdmMainPageSettingView, basename='adm-main-page-api')
adm_router.register(r'contact', site.AdmContactSettingView, basename='adm-contact-api')
adm_router.register(r'typo', site.AdmTypoView, basename='adm-typo-api')
adm_router.register(r'week-day', contact.AdmWeekDayView, basename='adm-week_day-api')
adm_router.register(f'reception', contact.AdmReceptionView, basename='adm-reception-api')
adm_router.register(r'menu', menu.AdmMenuView, basename='adm-menu-api')
adm_router.register(r'static-page', menu.AdmStaticPageView, basename='adm-static_page-api')
adm_router.register(r'static-data', static.AdmStaticDataView, basename='adm-static_data-api')
adm_router.register(r'regional-department', site.AdmRegionDepartmentView, basename='adm-regional_department-api')
adm_router.register(r'contact-type', contact.AdmContactTypeView, basename='adm-contact_type-api')
adm_router.register(r'appeal', contact.AdmContactView, basename='adm-appeal-api')
adm_router.register(r'feedback', contact.AdmFeedBackView, basename='adm-feedback-api')
adm_router.register(r'cars', about.AdmCarsView, basename='adm-cars-api')
adm_router.register(r'car-info', about.AdmCarInfoView, basename='adm-car_info-api')
adm_router.register(r'search-hashtag', news.NewsHashtagSearchView, basename='search-hashtag-api')
adm_router.register(r'upload_files', docs.AdmUploadFilesView, basename='adm-upload_files-api')

bot_router = routers.DefaultRouter()
bot_router.register(r'bot_db', rating.SubscribersViewSet, basename='bot_db-api')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search.Search.as_view(), name='search-api'),
    path('search-date/', search.SearchWithDate.as_view(), name='search-date-api'),
    path('upload/', search.ImageUploadView.as_view(), name='image-upload'),
    path('rating/', include(rating_router.urls)),
    path('vote/', include(vote_router.urls)),
    path('bot/', include(bot_router.urls)),
    path('login/', auth.LogInView.as_view(), name='login-api'),
    path('site-adm/', include(adm_router.urls)),
]
