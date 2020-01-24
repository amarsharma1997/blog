from django.contrib import admin
from posts.models import post,topic,review,comment,commentReply
# Register your models here.

class postAdmin(admin.ModelAdmin):
    list_display=['title','updated','timestamp']
    search_fields=['title','content']
    class Meta:
        model=post


admin.site.register(commentReply)
admin.site.register(post,postAdmin)
admin.site.register(topic)
admin.site.register(review)
admin.site.register(comment)