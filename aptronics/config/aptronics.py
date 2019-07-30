from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Settings"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Assessment",
					"description":_("SPORT.io assessment application")
				}
			]
		},
		{
			"label": _("Assessment"),
			"items": [
				{
					"type": "doctype",
					"name": "Assessment Feedback",
					"description":_("SPORT.io assessment")
				}
			]
		}
	]
