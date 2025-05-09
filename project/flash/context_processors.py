from .models import Category

def categories_context(request):
    categories = Category.objects.filter(status=True).exclude(name="")
    return {'categories': categories}
