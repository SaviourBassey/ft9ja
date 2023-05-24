from django.shortcuts import render
from django.views import View
from .price_simulator import trade_simulator
from .models import UserTrades
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import UserBalance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.db.models import Q, Count, Sum, Case, When, FloatField
from django.template.loader import render_to_string

# Create your views here.

class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/admin-dashboard.html")
    

class GetTraderInfo(View):
    def get(self, request, *args, **kwargs):
        # Retrieve trader information for non-superuser users
        traders = User.objects.filter(is_superuser=False).annotate(
            total_trades=Count('usertrades'),
            successful_trades=Count('usertrades', filter=Q(usertrades__result='profit')),
            losing_trades=Count('usertrades', filter=Q(usertrades__result='loss')),
            success_rate=Case(
                When(total_trades__gt=0, then=(Count('usertrades', filter=Q(usertrades__result='profit')) / Count('usertrades')) * 100),
                default=0,
                output_field=FloatField()
            ),
            loss_rate=Case(
                When(total_trades__gt=0, then=(Count('usertrades', filter=Q(usertrades__result='loss')) / Count('usertrades')) * 100),
                default=0,
                output_field=FloatField()
            ),
            profit=Sum('usertrades__trade_amount')
        )

        # Render the trader information using a template
        trader_info_html = render_to_string('dashboard/trader_info.html', {'traders': traders})

        # Return the rendered trader information as JSON response
        return JsonResponse({'trader_info_html': trader_info_html})
    

class UserDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        UserTrades.objects.filter(user=request.user).delete()
        user_bal = UserBalance.objects.get(user=request.user)
        user_bal.account_balance = 100.0
        user_bal.save()
        current_bal = user_bal.account_balance
        context = {
            "current_bal":current_bal,
        }
        return render(request, "dashboard/user-dashboard.html", context)

class SimulateTradeView(View):
    def get(self, request, *args, **kwargs):
        try:
            trader = User.objects.exclude(is_superuser=True).get(username=request.user.username)
        except:
            trader = None
        print(trader)
        if trader:
            # generate a trade
            trade_amount, currency_pair, entry_price, exit_price, trade_type = trade_simulator()

            #Get the trader account balance and update
            user_bal = UserBalance.objects.get(user=trader)
            current_bal = user_bal.account_balance
            user_bal.account_balance = user_bal.account_balance + trade_amount
            user_bal.save()
            # if current_bal >= 0:
            #     user_bal.account_balance = user_bal.account_balance + trade_amount
            #     user_bal.save()


            # Add new trade record for the trader
            if user_bal.account_balance > current_bal:
                UserTrades.objects.create(user=trader, new_bal=user_bal.account_balance, result="profit", trade_amount=trade_amount, currency_pair=currency_pair, exit_point=exit_price, entry_point=entry_price, trade_type=trade_type)
            else:
                UserTrades.objects.create(user=trader, new_bal=user_bal.account_balance, result="loss", trade_amount=trade_amount, currency_pair=currency_pair, exit_point=exit_price, entry_point=entry_price, trade_type=trade_type)

            # Update the 3 most recent trades
            recent_trades = UserTrades.objects.all().order_by("-timestamp")[:3]

            # Convert the QuerySet to a list of dictionaries
            trades_list = [model_to_dict(trade) for trade in recent_trades]
            
            # To get the price difference after a trade
            timestamp = []
            price_difference = []
            for trade in UserTrades.objects.filter(user=request.user):
                price_difference.append(trade.new_bal)
                timestamp.append(trade.formatted_timestamp())
            
            data = {
                "status":"success",
                "recent_trades":trades_list,
                "bal": user_bal.account_balance,
                "timestamp":timestamp,
                "price_difference":price_difference
            }
        else:
            data = {
                "status":"failed",
            }
        return JsonResponse(data)
