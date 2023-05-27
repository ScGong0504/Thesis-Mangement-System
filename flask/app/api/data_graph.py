from flask import jsonify, g, request


def domain_pic(mode):
    from ..models import Paper, PaperDomain as Paper_domain
    from .domain_manage import get_domain_list_
    if mode == 'user':
        user_id = g.user.id
    else:
        user_id = request.args.get('user_id')
    papers = Paper.query.filter_by(paper_account_id=user_id).all()
    domain_list = []
    domain_dict = {}
    domain_tree = get_domain_list_()

    for one in papers:
        domains = Paper_domain.query.filter_by(paper_id=one.id).all()    # 需要解决paperdomain表的一对多问题
        for domain in domains:
            if domain.domain_name in domain_list:
                domain_dict[domain.domain_name] += 1
            else:
                domain_list.append(domain.domain_name)
                domain_dict[domain.domain_name] = 1
    dict1 = {
        'level1': {},
        'level2': {},
        'level3': {}
    }

    for d1 in domain_tree:
        l1 = d1.get('label')
        if l1 in domain_list:
            dict1['level1'][l1] = domain_dict[l1]
        else:
            dict1['level1'][l1] = 0
        children1 = d1.get('children')
        if len(children1) != 0:
            for d2 in children1:
                l2 = d2.get('label')
                if l2 in domain_list:
                    dict1['level1'][l1] += domain_dict[l2]
                    dict1['level2'][l2] = domain_dict[l2]
                else:
                    dict1['level2'][l2] = 0
                children2 = d2.get('children')
                if len(children2) != 0:
                    for d3 in children2:
                        l3 = d3.get('label')
                        if l3 in domain_list:
                            dict1['level1'][l1] += domain_dict[l3]
                            dict1['level2'][l2] += domain_dict[l3]
                            dict1['level3'][l3] = domain_dict[l3]
                        else:
                            dict1['level3'][l3] = 0
    dict1['level1_total'] = len(dict1['level1'])
    dict1['level2_total'] = len(dict1['level2'])
    dict1['level3_total'] = len(dict1['level3'])
    return jsonify({'code': 200, 'value': dict1})
