def draw(tree: dict, path: str):
    button_block = list(tree.values())[0]
    head_element = button_block.pop('data')
    html_tree = f'''
    <div class="dropdown">
        <div class="btn-group">
            <a href="{head_element.url}" class="btn btn-secondary">
                {head_element.title}
            </a>
            <button type="button" class="btn btn-secondary dropdown-toggle 
                dropdown-toggle-split" id="dropdownMenuReference" data-toggle="dropdown" 
                aria-haspopup="true" aria-expanded="false" data-reference="parent">
            </button>
        <ul class="dropdown-menu">
    '''
    for value in button_block.values():
        html_tree += draw_element(value, path)
    html_tree += '</ul></div></div>'
    if 'active' in html_tree:
        html_tree = html_tree.replace('on_path"', '" style = "display: block"')
        html_tree = html_tree.replace("btn-group", "btn-group open")
    elif (
        (path in head_element.url or head_element.url in path)
        and abs(len(head_element.url) - len(path)) <= 1
    ):
        html_tree = html_tree.replace("btn-group", "btn-group open")
    return html_tree


def draw_element(element: dict, path: str):
    menu_item = element.get("data")
    if len(element) == 1:
        result = (
            f'<li><a tabindex="-1" href="{menu_item.url}" class="dropdown-item {"active" if menu_item.url == path else ""}">{menu_item.title}</a></li>'
        )
    else:
        result = f'''
            <li class="dropdown-submenu">
                <a class="subtitle dropdown-item {"active" if menu_item.url == path else ""}" tabindex="-1" href="{menu_item.url}">{menu_item.title} <span class="caret"></span> </a>
                <ul class="dropdown-menu {"on_path" if menu_item.url in path or (path in menu_item.url and len(path) == len(menu_item.url) - 1) else ""}">
        '''
        for key, value in element.items():
            if key != 'data':
                result += draw_element(value, path)
        result += '''
                </ul>
            </li>
        '''
    return result
