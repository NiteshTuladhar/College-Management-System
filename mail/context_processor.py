from .models import ContactUs

def messagecount(request):
    messagecount = ContactUs.objects.filter(checked=False).count()
    print(messagecount)
    return {'count': messagecount}