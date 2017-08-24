def find(node, tag_name, class_name):
    find_one = node.find(tag_name, class_=class_name)
    if find_one:
        return find_one
    else:
        return None


def find_all(node, tag_name, class_name):
    find_list = node.find_all(tag_name, class_=class_name)
    if len(find_list) == 0:
        return None
    else:
        return find_list


def string(node):
    s = node.string.strip()
    if s:
        return s
    else:
        return None


def h2(node):
    h2_node = node.h2
    if h2_node:
        return h2_node
    else:
        return None


def small(node):
    small_node = node.small
    if small_node:
        return small_node
    else:
        return None


def a(node):
    a_node = node.a
    if a_node:
        return a_node
    else:
        return None


def attri_href(node):
    href = node['href']
    if href:
        return href
    else:
        return None


def find_itemprop(node, tag_name, attribute):
    find_one = node.find(tag_name, itemprop=attribute)
    if find_one:
        return find_one
    else:
        return None


def find_all_itemprop(node, tag_name, attribute):
    find_list = node.find_all(tag_name, itemprop=attribute)
    if len(find_list) == 0:
        return None
    else:
        return find_list


def span(node):
    span_node = node.span
    if span_node:
        return span_node
    else:
        return None


def select_one(node, param):
    element = node.select_one(param)
    if element:
        return element
    else:
        return None


def select(node, param):
    element_list = node.select(param)
    if len(element_list) == 0:
        return None
    else:
        return element_list

parser_map = {
    "find": find,
    "find_all": find_all,
    "string": string,
    "h2": h2,
    "small": small,
    "a": a,
    "attri_href": attri_href,
    "find_itemprop": find_itemprop,
    "find_all_itemprop": find_all_itemprop,
    "span": span,
    "select_one": select_one,
    "select": select
}
