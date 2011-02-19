from models import ImpostorLog
from django.contrib import admin
from django.shortcuts import render_to_response


class ImpostorAdmin(admin.ModelAdmin):
	fields = ('impostor', 'imposted_as', 'logged_in', 'impostor_ip')
	list_display = ('impostor', 'imposted_as', 'impostor_ip', 'logged_in')
	list_editable = ()
	actions_on_top = False
	actions_on_bottom = False
	ordering = ('-logged_in', 'impostor')
	readonly_fields = ('impostor', 'imposted_as', 'impostor_ip', 'logged_in', 'logged_out')
	search_fields = ('impostor__username', 'imposted_as__username')

	def add_view(self, request, form_url='', extra_context=None):
		request.method = 'GET'
		return super(ImpostorAdmin, self).add_view(request, form_url, extra_context)

	def change_view(self, request, form_url='', extra_context=None):
		request.method = 'GET'
		return super(ImpostorAdmin, self).change_view(request, form_url, extra_context)

	def delete_view(self, request, object_id, extra_context=None):
		model = self.model
		opts = model._meta
		app_label = opts.app_label
		return render_to_response('delete_nono.html', {'app_label': app_label, 'opts': opts})



admin.site.register(ImpostorLog, ImpostorAdmin)
