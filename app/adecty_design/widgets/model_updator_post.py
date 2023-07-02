#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from flask import redirect, request


def model_updator_post(fields: list, model, url_back: str = '/'):
    for field in fields:
        field_id = field.id
        field_value = request.form.get(field.id)
        if not field_value:
            print('ERROR')

        exec(
            'model.{field_id} = "{field_value}"'.format(
                field_id=field_id,
                field_value=field_value,
            ),
        )

    model.save()
    return redirect(location=url_back), 302
