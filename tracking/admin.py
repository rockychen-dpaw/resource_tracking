from django.conf import settings
from django.contrib.admin import ModelAdmin, register, AdminSite
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Device, LoggedPoint


@register(Device)
class DeviceAdmin(ModelAdmin):
    date_hierarchy = "seen"
    list_display = ("deviceid", "registration", "rin_display", "symbol", "district", "seen")
    list_filter = ("symbol", "district")
    search_fields = ("deviceid", "registration", "rin_display", "symbol", "district")
    readonly_fields = ("deviceid",)
    fieldsets = (
        ("Vehicle/Device details", {
            "description": """<p class="errornote">This is the live tracking database; 
            changes made to these fields will apply to the Device Tracking map in all 
            variants of the Spatial Support System.</p>
            """ if settings.PROD_SCARY_WARNING else "",
            "fields": ("deviceid", "district", ("symbol", "rin_number"), "registration")
        }),
        ("Crew Details", {
            "fields": (("current_driver", "current_callsign"),
                ("usual_driver", "usual_callsign"), "usual_location")
        }),
        ("Contractor Details", {
            "fields": ("contractor_details",)
        }),
        ("Other Details", {
            "fields": ("other_details",)
        })
    )


    class Media:
        js = (
            settings.JQUERY_SOURCE,
            settings.JQUERYUI_SOURCE,
        )

class DeviceSSSAdmin(DeviceAdmin):

    def add_view(self, request, obj=None):
        return HttpResponseRedirect(reverse('sss_admin:tracking_device_changelist'))


@register(LoggedPoint)
class LoggedPointAdmin(ModelAdmin):
    list_display = ("seen", "device")
    list_filter = ("device__symbol", "device__district")
    search_fields = ("device__deviceid", "device__registration")
    date_hierarchy = "seen"

    def add_view(self, request, obj=None):
        return HttpResponseRedirect(reverse('admin:tracking_loggedpoint_changelist'))

    def change_view(self, request, obj=None):
        return HttpResponseRedirect(reverse('admin:tracking_loggedpoint_changelist'))


class TrackingAdminSite(AdminSite):
    site_header = 'SSS administration'
    site_url = None

tracking_admin_site = TrackingAdminSite(name='sss_admin')
tracking_admin_site.register(Device, DeviceSSSAdmin)

