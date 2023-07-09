from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ToDoList(models.Model):
    name = models.CharField(max_length=100, help_text="name of list")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # tag = models.CharField(max_length=)

    def __str__(self):
        return self.name

class ToDoItem(models.Model):
    title = models.CharField(max_length=100, help_text="Item name")
    description = models.CharField(max_length=400, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todoitem = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    status_list = [('p','prcessing'),
                   ('e', 'exepted',),
                   ('c', 'cheking'),
                   ('d','done'),]
    status = models.CharField(max_length=1 ,choices=status_list, default='p')

    def get_active_items(self):
        if self.active == True:
            return object
    
    def __str__(self):
        return "{0} : {2} => {1}".format(self.user.username, self.todoitem.name, self.title)