from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ToDoItem, ToDoList
from .forms import ToDoItemForm, ToDoListForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
import json
# Create your views here.

class ToDoListView(View):
    form_class = ToDoListForm

    def setup(self, request, *args, **kwargs):
        self.itemsList = ToDoList.objects.all()
        return super().setup(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        # items_select = ToDoList.objects.all().values('todoitem','id').aggregate(Count('todoitem'))
        # print(items_select)
        # for i in items_select:
            # print(i.todoitem.all())
        # print(ToDoItem.objects.get(pk=1).todoitem.all())
        alllist = ToDoList.objects.all().values("pk")
        al = [item['pk'] for item in alllist]
        ass = ToDoList.objects.filter(id__in=al)
        ff = ToDoItem.objects.values('todoitem').annotate(item_count=Count('todoitem'))
        print(ff)
        context = { 
            'items': self.itemsList,
            'form': self.form_class,
            'item_count': ff
        }
        return render(request, 'todoapp/todolist.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ToDoListForm(request.POST)
        if form.is_valid():
            ins = ToDoList(name=form.cleaned_data['name'], user=request.user)
            ins.save()
            inst = {
                'name': ins.name,
                'id': ins.pk,
                'user': ins.user.username,
            }
            return JsonResponse({"id": ins.pk,"name": ins.name, "user": ins.user.username, 'status':"200"})
        
        action = request.POST.getlist('action')
        if action[0] == 'delete':
            items_delete = str(request.POST['items-for-delete'])
            items_delete = items_delete.split("-")
            items_delete.pop()
            items_deleted = ToDoList.objects.filter(id__in=items_delete).delete()
            context = {
            'items': self.itemsList,
            'form': form,
            'item_deleted_count': items_deleted,
            }
            return JsonResponse({"count":items_deleted[0]})
        
        context = {
            'items': self.itemsList,
            'form': form,
        }
        return render(request, 'todoapp/todolist.html', context)


class ToDoListDetailsView(LoginRequiredMixin ,View):
    login_url = '/'
    form_class = ToDoItemForm
    template_name = 'todoapp/list_detail.html'

    def setup(self, request, pk, *args, **kwargs):
        self.todolist = get_object_or_404(ToDoList, pk=pk)
        self.todoitems = ToDoItem.objects.filter(todoitem=self.todolist)
        return super().setup(request, pk, *args, **kwargs)
    
    def get(self, request, pk, *args, **kwargs):
        form = self.form_class()
        context = {
            'items': self.todoitems,
            'todolist': self.todolist,
            'form': form,
            'id': self.todolist.id,
            'count_deleted': request.GET.get('d'),
            'count_updated': request.GET.get('u'),
        }
        return render(request, self.template_name, context)
    

    def post(self, request, pk, *args):
        # print(request.get_full_path())  django have a error only when send form with action, django cant gave me get_full_path().Django dosnt retuen response for a long time &
        action = request.POST.get("action")
        if action=="update" or action=="delete":
            item = request.POST.get("delete_item_id")
            next_url = request.POST.get('next')
            itm = get_object_or_404(ToDoItem, pk=item)
        if action=="delete":
            itm2 = itm.delete()
            return redirect(f'/details/{next_url}?d={itm2[0]}')
        elif action=='update':
            if itm.active:
                itm.active=False
            else:
                itm.active=True
            itm.save()
            return redirect(f'/details/{next_url}?u={1}')
        
        form = self.form_class(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data.get('description')
            newtodoitem =ToDoItem(title=title, description=description, user=request.user, todoitem=self.todolist)
            newtodoitem.save()
            # return JsonResponse({"id":newtodoitem.id, "title": newtodoitem.title, 'get_status_display': newtodoitem.get_status_display})
            context = {
                'items': self.todoitems,
                'todolist': self.todolist,
                'form': self.form_class,
            }
        else:
            context = {
                'items': self.todoitems,
                'todolist': self.todolist,
                'form': form,
                'msg': 'invalid form',
            }
        return render(request, self.template_name, context)
    

    # a view for active object without refresh page(with axios)
    # deactive this method and url and axios script in list_detail.html for use post method in ToDoListDetailsView class
def activeView(request, pk):
    item = get_object_or_404(ToDoItem, pk=pk)
    print(pk, item)
    item.active= True if item.active==False else False
    item.save()
    return redirect('/details/1')

def getData(request):
    if request.method == "POST":
        return JsonResponse({"s":"ok"})
    else:
        return render(request, 'todoapp/test2.html', {})


   # for when use delete one item. this for test
# def deleteItemView(request, id):
#     item = get_object_or_404(ToDoItem, pk=id)
#     next_u =request.get_full_path()
#     print(next_u)
#     item.delete()
#     return redirect('/')


   # for when use delete multiple item (delete action). this for test
# def deleteItem(request):
#     if request.method == 'POST':
#         items_selected = request.POST.getlist('item_check')
#         action = request.POST.getlist('test')
#         id_list = [int(item) for item in items_selected]
#         items = ToDoItem.objects.filter(id__in=id_list).delete()
#     return redirect('get list')   


   # for when use update  multiple item (update action). this for test
# def activeItems(id_list, action):
#     if action[0] == "active":
#         action = True
#     elif action[0] == 'deactive':
#         action = False
#     print(action)
#     # items = ToDoItem.objects.raw("UPDATE todoapp_todoitem SET active=true WHERE id IN (25, 26,)")
#     id_list = (1, 2)
#     action = True
#     ToDoItem.objects.raw("UPDATE todoapp_todoitem SET active=True WHERE id IN (1,2)")
#
#      return items


   # for when use update and delete  multiple item (update and delete action) this for test
# def testAction(request):
#     if request.method == 'POST':
#         items_selected = request.POST.getlist('item_check')
#         action =request.POST.getlist('test')
#         items = ToDoList.objects.all()
#         id_list = [int(item) for item in items_selected]
#
#         if action[0] == 'active':
#             action = True
#         elif action[0] == 'deactive':
#             action = False
#         elif action[0] == 'delete':
#             item = ToDoItem.objects.filter(id__in=id_list).delete()
#
#             context = {
#                 'item_deleted_count': item,
#                 'items': items,
#                 }
#             return render(request, 'todoapp/todolist.html', context)
#            
#         item = ToDoItem.objects.filter(id__in=id_list).update(active=action)
#         context = {
#                 'item_deleted_count': item,
#                 'items': items,
#                 }
#         return render(request, 'todoapp/todolist.html', context)
#     return redirect('get list')

