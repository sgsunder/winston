from settings import settings

def has_role(member, role):
	role_names = [ role.name for role in member.roles ]
	return role in role_names

def has_roles(member, *roles):
	for role in roles:
		if not has_role(member, role):
			return False
	return True

def is_admin(ctx):
	return has_role(ctx.author,  settings.admin_role)

def is_mod(ctx):
	return has_role(ctx.author,  settings.admin_role) or has_role(ctx.author,  settings.mod_role)