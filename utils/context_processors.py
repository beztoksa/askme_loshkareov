from app.models import Tag, Profile

def tag_context(request):

    popular_tags = Tag.objects.popular_tags()
    return {'popular_tags': popular_tags}
def is_login(request):
    is_login = True
    return {'is_login': is_login}
def top_profile(request):
    popular_profiles = Profile.objects.popular_profiles()
    return {'popular_profiles': popular_profiles}
