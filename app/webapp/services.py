import json
from aiohttp.web import Response
from worker.services import postprocess


def storefile(file_object):
    filename = file_object[1].filename

    input_file = file_object[1].file

    with open(f'/var/file_deposit/{filename}', 'wb+') as output_file:
        output_file.write(input_file.read())

    return filename


def processaction(item):
    return json.loads(item[1])


def apend_filename(item, filename):
    item['filename'] = filename


async def process(request):
    formdata = await request.post()
    items = formdata.items()

    processed_parameters = list(map(
        processaction,
        filter(
            lambda x: x[0] == 'actions',
            items
        )
    ))

    processed_files = list(map(
        storefile,
        filter(
            lambda x: x[0] == 'files',
            items
        )
    ))

    list(map(
        lambda x: apend_filename(*x),
        zip(
            processed_parameters,
            processed_files
        )
    ))

    postprocess.delay(processed_parameters)

    return Response(text='OK')
