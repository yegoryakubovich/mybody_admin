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
from app.adecty_design.widgets.header import header_get
from app.adecty_design.widgets.models_creator_get import models_creator_get, Field
from app.adecty_design.widgets.models_creator_post import models_creator_post
from app.database import Product

URL_BACK = '/parameters/'
FIELDS = [
    Field(id='key', name='Ключ'),
    Field(id='text', name='Текст'),
    Field(id='gender', name='Пол'),
    Field(id='tag', name='Тег'),
]


def interface_parameters_create():
    if request.method == 'POST':
        return models_creator_post(
            fields=FIELDS,
            model=Product(),
            url_back=URL_BACK,
        )

    header = header_get(text='Создать вопрос', url_back=URL_BACK)
    widgets = [
        header,
    ]

    widgets += models_creator_get(
        fields=FIELDS,
    )

    interface_html = interface.html_get(
        widgets=widgets,
        active='parameters',
    )
    return interface_html, 200
