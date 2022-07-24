import datetime
import jinja2

if __name__ == '__main__':
    loader = jinja2.PackageLoader('nepub')
    env = jinja2.Environment(
        loader=loader,
        autoescape=True
    )
    # template = env.get_template('content.opf')
    # result = template.render({
    #     'title': 'たいとる',
    #     'author': '作者',
    #     'created_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    #     'episodes': [{
    #         'id': '001'
    #     }, {
    #         'id': '002'
    #     }]
    # })
    # print(result)

    template = env.get_template('navigation.xhtml')
    result = template.render({
        'chapters': [
            {
                'name': 'default',
                'episodes': []
            }, {
                'name': 'ちゃぷたー1',
                'episodes': [
                    {
                        'id': '001',
                        'title': 'たいとる1',
                        'paragraphs': []
                    }, {
                        'id': '002',
                        'title': 'たいとる2',
                        'paragraphs': []
                    }
                ]
            }, {
                'name': 'ちゃぷたー2',
                'episodes': [
                    {
                        'id': '003',
                        'title': 'たいとる3',
                        'paragraphs': []
                    }
                ]
            }
        ]
    })
    print(result)