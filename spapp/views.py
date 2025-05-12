import os
import yfinance as yf
import plotly.graph_objects as go
import requests
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
import logging
from .forms import coll
from django.contrib import messages
from .models import Collection
from django.conf import settings
from datetime import datetime 
from django.http import JsonResponse



logger = logging.getLogger('operation')

# Create your views here.
def home(request):
    return render(request,'home.html')

def tetris(request):
    return render(request,'tetris.html')

def calculator(request):
    return render(request,'calculator.html')

def calendar(request):
    return render(request,'calendar.html')

def todolist(request):
    return render(request,'todolist.html')

def map(request):
    return render(request,'map.html')

def food(request):
    return render(request,'food.html')

def diary(request):
    return render(request,'diary.html')
    
def datamanage(request):
    data=Collection.objects.all()
    if(data!=''):
        return render(request,'datamanage.html', {'data': data} )
    else:
        return render(request,'home.html')

def insert(request):
    Collection.objects.defer('id',)
    if request.method=='POST':
        form=coll(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request,'Data inserted successfully')
                logger.info(f"Inserted ")
                return redirect('home')
            except:
                pass
    else:
        form=coll()
    return render(request,'register.html',{'form':form})

def update(request, id):
    data=Collection.objects.get(id=id)
    if request.method=='POST':
        Study_Name=request.POST['Study_Name']
        Study_Description=request.POST['Study_Description']
        Study_Phase=request.POST['Study_Phase']
        Sponser_Name=request.POST['Sponser_Name']

        data.Study_Name=Study_Name
        data.Study_Description=Study_Description
        data.Study_Phase=Study_Phase
        data.Sponser_Name=Sponser_Name
        data.save()
        messages.success(request,'Data updated successfully')
        logger.info(f"Updated")
        return redirect('home')
    return render(request,'update.html',{'data':data})

def delete(request):
    data = Collection.objects.all()
    if request.method=='POST':
        selected_studies=request.POST.getlist('selected_studies')
        if selected_studies:
            data.filter(id__in=selected_studies).delete()
            messages.success(request,'Data deleted successfully')
            return redirect('home')
    data = Collection.objects.all()
    return redirect('home')

def see(request, id):
    data=Collection.objects.filter(id=id).first()
    if data:
        context={
            'data':data,
        }   
        print(context)
    logger.info(f"Viewing Table")
    return render(request, 'viewdet.html',context)

expense_file = os.path.join(settings.BASE_DIR, 'expenses.txt')
balance_file = os.path.join(settings.BASE_DIR, 'balance.txt')
def read_expenses():
    expenses = []
    balance = 0      
    if os.path.exists(balance_file):
        with open(balance_file, 'r', encoding='utf-8') as file:
            balance = float(file.read().strip() or 0)  
    if os.path.exists(expense_file):
        with open(expense_file, 'r', encoding='utf-8') as file:
            for line in file:
                name, amount = line.strip().split('|')
                amount = float(amount)
                expenses.append((name, amount))
                balance -= amount
    return expenses, balance

def expense_tracker(request):
    expenses, balance = read_expenses()
    if request.method == 'POST':
        if 'set_balance' in request.POST:
            new_balance = request.POST.get('balance', '').strip()
            if new_balance.isdigit():
                with open(balance_file, 'w', encoding='utf-8') as file:
                    file.write(new_balance)
                return redirect('expense_tracker')     
        if 'reset' in request.POST:
            if os.path.exists(expense_file):
                os.remove(expense_file)
            if os.path.exists(balance_file):
                os.remove(balance_file)
            return redirect('expense_tracker')      
        if 'remove_expense' in request.POST:
            remove_index = int(request.POST.get('remove_expense'))
            expenses.pop(remove_index)
            with open(expense_file, 'w', encoding='utf-8') as file:
                for name, amount in expenses:
                    file.write(f'{name}|{amount}\n')
            return redirect('expense_tracker')     
        name = request.POST.get('name', '').strip()
        amount = request.POST.get('amount', '').strip()     
        if name and amount.isdigit():
            with open(expense_file, 'a', encoding='utf-8') as file:
                file.write(f'{name}|{amount}\n')
            return redirect('expense_tracker') 
    return render(request, 'expense.html', {'expenses': expenses, 'balance': balance})

def chatbot_response(message):
    responses = {
        "hello": "Hi there! How can I help you?",
        "how are you": "I'm just a bot, but I'm doing great! 😊",
        "bye": "Goodbye! Have a great day! 👋",
        "name": "I'm your friendly Django Chatbot.",
        "age": "I'm a computer program, I don't have an age.",
        "date": "I'm a computer program, I don't have a birthdate.",
        "time": "I'm a computer program, I don't have a watch.",
        "thanks": "You're welcome! 😊",
        "thank you": "You're welcome! 😊",
        "": "Please say something.",
        "weather": "I'm a computer program, I can't go outside. ☁️",
        "news": "I'm a computer program, I can't read newspapers. 📰",
        "music": "I'm a computer program, I can't listen to music. 🎵",
        "movie": "I'm a computer program, I can't watch movies. 🎥",
        
    } 
    message = message.lower()
    return responses.get(message, "I'm not sure how to respond to that. 🤔")

def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        bot_reply = chatbot_response(user_message)
        return JsonResponse({"reply": bot_reply})
    return render(request, "chatbot.html")

STOCKS = ["APPLE", "MSFT", "GOOGLE", "AMAZON", "TESLA"]
def fetch_stock_data(ticker):
    """Fetch historical stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo") 
    return hist

def stock_chart(request, symbol="AAPL"):
    """Render stock chart page."""
    if symbol not in STOCKS:
        symbol = "AAPL"  
    data = fetch_stock_data(symbol)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name=f"{symbol} Closing Price"))
    fig.update_layout(title=f"{symbol} Stock Prices (Last 1 Month)", xaxis_title="Date", yaxis_title="Price (USD)")
    chart_html = fig.to_html(full_html=False)
    return render(request, "stock.html", {"chart": chart_html, "stocks": STOCKS})

def stock_data_api(request, symbol="AAPL"):
    """API endpoint for fetching stock data."""
    if symbol not in STOCKS:
        return JsonResponse({"error": "Invalid stock symbol"}, status=400)
    data = fetch_stock_data(symbol)
    json_data = data["Close"].to_json()
    return JsonResponse({"symbol": symbol, "prices": json_data})


def weather(request):
    weather_data = None
    if request.method == "POST":
        city = request.POST.get("city")
        api_key = "2d84429e6228c1ff68904c8869c1dab9"  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"   
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            weather_data = {"error": "City not found!"}
    return render(request, "weather.html", {"weather": weather_data})
