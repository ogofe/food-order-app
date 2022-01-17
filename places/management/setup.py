from ..models import *


ADMIN_MODELS = [
	Customer,
	Staff,
	FoodItem,
	Order,
]	

def create_add_permission(model):
	for model in ADMIN_MODELS:
		perm = StaffPermissions(
			code_name=f'add {model.__class__.__name__}'
			)
	return True



def create_edit_permission(model):
	for model in ADMIN_MODELS:
		perm = StaffPermissions(
			code_name=f'edit {model.__class__.__name__}'
			)
	return True



def create_view_permission(model):
	for model in ADMIN_MODELS:
		perm = StaffPermissions(
			code_name=f'view {model.__class__.__name__}'
			)
	return True



def create_delete_permission(model):
	for model in ADMIN_MODELS:
		perm = StaffPermissions(
			code_name=f'delete {model.__class__.__name__}'
			)
	return True




def create_permissions():
	create_add_permission()
	create_edit_permission()
	create_view_permission()
	create_delete_permission()
	return True




