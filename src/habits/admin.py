from django.contrib import admin

# Register your models here.
from .models import HabitPost, HabitTrack, HabitEvent, JustRecurrence, PostComment, PostLike, CommentLike

admin.site.register(HabitPost)
admin.site.register(HabitTrack)
admin.site.register(HabitEvent)

admin.site.register(JustRecurrence)




admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
