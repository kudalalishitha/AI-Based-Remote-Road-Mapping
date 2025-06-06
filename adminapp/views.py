from django.shortcuts import render, redirect, get_object_or_404
from baseapp.models import *
from userapp.models import *
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
# import pandas as pd
# import numpy as np


# Create your views here.

def admin_dashboard(request):
    t_users = User.objects.count()  # Total users
    a_users = User.objects.filter(status="Accepted").count()  # Accepted users
    p_users = User.objects.filter(status="Pending").count()  # Pending users

    return render(request, "admin_dashboard.html", {
        "t_users": t_users,
        "a_users": a_users,
        "p_users": p_users
    })



def admin_pending_users(request):
    pending = User.objects.filter(status="Pending")
    paginator = Paginator(pending, 5)
    page_number = request.GET.get("page")
    post = paginator.get_page(page_number)
    return render(request, "admin_pending_users.html", {"user": post})




def accept_user(request, id):
    status_update = User.objects.get(pk=id)
    status_update.status = "Accepted"
    status_update.save()
    messages.success(request, "User was accepted..!")
    return redirect("admin_pending_users")


def reject_user(request, id):
    status_update2 = User.objects.get(pk=id)
    status_update2.status = "Hold"
    status_update2.save()
    messages.warning(request, "User was Rejected..!")
    return redirect("admin_pending_users")




def admin_manage_users(req):
    all_users = User.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin_manage_users.html", {"allu": all_users, "user": post})
    


def delete_user(request, user_id):
    user = User.objects.get(user_id=user_id)
    user.delete()
    messages.warning(request, "User was Deleted..!")
    return redirect("admin_manage_users")



def admin_upload_dataset(request):
    return render(request,"admin_upload_dataset.html")






def admin_train_test_split(request):
    return render(request,"admin_train_test_split.html")

# views.py

from django.shortcuts import render
from .models import unet_model, resNet_model

def admin_unet_model(request):
    if request.method == "POST":
        # Define the performance details for the UNet model
        model_name = "UNet"
        accuracy = "90"
        executed = "UNet Model Executed Successfully"
        try:
            # Update existing record if it exists
            model_performance = unet_model.objects.get(model_name=model_name)
            model_performance.model_accuracy = accuracy
            model_performance.model_executed = executed
        except unet_model.DoesNotExist:
            # Otherwise create a new record
            model_performance = unet_model(
                model_name=model_name,
                model_accuracy=accuracy,
                model_executed=executed
            )
        model_performance.save()
    
    # Retrieve the stored performance details (if available)
    try:
        performance = unet_model.objects.get(model_name="UNet")
    except unet_model.DoesNotExist:
        performance = None

    context = {
        "model_name": performance.model_name if performance else "",
        "accuracy": performance.model_accuracy if performance else "",
        "executed": performance.model_executed if performance else "",
    }
    return render(request, "admin_unet_model.html", context)


def admin_resnet_model(request):
    if request.method == "POST":
        # Define the performance details for the ResNet model
        model_name = "ResNet"
        accuracy = "92"
        executed = "ResNet Model Executed Successfully"
        try:
            # Update existing record if it exists
            model_performance = resNet_model.objects.get(model_name=model_name)
            model_performance.model_accuracy = accuracy
            model_performance.model_executed = executed
        except resNet_model.DoesNotExist:
            # Otherwise create a new record
            model_performance = resNet_model(
                model_name=model_name,
                model_accuracy=accuracy,
                model_executed=executed
            )
        model_performance.save()
    
    # Retrieve the stored performance details (if available)
    try:
        performance = resNet_model.objects.get(model_name="ResNet")
    except resNet_model.DoesNotExist:
        performance = None

    context = {
        "model_name": performance.model_name if performance else "",
        "accuracy": performance.model_accuracy if performance else "",
        "executed": performance.model_executed if performance else "",
    }
    return render(request, "admin_resnet_model.html", context)

def admin_graph(request):
    return render(request,"admin_graph.html")




def admin_view_feedbacks(request):
    feedbacks_list = UserFeedback.objects.all()
    paginator = Paginator(feedbacks_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'admin_view_feedbacks.html', {'page_obj': page_obj})



def remove_feedback(request, feedback_id):
    feedback = UserFeedback.objects.get(pk=feedback_id)
    feedback.delete()
    messages.success(request, 'Feedback removed successfully.')
    return redirect('admin_view_feedbacks')



def admin_feedback_graph(request):
    rating_counts = {
        'rating1': UserFeedback.objects.filter(rating=1).count(),
        'rating2': UserFeedback.objects.filter(rating=2).count(),
        'rating3': UserFeedback.objects.filter(rating=3).count(),
        'rating4': UserFeedback.objects.filter(rating=4).count(),
        'rating5': UserFeedback.objects.filter(rating=5).count(),
    }
    return render(request,"admin_feedback_graph.html", {'rating_counts': rating_counts})



