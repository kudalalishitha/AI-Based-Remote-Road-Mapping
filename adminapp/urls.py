from adminapp import views as views
from django.urls import path


urlpatterns = [
 
    path('dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('pending/users/',views.admin_pending_users,name="admin_pending_users"),
    path('accept/user/<int:id>', views.accept_user, name = 'admin_accept_user'),
    path('reject/user/<int:id>', views.reject_user, name = 'admin_reject_user'),
    path('manage/users/',views.admin_manage_users,name="admin_manage_users"),
    path('delete/user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('upload/dataset/',views.admin_upload_dataset,name="admin_upload_dataset"),
    path('train/test/split',views.admin_train_test_split,name="admin_train_test_split"),
    path('resnet',views.admin_resnet_model,name="admin_resnet_model"),
    path('unet',views.admin_unet_model,name="admin_unet_model"),
    path('graph',views.admin_graph,name="admin_graph"),
    path('view/feedbacks/', views.admin_view_feedbacks, name='admin_view_feedbacks'),
    path('remove/feedback/<int:feedback_id>/', views.remove_feedback, name='remove_feedback'),
    path('feedback-graph/',views.admin_feedback_graph,name="admin_feedback_graph"),




   
    
]