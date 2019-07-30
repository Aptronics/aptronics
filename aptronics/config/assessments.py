from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Assessments"),
			"items": [
				{
					"type": "doctype",
					"name": "Assessments",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Assessment Objectives",
					"onboard": 1,
				}
			]
		}
	]
