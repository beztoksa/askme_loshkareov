from app.models import Tag

def tag_context(request):

    popular_tags = Tag.objects.popular_tags()
    return {'popular_tags': popular_tags}
def is_login(request):
    is_login = True
    return {'is_login': is_login}
