import json
from aiohttp.web import Response
from worker.services import postprocess


def storefile(file_object):
    filename = file_object[1].filename

    input_file = file_object[1].file

    with open(f'/var/file_deposit/{filename}', 'wb+') as output_file:
        output_file.write(input_file.read())

    return filename


async def process(request):
    formdata = await request.post()
    items = formdata.items()

    parameters = json.loads(formdata['actions'])

    processed_files = [
        storefile(item)
        for item in items
        if item[0] == 'files'
    ]

    postprocess.delay(parameters, processed_files)

    return Response(text='OK')
