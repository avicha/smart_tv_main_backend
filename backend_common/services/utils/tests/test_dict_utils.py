# coding=utf-8


def test_dict_pick(dict_utils):
    source_dict = {'x': 1, 'y': 2, 'z': 3}
    target_dict = dict_utils.pick(source_dict, 'x', 'y')
    assert target_dict.has_key('x')
    assert target_dict.has_key('y')
    assert not target_dict.has_key('z')


def test_dict_pick_param_as_array(dict_utils):
    source_dict = {'x': 1, 'y': 2, 'z': 3}
    target_dict = dict_utils.pick(source_dict, ['x', 'y'])
    assert target_dict.has_key('x')
    assert target_dict.has_key('y')
    assert not target_dict.has_key('z')


def test_dict_pick_allow_field_not_exists(dict_utils):
    source_dict = {'x': 1, 'y': 2, 'z': 3}
    target_dict = dict_utils.pick(source_dict, 'x', 'y', 'u', 'v')
    assert target_dict.has_key('x')
    assert target_dict.has_key('y')
    assert target_dict.has_key('u')
    assert target_dict.has_key('v')
    assert target_dict.get('u') == None
    assert target_dict.get('v') == None
    assert not target_dict.has_key('z')


def test_dict_pick_not_allow_field_not_exists(dict_utils):
    source_dict = {'x': 1, 'y': None, 'z': 3}
    target_dict = dict_utils.pick(source_dict, 'x', 'y', 'u', 'v', allow_field_not_exists=False)
    assert target_dict.has_key('x')
    assert target_dict.has_key('y')
    assert not target_dict.has_key('u')
    assert not target_dict.has_key('v')
    assert not target_dict.has_key('z')
