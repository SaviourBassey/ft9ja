from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("admin-dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard_view"),
    path("user-dashboard/", views.UserDashboardView.as_view(), name="user_dashboard_view"),
    path("place-trade/", views.SimulateTradeView.as_view(), name="simulate_trade_view"),
    path("get-trader-info/", views.GetTraderInfo.as_view(), name="get_trader_info_view")
]
