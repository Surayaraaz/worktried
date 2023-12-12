
from .models import employnav,Employs,NotificationEmploy,companylogo
def dynamic_nav(request):
    # Retrieve the navigation items
    try:
        a=companylogo.objects.all()
        s=employnav.objects.all()
        employ_obj=Employs.objects.get(admin=request.user.id)
        

        notification1=NotificationEmploy.objects.filter(employ_id=employ_obj.id)
        notifications1=NotificationEmploy.objects.filter(employ_id=employ_obj.id).count()
    # You can perform any additional logic or filtering here if needed
    except Employs.DoesNotExist:
        # Handle the case where the Employ object doesn't exist
        employ_obj = None
        notifications1 = 0
        notification1 = 0
    # Return the navigation items in a dictionary
    return {'s': s,'notifications1':notifications1,'notification1':notification1,'a':a}

