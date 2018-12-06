"""Generates a jinja template."""
import jinja2


def return_print_var(mem_list, current_member):
    """Creates a variable that changes formatting based on children."""
    new_list = []
    print_var = ''
    for mem in mem_list:
        if mem.family_role == 'Child' or mem.family_role == 'Adult':
            new_list.append(mem)
    if current_member == new_list[0]:
        print_var = '<br>'
    elif current_member == new_list[-1]:
        print_var = ''
    else:
        print_var = ','
    if print_var == '<br>' and len(new_list) > 1:
        return print_var + current_member.name + ','
    elif print_var == '<br>':
        return print_var + current_member.name
    else:
        return current_member.name + print_var

loader = jinja2.FileSystemLoader('./')
Env = jinja2.Environment(loader=loader)
template = Env.get_template('template.html')
template.globals['return_print_var'] = return_print_var
template.globals['len'] = len

def render_template(**people):
    """This renders the jinja template."""
    return template.render(**people)



