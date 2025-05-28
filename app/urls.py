"""
URL configuration for askme_loshkareov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tkinter.font import names

from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
#from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="register"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('tag/<tag_name>', views.tag, name="tag"),
    path('ask/', views.ask, name="ask"),
    path('logout/', views.logout, name="logout"),
    path('<question_id>/qlike',views.QuestionRating, name="QuestionRating" ),
    path('<answer_id>/alike',views.AnswerRating, name="AnswerRating" ),
    path('<question_id>/<answer_id>/correct',views.correct, name="correct"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
