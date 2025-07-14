from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class RoomName(models.Model):
    name = models.CharField(max_length=100, unique=True)
    participant = models.ManyToManyField(User, related_name='chat_groups', blank=True)

    def __str__(self):
        return self.name

    def count_of_participants(self):
        return self.participant.count()
    

class PrivateChat(models.Model):
    user_1 = models.ForeignKey(User, related_name="chats_as_user1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="chats_as_user2", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user_1", "user_2"]

    def __str__(self):
        return f'chat for {self.user_1} and {self.user_2}'
    
    def participants(self):
        return [self.user_1, self.user_2]

class GroupMessage(models.Model):
    room_name = models.ForeignKey(RoomName, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.author.username}: {self.content[:10]}"

class PrivateMessage(models.Model):
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.author.username}: {self.content[:10]}"
    

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/avatar/')
    about_user = models.TextField(blank=True)
    birthday = models.DateField()




