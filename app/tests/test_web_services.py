import mock
from aiohttp import web
from multidict import MultiDict
from webapp.services import (
    storefile,
    process
)


@mock.patch('builtins.open', new_callable=mock.mock_open())
def test_storefile(_open):
    # simple test that verify correct item indexing

    mock_item = mock.Mock()
    
    mock_item = [
        'fakeitemname',
        mock.Mock()
    ]

    mock_item[1].filename = 'fakefilename'
    mock_item[1].file.read = mock.Mock(return_value="filecontents")

    storefile(mock_item)

    _open.assert_called_once_with('/var/file_deposit/fakefilename', 'wb+')
    _open.return_value.__enter__().write.assert_called_once_with('filecontents')


@mock.patch('webapp.services.postprocess')
async def test_process(_postp, aiohttp_client, loop, postdata):
    app = web.Application()
    app.add_routes([
        web.post('/process', process)
    ])

    client = await aiohttp_client(app)

    datacontent = MultiDict([
        ('actions', postdata),
        ('files', open('tests/fixtures/test-pattern.jpeg', 'rb')),
        ('files', open('tests/fixtures/tv-pattern.png', 'rb'))
    ])

    resp = await client.post('/process', data=datacontent)
    response = await resp.content.read()

    _postp.delay.assert_called_once_with(
        {
            'operations': [
                ['resize', '200x300'],
                ['split', True],
                ['blur', 'gaussian'],
                ['blur', 'gaussian'],
                ['split', True]
            ],
            'output': 'jpg'
        },
        [
            'test-pattern.jpeg',
            'tv-pattern.png'
        ]
    )

    assert response == b'OK'
