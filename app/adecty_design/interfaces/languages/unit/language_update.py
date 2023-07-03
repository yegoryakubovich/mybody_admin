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


from flask import request

from app.adecty_design.interface import interface
from app.adecty_design.widgets.field import Field
from app.adecty_design.widgets.header import header_get
from app.adecty_design.widgets.model_updater_get import model_updator_get
from app.adecty_design.widgets.model_updator_post import model_updator_post
from app.database.models import Language

URL_BACK = '/languages/'
FIELDS = [
    Field(id='name', name='Название языка'),
]


def interface_language_update(language: Language):
    if request.method == 'POST':
        return model_updator_post(
            fields=FIELDS,
            model=language,
            url_back=URL_BACK,
        )

    header = header_get(text='Редактирование языка', url_back=URL_BACK)
    widgets = [
        header,
    ]

    widgets += model_updator_get(
        fields=FIELDS,
        model=language,
    )

    interface_html = interface.html_get(
        widgets=widgets,
        active='languages',
    )
    return interface_html, 200
