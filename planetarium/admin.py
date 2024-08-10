from django.contrib import admin

from planetarium.models import (
    PlanetariumDome,
    AstronomyShow,
    ShowTheme,
    ShowSession,
    Ticket,
    Reservation
)

admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(Ticket)
admin.site.register(Reservation)
