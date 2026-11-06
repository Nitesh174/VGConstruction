import json

import anthropic
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import ContactEnquiry


def home(request):
    return render(request, "core/home.html")


def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        service = request.POST.get("service", "other")
        budget = request.POST.get("budget", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not phone:
            messages.error(request, "Name and phone number are required.")
            return redirect("home")

        valid_services = dict(ContactEnquiry.SERVICE_CHOICES)

        if service not in valid_services:
            service = "other"

        ContactEnquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            service=service,
            budget=budget,
            message=message,
        )

        messages.success(
            request,
            "Thank you! Your enquiry has been submitted successfully."
        )
        return redirect("home")

    return redirect("home")


# ---------------- AI CHAT ----------------

SYSTEM_PROMPT = """You are the virtual assistant for VG Construction & Interior Design (Patna, Bihar).
Services: house construction, interior design, architectural planning, renovation.
Directors: Vijay Singh (CEO, 8877338601) and Ganesh Kumar (Director, 7004279605).
Reply in the same language the visitor uses (Hindi, English or Hinglish). Keep answers short and friendly.
Ask about plot size, location, budget and timeline. Never quote exact prices or promise timelines;
say the team will give a proper estimate after discussion. Encourage the visitor to share their
name and phone number or use the enquiry form below."""


@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        history = data.get("messages", [])[-10:]
        history = [
            {"role": m["role"], "content": str(m["content"])[:1000]}
            for m in history
            if m.get("role") in ("user", "assistant")
        ]
        if not history or history[0]["role"] != "user":
            return JsonResponse({"reply": "Please type a message."}, status=400)

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=history,
        )
        return JsonResponse({"reply": response.content[0].text})
    except Exception as e:
        print("CHAT ERROR:", e)
        return JsonResponse(
            {"reply": "Sorry, kuch problem aa gayi. Kripya WhatsApp par sampark karein: 7004279605"},
            status=500,
        )